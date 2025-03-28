import requests
from bs4 import BeautifulSoup
import os
import zipfile

# Configurações
url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
pasta = "arquivos"
zip_nome = "Anexos_ANS.zip"

# Limpa a pasta se já existir
if os.path.exists(pasta):
    for arquivo in os.listdir(pasta):
        os.remove(os.path.join(pasta, arquivo))
else:
    os.makedirs(pasta)

print("Iniciando busca pelos anexos...")

# Baixa a página
pagina = requests.get(url)
soup = BeautifulSoup(pagina.text, "html.parser")

# Dicionário para controlar os anexos
anexos = {
    "Anexo I": {"encontrado": False, "nome": "Anexo I.pdf", "url": None},
    "Anexo II": {"encontrado": False, "nome": "Anexo II.pdf", "url": None}
}

# Procura pelos links dos anexos
for link in soup.find_all("a"):
    href = link.get("href")
    if href and href.endswith(".pdf"):
        texto_link = link.text.strip()
        for anexo in anexos:
            if anexo in texto_link:
                anexos[anexo]["encontrado"] = True
                anexos[anexo]["url"] = href
                print(f"{anexo} encontrado")

# Verifica se ambos foram encontrados
if not all(anexo["encontrado"] for anexo in anexos.values()):
    print("\nErro: Ambos os anexos não foram encontrados na página")
    print("A execução foi interrompida")
    exit()

print("\nIniciando downloads...")

# Baixa os arquivos
for anexo in anexos.values():
    caminho = os.path.join(pasta, anexo["nome"])
    resposta = requests.get(anexo["url"])
    if resposta.status_code == 200:
        with open(caminho, "wb") as f:
            f.write(resposta.content)
        print(f"{anexo["nome"]} baixado com sucesso")
    else:
        print(f"Falha ao baixar {anexo["nome"]} (Status: {resposta.status_code})")
        exit()

# Cria o ZIP
caminho_zip = os.path.join(pasta, zip_nome)
with zipfile.ZipFile(caminho_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
    for anexo in anexos.values():
        arquivo = os.path.join(pasta, anexo["nome"])
        zipf.write(arquivo, anexo["nome"])
print(f"\nZIP criado com sucesso: {zip_nome}")

print("\nConcluído com sucesso!")