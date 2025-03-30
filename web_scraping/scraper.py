import requests
from bs4 import BeautifulSoup
from pathlib import Path
import zipfile
from tqdm import tqdm
import shutil
import time

url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"


base_dir = Path(__file__).resolve().parent
pasta = base_dir / "arquivos" / "temp_download"
pasta_zip = base_dir / "arquivos"
zip_nome = pasta_zip / "Anexos_ANS.zip"


pasta_zip.mkdir(parents=True, exist_ok=True)
pasta.mkdir(parents=True, exist_ok=True)

print("Iniciando busca pelos anexos...")


pagina = requests.get(url)
soup = BeautifulSoup(pagina.text, "html.parser")


anexos = {
    "Anexo I": {"encontrado": False, "nome": "Anexo I.pdf", "url": None},
    "Anexo II": {"encontrado": False, "nome": "Anexo II.pdf", "url": None}
}


for link in soup.find_all("a"):
    href = link.get("href")
    if href and href.endswith(".pdf"):
        texto_link = link.text.strip()
        for anexo in anexos:
            if anexo in texto_link:
                anexos[anexo]["encontrado"] = True
                anexos[anexo]["url"] = href
                print(f"{anexo} encontrado")


if not all(anexo["encontrado"] for anexo in anexos.values()):
    print("Erro: Nem todos os anexos foram encontrados na página.")
    print("Execução interrompida.")
    exit()

print("Iniciando downloads e compactação direta para o ZIP...")


with zipfile.ZipFile(zip_nome, "w", zipfile.ZIP_DEFLATED) as zipf:
    for anexo in anexos.values():
        caminho_temp = pasta / anexo["nome"]
        resposta = requests.get(anexo["url"], stream=True)
        total = int(resposta.headers.get('content-length', 0))

        if resposta.status_code == 200:
            with open(caminho_temp, "wb") as f, tqdm(
                desc=f"Baixando {anexo['nome']}",
                total=total,
                unit='B',
                unit_scale=True,
                ncols=80
            ) as bar:
                for chunk in resposta.iter_content(chunk_size=1024):
                    f.write(chunk)
                    bar.update(len(chunk))

            zipf.write(caminho_temp, anexo["nome"])
            caminho_temp.unlink()  # Remove o arquivo baixado
            print(f"{anexo['nome']} adicionado ao ZIP")
        else:
            print(f"Falha ao baixar {anexo['nome']} (Status: {resposta.status_code})")
            exit()


for tentativa in range(3):
    try:
        shutil.rmtree(pasta)
        break
    except PermissionError:
        print("Tentando remover a pasta temporária novamente...")
        time.sleep(1)

print("Processo concluído com sucesso.")
