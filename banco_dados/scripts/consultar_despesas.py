import mysql.connector
import pandas as pd
from datetime import datetime, timedelta
from tqdm import tqdm

# Conecta ao banco de dados
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="SUA_SENHA",
    database="ans_teste"
)

# Define data de corte (ultimo trimestre e ultimo ano)
hoje = datetime.today()
ultimo_trimestre = hoje - timedelta(days=90)
um_ano_atras = hoje - timedelta(days=365)

# Filtro aproximado padronizado para a descrição
filtro_padrao = "SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA À SAÚDE MÉDICO HOSPITALAR"

# Monta as queries
query_trimestre = f"""
    SELECT o.razao_social, d.descricao, d.vl_saldo_final
    FROM demonstrativos d
    JOIN operadoras o ON d.reg_ans = o.registro_ans
    WHERE REPLACE(d.descricao, '  ', ' ') LIKE '%{filtro_padrao}%'
      AND d.data >= '{ultimo_trimestre.date()}'
    ORDER BY d.vl_saldo_final DESC
    LIMIT 10;
"""

query_ano = f"""
    SELECT o.razao_social, d.descricao, d.vl_saldo_final
    FROM demonstrativos d
    JOIN operadoras o ON d.reg_ans = o.registro_ans
    WHERE REPLACE(d.descricao, '  ', ' ') LIKE '%{filtro_padrao}%'
      AND d.data >= '{um_ano_atras.date()}'
    ORDER BY d.vl_saldo_final DESC
    LIMIT 10;
"""

# Executa e exibe resultados com pandas
cursor = conn.cursor()
print("\n🔍 Top 10 despesas - Último Trimestre:")
cursor.execute(query_trimestre)
dados_tri = list(tqdm(cursor.fetchall(), desc="Carregando dados do trimestre", ncols=80))
colunas_tri = [desc[0] for desc in cursor.description]
df_tri = pd.DataFrame(dados_tri, columns=colunas_tri)
df_tri.index = df_tri.index + 1
if df_tri.empty:
    print("⚠️ Nenhuma despesa encontrada para o último trimestre.")
else:
    df_tri["vl_saldo_final"] = df_tri["vl_saldo_final"].apply(lambda x: f"R$ {x:,.2f}".replace(",", "v").replace(".", ",").replace("v", "."))
    print(df_tri)

print("\n🔍 Top 10 despesas - Último Ano:")
cursor.execute(query_ano)
dados_ano = list(tqdm(cursor.fetchall(), desc="Carregando dados do ano", ncols=80))
colunas_ano = [desc[0] for desc in cursor.description]
df_ano = pd.DataFrame(dados_ano, columns=colunas_ano)
df_ano.index = df_ano.index + 1
if df_ano.empty:
    print("⚠️ Nenhuma despesa encontrada para o último ano.")
else:
    df_ano["vl_saldo_final"] = df_ano["vl_saldo_final"].apply(lambda x: f"R$ {x:,.2f}".replace(",", "v").replace(".", ",").replace("v", "."))
    print(df_ano)

cursor.close()
conn.close()
