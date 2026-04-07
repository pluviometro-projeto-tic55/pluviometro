<h1 align="center">
   Backend-api
</h1>

API para calcular as variáveis climáticas e para a transferência de dados do banco ao painel de monitoramento.

---

## 🚀 Como executar o projeto


1. Certifique-se de ter o Python e o [Banco de Dados](https://github.com/weather-station-project-tic55/database-scripts) configurado.


2. Clone este repositório em sua máquina local usando o seguinte comando no terminal: `git clone https://github.com/weather-station-project-tic55/backend-api.git`

3. Acesse o diretório do projeto: `cd backend-api`

4. Configure as variáveis de ambiente: 
- .env contendo URL do banco: `DATABASE_URI=mysql+pymysql://DB_USER:DB_PASSWORD@DB_HOST:DB_PORT/DB_NAME`
- .env contendo string da API externa: `API_KEY = ec27234aed1747ea95234412252511'`

5. Instale as dependências: `pip install -r requirements.txt`

6. Inicie a aplicação: `python main.py`








