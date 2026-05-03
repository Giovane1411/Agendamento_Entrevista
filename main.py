from fastapi import FastAPI
import json
import api_service

app = FastAPI()

resultados = []
candidatos = []
vagas = []
agendamentos = []

@app.get("/")
def home():
    return {"mensagem": "API RH funcionando"}

# -------------------------
# CANDIDATOS
# -------------------------

@app.post("/candidatos")
def criar_candidato(nome: str, habilidade: str):
    candidato = {
        "id": len(candidatos) + 1,
        "nome": nome,
        "habilidade": habilidade
    }
    candidatos.append(candidato)
    return candidato

@app.get("/candidatos")
def listar_candidatos():
    for candidato in candidatos:
        return candidato

# -------------------------
# VAGAS
# -------------------------

@app.post("/vagas")
def criar_vaga(titulo: str, habilidade: str):
    vaga = {
        "id": len(vagas) + 1,
        "titulo": titulo,
        "habilidade": habilidade
    }
    vagas.append(vaga)
    return vaga

@app.get("/vagas")
def listar_vagas():
    return vagas

# -------------------------
# MATCH
# -------------------------

@app.get("/match")
def match():
    for candidato in candidatos:
        for vaga in vagas:
            if candidato["habilidade"] == vaga["habilidade"]:
                resultados.append({
                    "candidato": candidato["nome"],
                    "vaga": vaga["titulo"]
                })

    return resultados

# ---------------------------------
# AGENDAMENTO ENTREVISTA PRESENCIAL
# ---------------------------------
@app.post("/agendamento")
def criar_agendamento(
    candidato: str,
    vaga: str,
    data_inicio: str,
    data_fim: str,
    indicado: str
    # Formato da data: "YYYY-MM-DDTHH:MM:SS-03:00"
):
    candidatos = listar_candidatos()
    resultado_match = match()

    candidato_valido = any(candidato == candidatos["nome"]
                           for candidato in candidatos
                           )

    
    match_valido = any(resultado["candidato"] == candidato and resultado["vaga"] == vaga
                       for resultado in resultado_match 
                       )
    if match_valido or indicado == "sim" and candidato_valido:
        # Aqui estou chamando a API para posteriormente agendar a entrevista no google calendar.
        service = api_service.conectar_google_calendar()

        evento = {
            "summary": f"Entrevista - {candidato}",
            "description": f"Entrevista para a vaga: {vaga}",
            "start": {
                "dateTime": data_inicio,
                "timeZone": "America/Sao_Paulo",
            },
            "end":{
                "dateTime": data_fim,
                "timeZone": "America/Sao_Paulo",
            },
        }
        evento_criado = service.events().insert(
            calendarId="primary",
            body=evento
        ).execute()

        agendamento = {
            "id": len(agendamentos) + 1,
            "candidato": candidato,
            "vaga": vaga,
            "data_inicio": data_inicio,
            "data_fim": data_fim,
            "link_google_agenda": evento_criado.get("htmlLink")
        }

        agendamentos.append(agendamento)

        return agendamento
    else:
        return {"mensagem": "Candidato e vaga não são compatíveis para agendamento."}

# Listar os agendamentos criados
@app.get("/agendamento")
def listar_agendamentos():
    return agendamentos