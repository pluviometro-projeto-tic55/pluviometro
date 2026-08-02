# Checklist Pos-Restart

## Backend API
- [ ] Container API em execucao (`docker ps`)
- [ ] Container API saudavel (`healthy`)
- [ ] Healthcheck responde `{"status":"ok"}` em `/api/health`

## Frontend
- [ ] Frontend em execucao (`docker ps`)
- [ ] Home em `:3000` responde HTTP 200
- [ ] Dashboard carrega sem erro de runtime no navegador

## Dados
- [ ] Endpoint atual responde: `/api/stations/<id>/current`
- [ ] Endpoint externo responde: `/api/stations/<id>/external/current`
- [ ] Endpoint de previsao responde: `/api/stations/<id>/forecast`
- [ ] Status da estacao coerente com recencia de dados (`last_update`)

## Resiliencia
- [ ] Politica de restart da API: `always`
- [ ] Sem conflito de pastas duplicadas de deploy
- [ ] Sem artefatos locais indevidos versionados no commit
