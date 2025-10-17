document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('form-candidato');
    const statusDiv = document.getElementById('upload-status');

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        statusDiv.textContent = 'Enviando...';
        statusDiv.style.color = '#2d3e50';

        const formData = new FormData(form);
        if (!formData.get('arquivo') || !formData.get('nome')) {
            statusDiv.textContent = 'Por favor, preencha o nome e selecione o PDF.';
            statusDiv.style.color = 'red';
            return;
        }

        fetch('http://localhost:5000/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log(data); // Adicionado para depuração
            if (data.sucesso) {
                statusDiv.textContent = 'Perfil enviado com sucesso!';
                statusDiv.style.color = 'green';
                if (data.top5 && Array.isArray(data.top5)) {
                    let html = '';
                    data.top5.forEach((perfil, idx) => {
                        html += `<div class='perfil'><strong>${idx+1}. ${perfil.nome}</strong><br>Aderência: <b>${perfil.aderencia}%</b><br>Motivo: ${perfil.motivo}</div>`;
                    });
                    document.getElementById('resultados-perfis').innerHTML = html;
                }
            } else {
                statusDiv.textContent = data.erro || 'Erro ao enviar perfil.';
                statusDiv.style.color = 'red';
            }
        })
        .catch(() => {
            statusDiv.textContent = 'Erro ao enviar perfil.';
            statusDiv.style.color = 'red';
        });
    });
});
