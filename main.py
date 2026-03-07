import requests
from dotenv import load_dotenv
import os 

load_dotenv()
API_key = os.getenv("API_key")




def consumirApi(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}"

    response = requests.get(url)

    if response.status_code == 200:
        dados = response.json()
        print(round(dados["main"]["temp"] - 273.15, 2))
    else: 
        print(response.text)




def geoLocal(cidade):
    
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={cidade}&limit=1&appid={API_key}"
   

    response = requests.get(url)
    if response.status_code == 200:
        dados1 = response.json()
        return dados1[0]["lat"], dados1[0]["lon"]
    else: 
        print(response.text)

#lat, lon = geoLocal(input("Informe sua cidade: "))




def cotacao():
    url = f"https://economia.awesomeapi.com.br/json/last/USD-BRL"

    response = requests.get(url)
    if response.status_code == 200:
        valor = response.json()
        print("Dolar hoje vale R$: ",(valor["USDBRL"]["bid"]))
    else: 
        print(response.text)

#cotacao()

print("Escolha 1 para clima e 2 para cotação: ")
escolha = input("Escolha: ")
if escolha == "1":
        lat, lon = geoLocal(input("Informe sua cidade: "))
        consumirApi(lat, lon)
else: 
    cotacao()


    
    

