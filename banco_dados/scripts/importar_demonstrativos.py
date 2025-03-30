from pathlib import Path
import pandas as pd
import mysql.connector
from tqdm import tqdm

diretorio_base = Path("C:/Users/ithal/OneDrive/Área de Trabalho/Ithalo/Projetos pessoais/dataflow-project/banco_dados/dados")

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="himegami110395",
    database="ans_teste"
)

cursor = conn.cursor()

for arquivo_csv in diretorio_base.rglob("*.csv"):
    print(f"\nImportando arquivo: {arquivo_csv.name}")
    try:
        df = pd.read_csv(arquivo_csv, encoding="utf-8", sep=";")
        for _, row in tqdm(df.iterrows(), total=len(df), desc=f"Inserindo {arquivo_csv.name}"):
            query = """
                INSERT INTO demonstrativos (
                    data, reg_ans, cd_conta_contabil, descricao,
                    vl_saldo_inicial, vl_saldo_final
                ) VALUES (%s, %s, %s, %s, %s, %s)
            """
            valores = (
                row["DATA"],
                str(row["REG_ANS"]),
                str(row["CD_CONTA_CONTABIL"]),
                row["DESCRICAO"],
                float(str(row["VL_SALDO_INICIAL"]).replace(",", ".")),
                float(str(row["VL_SALDO_FINAL"]).replace(",", "."))
            )
            cursor.execute(query, valores)
        conn.commit()
        print(f"\n{arquivo_csv.name} importado com sucesso!")
    except Exception as e:
        print(f"Erro ao importar {arquivo_csv.name}: {e}")

cursor.close()
conn.close()

print("\nTodos os demonstrativos foram importados com sucesso!")
