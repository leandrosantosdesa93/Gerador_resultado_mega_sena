import pandas as pd
from flask import Flask, render_template
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import random

app = Flask(__name__)

# Função para gerar o novo resultado
def gerar_novo_resultado():
    caminho_arquivo = './resultados_mega_sena.csv'
    dados = pd.read_csv(caminho_arquivo)
    dados.fillna(0, inplace=True)
    features = dados[['bola 1', 'bola 2', 'bola 3', 'bola 4', 'bola 5', 'bola 6']]
    target = dados['Concurso']
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

    modelo = LinearRegression()
    modelo.fit(X_train, y_train)

    novo_resultado = None
    while True:
        novo_resultado = set()  # Usar um set para garantir números únicos
        while len(novo_resultado) < 6:
            novo_numero = random.randint(1, 60)
            novo_resultado.add(novo_numero)

        novo_resultado = sorted(list(novo_resultado))  # Ordenar os números gerados

        resultado_existente = dados[
            (dados['bola 1'] == novo_resultado[0]) &
            (dados['bola 2'] == novo_resultado[1]) &
            (dados['bola 3'] == novo_resultado[2]) &
            (dados['bola 4'] == novo_resultado[3]) &
            (dados['bola 5'] == novo_resultado[4]) &
            (dados['bola 6'] == novo_resultado[5])
        ]
        
        if resultado_existente.empty:
            break

    novo_resultado_dict = {
        'bola 1': novo_resultado[0],
        'bola 2': novo_resultado[1],
        'bola 3': novo_resultado[2],
        'bola 4': novo_resultado[3],
        'bola 5': novo_resultado[4],
        'bola 6': novo_resultado[5],
    }

    novo_resultado_df = pd.DataFrame(novo_resultado_dict, index=[0])
    dados = pd.concat([dados, novo_resultado_df], ignore_index=True)
    dados.to_csv(caminho_arquivo, index=False)

    return novo_resultado

# Rota para a página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para gerar o novo resultado
@app.route('/gerar_resultado', methods=['POST'])
def gerar_novo_resultado_rota():
    novo_resultado = gerar_novo_resultado()
    return render_template('resultado.html', novo_resultado=novo_resultado)

if __name__ == '__main__':
    app.run(debug=True)
