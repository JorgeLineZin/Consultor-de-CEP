from app import app
from flask import render_template, request
import requests


@app.route("/", methods=["GET", "POST"])
def home():
    dados_endereco = None
    erro = None
    cep_consultado = None

    if request.method == "POST":
        cep = request.form.get("cep", "").strip()
        # Remove caracteres não numéricos (hífen, espaços)
        cep = "".join(filter(str.isdigit, cep))

        if len(cep) != 8:
            erro = "CEP inválido. Digite 8 números."
        else:
            # Consulta ViaCEP
            try:
                response = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
                if response.status_code == 200:
                    dados = response.json()
                    if "erro" in dados:
                        erro = "CEP não encontrado."
                    else:
                        dados_endereco = dados
                        cep_consultado = cep
                else:
                    erro = "Erro ao consultar o serviço ViaCEP. Tente novamente."
            except requests.exceptions.RequestException:
                erro = "Falha de conexão. Verifique sua internet."

    # return render_template("home.html", dados_endereco=dados_endereco, erro=erro, cep_consultado=cep_consultado,)
    return render_template(
        "home.html",
        dados_endereco=dados_endereco,
        erro=erro,
        cep_consultado=cep_consultado,
    )
