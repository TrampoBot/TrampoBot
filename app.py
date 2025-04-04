from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def buscar_vagas(termo, local):
    url = f'https://www.google.com/search?q=site:linkedin.com/jobs+{termo}+{local}'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    vagas = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and 'linkedin.com/jobs' in href:
            vagas.append(href)
    
    return vagas[:10]  # Retorna até 10 vagas

@app.route('/')
def home():
    return "<h1>TrampoBot - O Caça Trampo</h1><p>API rodando...</p>"

@app.route('/buscar', methods=['GET'])
def buscar():
    termo = request.args.get('termo', '')
    local = request.args.get('local', '')
    if not termo:
        return jsonify({'erro': 'Especifique um termo de busca'}), 400
    
    vagas = buscar_vagas(termo, local)
    return jsonify({'vagas': vagas})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
