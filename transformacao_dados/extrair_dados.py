import pdfplumber
import pandas as pd
from pathlib import Path
import zipfile
import shutil
from tqdm import tqdm
import time
import gc

print("Iniciando o processo de extração...")

base_dir = Path(__file__).resolve().parent
zip_original = base_dir.parent / "web_scraping" / "arquivos" / "Anexos_ANS.zip"
output_dir = base_dir / "output"
temp_dir = output_dir / "temp_zip"
zip_path = output_dir / "Teste_Ithalo.zip"
pdf_path = temp_dir / "Anexo I.pdf"

output_dir.mkdir(parents=True, exist_ok=True)

if temp_dir.exists():
    try:
        shutil.rmtree(temp_dir)
    except Exception:
        time.sleep(1)
        shutil.rmtree(temp_dir, ignore_errors=True)
temp_dir.mkdir(parents=True, exist_ok=True)

if not zip_original.exists():
    print("ERRO: Arquivo 'Anexos_ANS.zip' não encontrado na pasta 'arquivos'")
    exit()

print("Extraindo 'Anexo I.pdf' do ZIP...")
try:
    with zipfile.ZipFile(zip_original, "r") as zipf:
        zipf.extract("Anexo I.pdf", path=temp_dir)
except KeyError:
    print("ERRO: 'Anexo I.pdf' não encontrado dentro do ZIP")
    exit()

print("Extraindo dados do PDF...")
dados = []
with pdfplumber.open(pdf_path) as pdf:
    for pagina in tqdm(pdf.pages, desc="Processando páginas", unit="página", ncols=80):
        tabela = pagina.extract_table()
        if tabela:
            dados.extend(tabela)

gc.collect()

print("Processando os dados...")
cabecalho = dados[0]
linhas = [linha for linha in dados[1:] if linha[0] != cabecalho[0]]
df = pd.DataFrame(linhas, columns=cabecalho)
df.replace({"OD": "Odontológico", "AMB": "Ambulatorial"}, inplace=True)

print("Criando arquivo ZIP com CSV...")
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
    csv_bytes = df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
    with tqdm(total=len(csv_bytes), unit="B", unit_scale=True, ncols=80, desc="Criando ZIP") as bar:
        zipf.writestr("dados.csv", csv_bytes)
        bar.update(len(csv_bytes))

for tentativa in range(5):
    try:
        shutil.rmtree(temp_dir)
        break
    except Exception:
        time.sleep(1)
        gc.collect()

print("\nConcluído com sucesso!")
print(f"Arquivo criado: {zip_path.name}")