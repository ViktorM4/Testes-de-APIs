import requests
from dotenv import load_dotenv
import os 
from datetime import datetime
import schedule
import time
import sqlite3
import logging

load_dotenv()

API_key = os.getenv("API_key")
cidade = os.getenv("CIDADE")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)



def consumirApi(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}"

    response = requests.get(url)

    if response.status_code == 200:
        dados = response.json()
        return(round(dados["main"]["temp"] - 273.15, 2))
    else: 
        logging.error(response.text)

    if response.status_code == 429:
    logging.warning("Rate limit atingido, aguardando próxima execução")
    return None




def geoLocal(cidade):
    
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={cidade}&limit=1&appid={API_key}"
   

    response = requests.get(url)
    if response.status_code == 200:
        dados1 = response.json()
        return dados1[0]["lat"], dados1[0]["lon"]
    else: 
        logging.error(response.text)

#lat, lon = geoLocal(input("Informe sua cidade: "))




def cotacao():
    url = f"https://economia.awesomeapi.com.br/json/last/USD-BRL"

    response = requests.get(url)
    if response.status_code == 200:
        valor = response.json()
        return (valor["USDBRL"]["bid"])
    else: 
        logging.error(response.text)

    if response.status_code == 429:
    logging.warning("Rate limit atingido, aguardando próxima execução")
    return None

with sqlite3.connect("/app/dados/dados.db") as conn:
    conn.execute("""
    CREATE TABLE IF NOT EXISTS registros(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data_hora TEXT,
    temperatura TEXT,
    cotacao TEXT)
    """)



def job():
    try:
        lat, lon = geoLocal(cidade)
        if lat is None:
            return

        temperatura = consumirApi(lat, lon)
        if temperatura is None:
            logging.error("Temperatura inválida, abortando inserção")
            return

        valor = cotacao()
        if valor is None:
            logging.error("Cotação inválida, abortando inserção")
            return

        agora = datetime.now().strftime("%d/%m/%Y %H:%M")
        with sqlite3.connect("/app/dados/dados.db") as conn:
            conn.execute("""
                INSERT INTO registros (data_hora, temperatura, cotacao)
                VALUES (?,?,?)
            """, (agora, temperatura, valor))
        logging.info(f"Dados de {cidade} adicionado, {temperatura}°C, cotação R$:{valor}")

    except Exception as e:
        logging.error(f"erro: {e}")

logging.info("SIstema Iniciado")

job()

schedule.every(60).minutes.do(job)


while True:
    schedule.run_pending()
    time.sleep(1)



