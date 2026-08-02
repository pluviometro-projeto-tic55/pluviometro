# Relatorio Completo de Reparos e Melhorias

Data de emissao: 2026-08-02
Projeto: pluviometro
Periodo analisado: ultimos 3 meses (inclui recorte de 2 meses)

## 1) Base de versao (Git)

- Branch atual: main
- Commit HEAD: 29a79920442bcb530155bda68c5ed445b45b43af
- Versao curta: 29a79920
- Remote:
  - origin https://github.com/pluviometro-projeto-tic55/pluviometro.git (fetch)
  - origin https://github.com/pluviometro-projeto-tic55/pluviometro.git (push)

## 2) Historico recebido pelo Git

### 2.1 Ultimos 3 meses
Total de commits no periodo: 30

| Hash | Data (ISO) | Autor | Mensagem |
|---|---|---|---|
| 29a79920 | 2026-07-06 18:05:30 -0300 | Jessica Van Klaveren | Add local VAR calibration scripts |
| d281924d | 2026-07-06 17:42:08 -0300 | unknown | Implementacao do Buffer com SQLite |
| 5b33391f | 2026-06-15 21:23:30 -0300 | Jessica Van Klaveren | Fix sensor humidity filtering, forecast date range, and feelsLike typo |
| 7a336114 | 2026-06-01 19:53:05 -0300 | unknown | Conserta update dos cards de revisao |
| 691de0f8 | 2026-06-01 19:26:09 -0300 | Jessica Van Klaveren | Atualizacoes de Front 1 |
| a977b94e | 2026-05-25 21:22:08 -0300 | Joao Andrey | fix(ui): remove 'Sensacao termica' dos cards de previsao |
| d2260983 | 2026-05-25 12:08:54 -0300 | annabeatriceneumann | Refactor sensor initialization and data handling |
| aa790dca | 2026-05-25 12:04:08 -0300 | annabeatriceneumann | Refactor sensor script for improved readability |
| b3073344 | 2026-05-25 11:52:44 -0300 | annabeatriceneumann | Refactor scheduler job definitions for clarity |
| bad79a63 | 2026-05-25 11:42:52 -0300 | annabeatriceneumann | Fix indentation in forecast_services.py |
| c8943054 | 2026-05-25 11:41:54 -0300 | annabeatriceneumann | Fix timezone handling for timestamp in forecast services |
| 1a68aa49 | 2026-05-25 10:07:00 -0300 | annabeatriceneumann | Fix formatting of response_details dictionary |
| 22ae2c16 | 2026-05-25 10:05:50 -0300 | annabeatriceneumann | Fix calculation of last update minutes in forecast_services |
| c57ddd94 | 2026-05-25 08:55:23 -0300 | annabeatriceneumann | Refactor response_details dictionary formatting |
| 99025084 | 2026-05-25 08:53:42 -0300 | annabeatriceneumann | Fix indentation in forecast_services.py |
| e2b22657 | 2026-05-25 08:46:56 -0300 | annabeatriceneumann | Refactor last_update_minutes calculation for readability |
| b313cf42 | 2026-05-25 08:45:49 -0300 | annabeatriceneumann | Refactor forecast_services.py to simplify response |
| db4bffc8 | 2026-05-25 08:44:14 -0300 | annabeatriceneumann | Enhance forecast response with weather details |
| 329e2897 | 2026-05-25 08:40:24 -0300 | annabeatriceneumann | Fix response_details structure in forecast_services.py |
| b4e2e404 | 2026-05-25 08:06:25 -0300 | annabeatriceneumann | Simplify online status check logic |
| ea2026f9 | 2026-05-25 08:01:41 -0300 | annabeatriceneumann | Refactor online status check for better clarity |
| 0f4a36c0 | 2026-05-25 07:58:26 -0300 | annabeatriceneumann | Refactor last_update calculation in forecast_services |
| 50ba5d11 | 2026-05-24 21:46:39 -0300 | annabeatriceneumann | Refactor useExternalCurrentData hook dependencies |
| acc1e3b1 | 2026-05-24 21:26:22 -0300 | annabeatriceneumann | Log last update time in DailySummary component |
| aebd3586 | 2026-05-24 21:09:45 -0300 | annabeatriceneumann | Refactor useExternalCurrentData hook for data fetching |
| 1444a54e | 2026-05-24 19:42:54 -0300 | annabeatriceneumann | Log broadcasted weather data in scheduler |
| 92d9fd68 | 2026-05-24 19:38:27 -0300 | annabeatriceneumann | Update timestamp handling to include timezone |
| 42829c03 | 2026-05-24 19:14:40 -0300 | annabeatriceneumann | Fix last_update calculation to use UTC timezone |
| 72498547 | 2026-05-18 19:33:23 -0300 | pluviometro-projeto-tic55 | Update README.md |
| 060fd74c | 2026-05-18 16:27:41 -0300 | Alessandro | Add note about repository inactivity since April 2026 |

Autores por volume (3 meses):
- 22 annabeatriceneumann
- 3 Jessica Van Klaveren
- 2 unknown
- 1 Alessandro
- 1 Joao Andrey
- 1 pluviometro-projeto-tic55

### 2.2 Ultimos 2 meses
Total de commits no periodo: 3

| Hash | Data (ISO) | Autor | Mensagem |
|---|---|---|---|
| 29a79920 | 2026-07-06 18:05:30 -0300 | Jessica Van Klaveren | Add local VAR calibration scripts |
| d281924d | 2026-07-06 17:42:08 -0300 | unknown | Implementacao do Buffer com SQLite |
| 5b33391f | 2026-06-15 21:23:30 -0300 | Jessica Van Klaveren | Fix sensor humidity filtering, forecast date range, and feelsLike typo |

