import requests
from dotenv import load_dotenv
import os 
from datetime import datetime
import schedule
import time
import sqlite3

load_dotenv()

API_key = os.getenv("API_key")
cidade = os.getenv("CIDADE")



def consumirApi(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}"

    response = requests.get(url)

    if response.status_code == 200:
        dados = response.json()
        return(round(dados["main"]["temp"] - 273.15, 2))
    else: 
        print(response.text)




def geoLocal(cidade):
    
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={cidade}&limit=1&appid={API_key}"
   

    response = requests.get(url)
    if response.status_code == 200:
        dados1 = response.json()
        return dados1[0]["lat"], dados1[0]["lon"]
    else: 
        return(response.text)

#lat, lon = geoLocal(input("Informe sua cidade: "))




def cotacao():
    url = f"https://economia.awesomeapi.com.br/json/last/USD-BRL"

    response = requests.get(url)
    if response.status_code == 200:
        valor = response.json()
        return (valor["USDBRL"]["bid"])
    else: 
        return(response.text)





def job():

    conn = sqlite3.connect("/app/dados/dados.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS registros(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data_hora TEXT,
    temperatura TEXT,
    cotacao TEXT)
    """)
    conn.commit()


    lat, lon = geoLocal(cidade)
    temperatura = consumirApi(lat, lon)
    valor = cotacao()
    agora = datetime.now().strftime("%d/%m/%Y %H:%M")
    cursor.execute("""
    INSERT INTO registros (data_hora, temperatura, cotacao)
    VALUES (?,?,?)
    """, (agora, temperatura, valor))
    conn.commit()

    conn.close()


schedule.every(10).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)



