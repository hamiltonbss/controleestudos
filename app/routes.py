from flask import render_template, request
from .models import Concurso, Disciplina, SessaoEstudo
from .services import gerar_cronograma, calcular_progresso, sugestao_revisao

@app.route('/')
def home():
    concursos = Concurso.query.all()
    return render_template('concurso_listar.html', concursos=concursos)

@app.route('/cronograma/<int:concurso_id>')
def cronograma(concurso_id):
    concurso = Concurso.query.get_or_404(concurso_id)
    cronograma = gerar_cronograma(concurso_id, horas_diarias=4)  # Exemplo com 4 horas de estudo diárias
    return render_template('cronograma.html', concurso=concurso, cronograma=cronograma)

@app.route('/progresso/<int:concurso_id>')
def progresso(concurso_id):
    progresso = calcular_progresso(concurso_id)
    revisoes = sugestao_revisao(concurso_id)
    disciplinas = Disciplina.query.filter_by(concurso_id=concurso_id).all()
    return render_template('progresso.html', progresso=progresso, revisoes=revisoes, disciplinas=disciplinas)
