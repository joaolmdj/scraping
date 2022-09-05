import os
import re
import pandas as pd
from bs4 import BeautifulSoup

Data = []
Titulo = []
Ipc = []
Resultado = []
Pedidos = []
Arquivo = []
Cnpj = []

def MakingMagic():
    count = 0
    for file in os.listdir('.'):
        if file.endswith(".html") and file != "patentes.html":
            count += 1
            html_doc = file

            html_report = open(html_doc, 'r')
            soup = BeautifulSoup(html_report, 'html.parser')

            file_name = os.path.splitext(html_doc)[0]
            Arquivo.append(file_name)

            cnpj = soup.table.find_all("div", attrs={"id": "tituloEResumoContext"})
            cnpj = re.sub('[^0-9]', '', str(cnpj))
            if cnpj == '':
                cnpj = soup.find_all("div", attrs={"align": "left"})
                cnpj = cnpj[1].contents
                cnpj = re.sub('[^0-9]', '', str(cnpj))
            Cnpj.append(cnpj)

            resultado = 0

            for pedido in soup.table.find_all("a", attrs={"class": "visitado"}):
                pedido = pedido.get_text(strip=True)

                Pedidos.append(pedido)
                resultado += 1
            Resultado.append(resultado)


            if resultado != 0:
                contador = resultado - 1
                while contador != 0:
                    Cnpj.append(cnpj)
                    Resultado.append(resultado)
                    Arquivo.append(file_name)
                    contador -= 1

                for data in soup.find_all("font", attrs={"id": "data"}):
                    data = data.get_text(strip=True)
                    Data.append(data)

                for titulo in soup.find_all("font", attrs={"id": "titulo"}):
                    titulo = titulo.get_text(strip=True)
                    Titulo.append(titulo)

                for ipc in soup.table.find_all("font", attrs={"class": "alerta"}):
                    ipc = ipc.get_text(strip=True)
                    Ipc.append(ipc)
            else:
                Pedidos.append('-')
                Data.append('-')
                Titulo.append('-')
                Ipc.append('-')
        
            df = pd.DataFrame(zip(Arquivo, Cnpj, Resultado, Pedidos, Data, Titulo,  Ipc), columns=['Arquivo', 'CNPJ', 'Resultado', 'Pedidos', 'Data', 'Titulo', 'IPC'])

    print(df)
    html = df.to_html()
    text_file = open("patentes.html", "w")
    text_file.write(html)
    text_file.close()

MakingMagic()

# @joaolmdj