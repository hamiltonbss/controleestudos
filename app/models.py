from . import db

class Concurso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    banca = db.Column(db.String(100))
    data_prova = db.Column(db.Date)
    disciplinas = db.relationship('Disciplina', backref='concurso')

class Disciplina(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    prioridade = db.Column(db.String(10))
    concurso_id = db.Column(db.Integer, db.ForeignKey('concurso.id'))
    topicos = db.relationship('Topico', backref='disciplina')

class Topico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    prioridade = db.Column(db.String(10))
    disciplina_id = db.Column(db.Integer, db.ForeignKey('disciplina.id'))
    revisado = db.Column(db.Boolean, default=False)

class SessaoEstudo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topico_id = db.Column(db.Integer, db.ForeignKey('topico.id'))
    tempo_minutos = db.Column(db.Integer)
    compreensao = db.Column(db.String(10))
    data = db.Column(db.Date)
