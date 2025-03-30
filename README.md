# 📊 Dataflow Project - ANS

Projeto de coleta, extração e análise de dados públicos da ANS (Agência Nacional de Saúde Suplementar), utilizando Python, MySQL, web scraping e tratamento de dados em PDF e CSV.

## 📁 Estrutura do Projeto

```
dataflow-project/
│
├── banco_dados/
│   ├── dados/                  # Arquivos CSV por trimestre e ano
│   │   ├── 2023/
│   │   └── 2024/
│   └── scripts/
│       ├── create_tables.sql      # Criação das tabelas no MySQL
│       ├── import_data.sql        # Importação via LOAD DATA
│       ├── importar_operadoras.py # Importa dados de operadoras (CSV)
│       └── importar_demonstrativos.py # Importa demonstrativos trimestrais
│
├── transformacao_dados/
│   ├── output/                # Gera o CSV final e compacta
│   │   └── Teste_Ithalo.zip  # Contém o dados extraídos do Anexo I.pdf
│   └── extrair_dados.py      # Extrai dados tabulares do PDF (Anexo I)
│
├── web_scraping/
│   ├── arquivos/              # Armazena os anexos baixados
│   └── scraper.py            # Faz scraping da página da ANS e gera o ZIP
│
└── README.md
```

---

## 🔧 Scripts e Funcionalidades

### 🐍 `scraper.py`
- Realiza scraping da página da ANS.
- Identifica e baixa os anexos I e II em PDF.
- Compacta diretamente em `Anexos_ANS.zip` na pasta `web_scraping/arquivos`.

### 🧠 `extrair_dados.py`
- Extrai a tabela do PDF "Anexo I" dentro do ZIP.
- Transforma os dados em `DataFrame`.
- Salva como CSV dentro de um ZIP final: `Teste_Ithalo.zip`.
- Mostra barra de progresso com `tqdm`.

### 🗃️ `importar_operadoras.py`
- Lê dados CSV das operadoras.
- Faz inserção no banco de dados MySQL (`ans_teste.operadoras`).
- Usa `pathlib` para manter caminhos seguros.

### 📈 `importar_demonstrativos.py`
- Varre todas as pastas 2023/2024 buscando arquivos `.csv`.
- Importa os dados financeiros para a tabela `demonstrativos`.
- Faz parse de números com vírgula e ignora erros por inconsistência.

---

## 🐘 Banco de Dados MySQL

Scripts `.sql` para:
- Criar tabelas (`create_tables.sql`)
- Importar CSVs com `LOAD DATA LOCAL INFILE` (`import_data.sql`)

Banco: `ans_teste`

---

## 💡 Observações
- O projeto usa `tqdm` para barras de progresso.
- Todos os caminhos são relativos e seguros com `pathlib`.

---

## 🚀 Como Executar

1. Clone o projeto:
```bash
git clone https://github.com/seu-usuario/dataflow-project.git
```
2. Instale os pacotes necessários:
```bash
pip install -r requirements.txt
```
3. Execute os scripts desejados:
```bash
python web_scraping/scraper.py
python transformacao_dados/extrair_dados.py
python banco_dados/scripts/importar_operadoras.py
python banco_dados/scripts/importar_demonstrativos.py
```

---

## ✨ Contribuição
Sinta-se livre para abrir issues ou dar sugestões. Este projeto foi feito com foco em aprendizado e boas práticas de organização.

---

Autor: Ithalo Teodósio Nascimento
