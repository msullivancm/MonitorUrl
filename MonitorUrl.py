import requests
import json
import time
from datetime import datetime

#função para testar a url e retornar código
def test(url):
    response = str(requests.get(url))
    ret=0
    if response[11]=='2':
        print("Serviço em operação!")
        ret=response[11:14]
    if response[11]=='4':
        print("Problema na regra de negócio")
        ret=response[11:14]
    if response[11]=='5':
        print("Serviço indisponível!")
        ret=response[11:14]
    return ret
#Variáveis auxiliares
cont=0 #contador de loops
result=0 #retorna o código a ser tratado
r2xx=0 #código da família 2XX
r4xx=0 #código da família 4XX
r5xx=0 #código da família 5XX
ciclo=0 #Conta o ciclo de loops até o número determinado.

#Cria o arquivo de log
arquivo = open('monitoramento.log','w')

#loop infinito
while(ciclo < 20):
    ciclo+=1 #Inicia novo ciclo
    time.sleep(2) #a cada 2 segundos
    result=test('https://desafioperformance.b2w.io/bairros') #testa a url e retorna código
    if result=='2':
        r2xx+=1
    if result=='4':
        r4xx+=1
    if result=='5':
        r5xx+=1
    cont+=1
    if cont==30:
        print("passou um minuto") #a cada minuto salva o teste acumulado
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        #Grava o acumulado do minuto numa linha do arquivo
        arquivo.write(datetime.now().strftime("%Y-%m-%d %H:%M")+","+str(r2xx)+","+str(r5xx)+","+str(r5xx)+"\n")
        #Quando verificamos código 5XX maior que 2XX, ou seja, site indisponível, reinicia o servço através da api correspondente
        if r5xx > r2xx:
            requests.put('https://desafioperformance.b2w.io/reinicia')
        cont=0
        result=0
        r2xx=0
        r4xx=0
        r5xx=0
        
arquivo.close() #Fecha o arquivo
        
