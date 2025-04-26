from datetime import datetime, timedelta
from .models import Concurso, Disciplina, Topico, SessaoEstudo, db

def gerar_cronograma(concurso_id, horas_diarias):
    concurso = Concurso.query.get(concurso_id)
    dias_disponiveis = (concurso.data_prova - datetime.now().date()).days

    if dias_disponiveis <= 0:
        return []

    disciplinas = Disciplina.query.filter_by(concurso_id=concurso_id).all()
    total_peso = sum(1 if d.prioridade == 'baixa' else 2 if d.prioridade == 'media' else 3 for d in disciplinas)

    cronograma = []
    dia_atual = datetime.now().date()
    dias_utilizados = [0] * dias_disponiveis  # Para controlar a quantidade de estudos por dia

    for d in disciplinas:
        peso = 1 if d.prioridade == 'baixa' else 2 if d.prioridade == 'media' else 3
        carga_total_disciplina = (peso / total_peso) * horas_diarias * dias_disponiveis
        topicos = d.topicos
        if not topicos:
            continue
        tempo_por_topico = carga_total_disciplina / len(topicos)

        for t in topicos:
            dia_ideal = dias_utilizados.index(min(dias_utilizados))
            dias_utilizados[dia_ideal] += tempo_por_topico
            data_estudo = dia_atual + timedelta(days=dia_ideal)
            cronograma.append({
                'data': data_estudo.isoformat(),
                'disciplina': d.nome,
                'topico': t.nome,
                'tempo_estimado': round(tempo_por_topico, 2)
            })

    cronograma.sort(key=lambda x: x['data'])
    return cronograma

def calcular_progresso(concurso_id):
    topicos = Topico.query.join(Disciplina).filter(Disciplina.concurso_id == concurso_id).all()
    total_topicos = len(topicos)
    estudados = SessaoEstudo.query.join(Topico).join(Disciplina).filter(
        Disciplina.concurso_id == concurso_id
    ).distinct(SessaoEstudo.topico_id).count()
    tempo_total = db.session.query(db.func.sum(SessaoEstudo.tempo_minutos)).join(Topico).join(Disciplina).filter(
        Disciplina.concurso_id == concurso_id).scalar() or 0

    return {
        'progresso_percentual': round((estudados / total_topicos) * 100, 2) if total_topicos > 0 else 0,
        'tempo_total_estudado': tempo_total
    }

def sugestao_revisao(concurso_id):
    revisoes = []
    sessoes = SessaoEstudo.query.join(Topico).join(Disciplina).filter(Disciplina.concurso_id == concurso_id).all()
    datas_revisao = {}

    for sessao in sessoes:
        if sessao.topico_id not in datas_revisao or sessao.data > datas_revisao[sessao.topico_id]:
            datas_revisao[sessao.topico_id] = sessao.data

    for topico_id, data_sessao in datas_revisao.items():
        dias_passados = (datetime.now().date() - data_sessao).days
        if dias_passados in [1, 3, 7, 14, 30]:
            topico = Topico.query.get(topico_id)
            revisoes.append({
                'data_revisao': datetime.now().date().isoformat(),
                'topico': topico.nome,
                'disciplina': topico.disciplina.nome
            })

    return revisoes