Autores por volume (2 meses):
- 2 Jessica Van Klaveren
- 1 unknown

## 3) Reparos e melhorias executados na intervencao atual

### 3.1 Backend/API
- Previsao com menor risco de travamento:
  - Rota de forecast prioriza cache e usa geracao on-demand quando necessario.
- Enriquecimento de dados externos expostos para o frontend:
  - luminosidade externa (proxy UV), UV, is_day, condition, rain_mm, sunrise/sunset e last_updated_epoch.
- Correcoes de robustez:
  - ajuste de unpack de tupla para evitar erro de runtime por mudanca no contrato da API externa.
- Resiliencia de leitura atual da estacao:
  - fallback para media de janela recente (rolling average) quando campos estiverem ausentes.
  - flags no payload para indicar estimativa e fonte da estimativa.
- Healthcheck da API:
  - endpoint /api/health operacional.

Arquivos relevantes modificados:
- backend-api/src/services/forecast_services.py
- backend-api/src/services/external_weather_service.py
- backend-api/src/routes/external_routes.py
- backend-api/src/routes/forecast_routes.py
- backend-api/src/__init__.py
- backend-api/docker-compose.yaml

### 3.2 Frontend
- Ajustes de semantica e apresentacao de chuva para mm acumulado.
- Limpeza de comparacao para manter apenas dados realmente comparaveis.
- Ajustes de status e recencia de dados externos.
- Polling periodico ajustado para reduzir estagnação visual e de dados.
- Melhorias de nomenclatura e legibilidade (Iluminancia, Lux, etc.).

Arquivos relevantes modificados:
- web-frontend/emj-react/src/components/DailySummary/index.jsx
- web-frontend/emj-react/src/components/DailySummary/comparisionModal.jsx
- web-frontend/emj-react/src/components/ForecastCards/index.jsx
- web-frontend/emj-react/src/components/WeatherCard/index.jsx
- web-frontend/emj-react/src/components/WeatherDetails/index.jsx
- web-frontend/emj-react/src/hooks/useDetailsData/index.js
- web-frontend/emj-react/src/hooks/useExternalCurrentData/useExternalCurrentData.js
- web-frontend/emj-react/src/hooks/useForecastData/index.js
- web-frontend/emj-react/src/utils/transformWeather/index.js
- web-frontend/emj-react/src/utils/transformWeather/transformWeather.test.js

Observacao: houve revert pontual de alteracao no arquivo de resumo diario para ajuste fino posterior.

### 3.3 Deploy, recuperacao e operacao
- Backup criado antes de deploy.
- Rebuild e restart da API e frontend via Docker Compose no servidor.
- Validacao de endpoints publicos (frontend e API) apos deploy.
- Limpeza de diretorios duplicados no servidor para reduzir risco de conflito operacional.

## 4) Validacao de resiliencia em producao

Evidencias operacionais confirmadas em servidor:
- Politica de restart do container da API: {"Name":"always","MaximumRetryCount":0}
- Estado atual: API em healthy e frontend em execucao.
- Health endpoint: /api/health retorna {"status":"ok"}.

Conclusao operacional:
- Queda de processo da API: auto-recuperacao configurada.
- Falta parcial de dado: backend responde com fallback/estimativa em vez de falhar endpoint.
- Queda de energia/host: retorno automatico depende do daemon Docker iniciar no boot do host (premissa padrao em Ubuntu com Docker habilitado).

## 5) Estado atual do working tree (arquivos relevantes)

Itens relevantes em alteracao local no momento da emissao:
- backend-api/docker-compose.yaml
- backend-api/src/__init__.py
- backend-api/src/routes/external_routes.py
- backend-api/src/routes/forecast_routes.py
- backend-api/src/services/external_weather_service.py
- backend-api/src/services/forecast_services.py
- web-frontend/emj-react/src/components/DailySummary/comparisionModal.jsx
- web-frontend/emj-react/src/components/DailySummary/index.jsx
- web-frontend/emj-react/src/components/ForecastCards/index.jsx
- web-frontend/emj-react/src/components/WeatherCard/index.jsx
- web-frontend/emj-react/src/components/WeatherDetails/index.jsx
- web-frontend/emj-react/src/hooks/useDetailsData/index.js
- web-frontend/emj-react/src/hooks/useExternalCurrentData/useExternalCurrentData.js
- web-frontend/emj-react/src/hooks/useForecastData/index.js
- web-frontend/emj-react/src/utils/transformWeather/index.js
- web-frontend/emj-react/src/utils/transformWeather/transformWeather.test.js

Nota: existem tambem alteracoes em artefatos gerados (__pycache__, cache/modelos) que nao representam regra de negocio.

## 6) Recomendacao final de governanca

- Congelar um baseline com commit e tag apos validacao funcional final.
- Versionar separadamente ajustes de resiliencia (backend) e UX (frontend).
- Excluir artefatos gerados do versionamento quando aplicavel (cache/modelos/pycache), para reduzir ruido de diff.
- Criar checklist de pos-restart (health API, fetch frontend, forecast endpoint, status da estacao).

## 7) Anexos (fontes)

Arquivos de evidencias gerados:
- reports/git_head.txt
- reports/git_branch.txt
- reports/git_remotes.txt
- reports/git_version.txt
- reports/git_log_3m.txt
- reports/git_log_2m.txt
- reports/git_authors_3m.txt
- reports/git_authors_2m.txt
- reports/git_status_relevant.txt
