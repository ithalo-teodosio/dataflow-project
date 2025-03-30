from pathlib import Path
import pandas as pd
import mysql.connector

caminho_csv = Path("C:/Users/ithal/OneDrive/Área de Trabalho/Ithalo/Projetos pessoais/dados abertos/operadoras/Relatorio_cadop.csv")

df = pd.read_csv(caminho_csv, encoding="utf-8", sep=";")

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="himegami110395",
    database="ans_teste"
)

cursor = conn.cursor()

for _, row in df.iterrows():
    query = """
        INSERT INTO operadoras (
            registro_ans, cnpj, razao_social, nome_fantasia, modalidade, logradouro,
            numero, complemento, bairro, cidade, uf, cep, ddd, telefone, fax,
            email, representante, cargo_representante, regiao_comercializacao, data_registro_ans
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    valores = tuple(row.fillna("").values)
    cursor.execute(query, valores)

conn.commit()
cursor.close()
conn.close()

print("Dados importados com sucesso!")
