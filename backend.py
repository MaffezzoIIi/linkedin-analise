import os
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import PyPDF2
from flask_cors import CORS

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

vaga = {
    "grau_escolaridade": "Graduação completa em Ciência da Computação ou áreas correlatas",
    "conhecimentos_desejados": ["Scrum", "Docker", "Kubernetes", "UI/UX", "APIs REST"], 
    "conhecimentos_obrigatorios": ["Python", "PostgreSQL", "Git", "APIs", "Java"],
    "tempo_experiencia": 3,
    "observacoes": "Inglês intermediário e trabalho híbrido em São Paulo"
}

app = Flask(__name__)
CORS(app)  # Permite CORS para todas as rotas
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Lista global para armazenar perfis analisados
perfis_armazenados = []

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extrair_texto_pdf(filepath):
    texto = ""
    with open(filepath, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            texto += page.extract_text() or ""
    return texto

def calcular_aderencia(texto):
    score = 0
    motivos = []
    total = 0
    # Checa obrigatórios
    for item in vaga["conhecimentos_obrigatorios"]:
        total += 1
        if item.lower() in texto.lower():
            score += 1
            motivos.append(f"Possui conhecimento obrigatório: {item}")
    # Checa desejados
    for item in vaga["conhecimentos_desejados"]:
        total += 0.5
        if item.lower() in texto.lower():
            score += 0.5
            motivos.append(f"Possui conhecimento desejado: {item}")
    # Checa tempo de experiência
    if str(vaga["tempo_experiencia"]) in texto:
        score += 1
        total += 1
        motivos.append("Tempo de experiência compatível")
    aderencia = round((score / total) * 100, 2) if total > 0 else 0
    motivo = "; ".join(motivos) if motivos else "Pouca aderência identificada"
    return aderencia, motivo

@app.route('/upload', methods=['POST'])
def upload():
    if 'arquivo' not in request.files or 'nome' not in request.form:
        return jsonify({'sucesso': False, 'erro': 'Dados incompletos.'}), 400
    file = request.files['arquivo']
    nome = request.form['nome']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'sucesso': False, 'erro': 'Arquivo inválido.'}), 400
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    try:
        texto = extrair_texto_pdf(filepath)
        aderencia, motivo = calcular_aderencia(texto)
        perfil = {'nome': nome, 'aderencia': aderencia, 'motivo': motivo}
        perfis_armazenados.append(perfil)
        # Ordena e pega os top 5
        top5 = sorted(perfis_armazenados, key=lambda x: x['aderencia'], reverse=True)[:5]
        return jsonify({'sucesso': True, 'top5': top5})
    except Exception as e:
        return jsonify({'sucesso': False, 'erro': f'Erro ao processar PDF: {str(e)}'}), 500

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    if path != "" and os.path.exists(os.path.join('frontend', path)):
        return send_from_directory('frontend', path)
    else:
        return send_from_directory('frontend', 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
