import pdfplumber
import pandas as pd
import os
import zipfile

print("Iniciando o processo de extração...")

base_dir = os.path.dirname(os.getcwd())
pdf_path = os.path.join(base_dir, "web_scraping", "arquivos", "Anexo I.pdf")
output_dir = os.path.join(base_dir, "transformacao_dados", "output")

os.makedirs(output_dir, exist_ok=True)

if not os.path.exists(pdf_path):
    print("ERRO: Arquivo 'Anexo I.pdf' não encontrado na pasta 'arquivos'")
    print("Certifique-se que:")
    print("- O arquivo foi baixado")
    print("- Está na pasta 'arquivos'")
    exit()

print("Extraindo dados do PDF...")

dados = []
with pdfplumber.open(pdf_path) as pdf:
    for pagina in pdf.pages:
        tabela = pagina.extract_table()
        if tabela:
            dados.extend(tabela)

print("Processando os dados...")

cabecalho = dados[0]
linhas = dados[1:]

linhas = [linha for linha in linhas if linha[0] != cabecalho[0]]

df = pd.DataFrame(linhas, columns=cabecalho)

df.replace({
    "OD": "Odontológico",
    "AMB": "Ambulatorial"
}, inplace=True)

csv_path = os.path.join(output_dir, "dados.csv")
zip_path = os.path.join(output_dir, "Teste_Ithalo.zip")

print("Salvando CSV...")
df.to_csv(csv_path, index=False, encoding="utf-8-sig")

print("Criando arquivo ZIP...")

with zipfile.ZipFile(zip_path, "w") as zipf:
    zipf.write(csv_path, os.path.basename(csv_path))

print("\nConcluído com sucesso!")
print(f"Arquivos criados em: {output_dir}")
print(f"- {csv_path}")
print(f"- {zip_path}")