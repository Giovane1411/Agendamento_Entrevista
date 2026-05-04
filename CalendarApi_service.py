from google.oauth2.credentials import Credentials
import os.path
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


# Aqui vou definir que tipo de permissão o meu projeto vai ter
SCOPES = ["https://www.googleapis.com/auth/calendar"]

#Aqui vou fazer a função para conectar com o google calendar
def conectar_google_calendar():
    creds = None #variável para armazenar as credenciais, inicialmente vai ser nula.]

    if os.path.exists("token.json"): #verificar se o arquivo de token existe
        creds = Credentials.from_authorized_user_file("token.json", SCOPES) # Se existir, significa que as credenciais foram autorizadas, então eu vou carregar as credenciais a partir do arquivo token.json

    if not creds or not creds.valid: # verifica se não existe ou se as credenciais são inválida:
        if creds and creds.expired and creds.refresh_token: # Se as credenciais existirem e tiverem expirada e podem ser renovadas automaticamente, então eu vou renovar as credenciais:
            creds.refresh(Request()) # Solicitar a renovação das credenciais usando o método refresh()
        else:
            # Se as credenciais não existirem ou não puderem ser renovadas, então eu vou iniciar o processo de autorização para obter novas credenciais
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", 
                SCOPES
            )
            creds = flow.run_local_server(port=0) # Iniciar um servidor local para o processo de autorização, onde o usuário pode conceder permissão para acessar o Google Calendar. O método run_local_server() é usado para iniciar esse processo.
        with open("token.json", "w") as token: # depois de obter as credenciais, eu vou salvar as credenciais em um arquivo token.json para uso futuro, evitando a necessidade de autorizar novamente.
            token.write(creds.to_json()) # Escrever as credenciais no arquivo token.json em formato JSON usando o método to_json() das credenciais.

    service = build("calendar", "v3", credentials=creds) # Criar um serviço para interagir com a API do Google Calendar usando as credenciais obtidas. O método build() é usado para criar esse serviço, especificando a API (calendar), a versão (v3) e as credenciais.
    return service # Retornar o serviço criado para ser usado em outras partes do código.