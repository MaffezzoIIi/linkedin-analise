import csv
import random

# Descrição fictícia da vaga
vaga = {
    "grau_escolaridade": "Graduação completa em Ciência da Computação ou áreas correlatas",
    "conhecimentos_desejados": ["Scrum", "Docker", "Kubernetes", "UI/UX", "APIs REST"],
    "conhecimentos_obrigatorios": ["Python", "PostgreSQL", "Git", "APIs"],
    "tempo_experiencia": 3,
    "observacoes": "Inglês intermediário e trabalho híbrido em São Paulo"
}

# Função para calcular aderência (simulada)
def calcular_aderencia(perfil):
    # Simula uma pontuação com base em palavras-chave encontradas (mock)
    score = random.uniform(60, 100)
    motivos = [
        "Possui experiência sólida com Python e APIs REST",
        "Conhecimento relevante em PostgreSQL e Docker",
        "Boa aderência aos requisitos técnicos e tempo de experiência"
    ]
    return round(score, 2), random.choice(motivos)

# Leitura do dataset com links (CSV)
# Exemplo de arquivo: candidatos.csv
# nome,linkedin_url
# Thomas Maffezzolli,https://www.linkedin.com/in/thomas-maffezzolli-8b029714a/

def ler_dataset(caminho_csv):
    candidatos = []
    with open(caminho_csv, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            candidatos.append(row)
    return candidatos

def analisar_perfis(caminho_csv):
    candidatos = ler_dataset(caminho_csv)
    resultados = []

    for candidato in candidatos:
        score, motivo = calcular_aderencia(candidato)
        resultados.append({
            "nome": candidato["nome"],
            "linkedin": candidato["linkedin_url"],
            "aderencia": score,
            "motivo": motivo
        })

    # Ordena por maior aderência
    top5 = sorted(resultados, key=lambda x: x["aderencia"], reverse=True)[:5]

    print("Top 5 perfis mais aderentes à vaga:\n")
    for i, perfil in enumerate(top5, start=1):
        print(f"{i}. {perfil['nome']} - {perfil['aderencia']}% de aderência")
        print(f"   LinkedIn: {perfil['linkedin']}")
        print(f"   Motivo: {perfil['motivo']}\n")

# Exemplo de execução
if __name__ == "__main__":
    analisar_perfis("data/candidatos.csv")
