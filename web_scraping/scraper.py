import requests
from bs4 import BeautifulSoup
import os

from twisted.spread.pb import respond

url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
pasta_downloads = "arquivos"

os.makedirs("arquivos", exist_ok=True)

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

for link in soup.find_all("a"):
    href=link.get("href")
    if href and href.endswith(".pdf") and ("Anexo I" in link.text or "Anexo II" in link.text):
        pdf_url = href if href.startwith("http") else url + href
        arquivos = os.path.join(arquivos, pdf_url.split("/")[-1])

        print(f"Baixando: {arquivos}")
        pdf_response = requests.get(pdf_url)

        with open(arquivos, "wb") as f:
            f.write(pdf_response.content)

print("Download concluído!")