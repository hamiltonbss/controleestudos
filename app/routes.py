from flask import request, jsonify, current_app as app
from .models import db, Concurso, Disciplina, Topico, SessaoEstudo
from datetime import datetime

@app.route('/')
def index():
    return jsonify({"mensagem": "API de Estudos Pessoais"})

@app.route('/concurso', methods=['POST'])
def cadastrar_concurso():
    data = request.get_json()
    concurso = Concurso(
        nome=data['nome'],
        banca=data['banca'],
        data_prova=datetime.strptime(data['data_prova'], "%Y-%m-%d")
    )
    db.session.add(concurso)
    db.session.commit()
    return jsonify({"id": concurso.id}), 201
