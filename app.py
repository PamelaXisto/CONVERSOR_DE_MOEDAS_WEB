import requests
from flask import Flask, render_template, request
import os

app = Flask (__name__)

def obter_taxas():
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    response = requests.get(url)
    data = response.json()
    return data['rates']

def converter_moedas(valor, moeda_origem, moeda_destino, taxas):
    if moeda_origem in taxas and moeda_destino in taxas:
        taxa_origem = taxas[moeda_origem]
        taxa_destino = taxas[moeda_destino]
        valor_em_usd = valor / taxa_origem
        valor_convertido = valor_em_usd * taxa_destino
        return valor_convertido
    else:
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = None
    erro = None
    if request.method == 'POST':
        try:
            valor = float(request.form['valor'])
            moeda_origem = request.form['moeda_origem'].upper()
            moeda_destino = request.form['moeda_destino'].upper()
            taxas = obter_taxas()
            valor_convertido = converter_moedas(valor, moeda_origem, moeda_destino, taxas)
            
            if valor_convertido is not None:
                resultado = f'{valor:.2f} {moeda_origem} é equivalente a {valor_convertido:.2f} {moeda_destino}'
            else:
                erro = 'Moedas não encontradas ou inválidas.'
        except ValueError:
            erro = 'Valor inválido. Digite um número.'
    return render_template('index.html', resultado=resultado, erro=erro)

if __name__ == '__main__':
    import os
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)), debug=True)
