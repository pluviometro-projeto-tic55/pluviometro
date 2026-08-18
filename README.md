# Estação Meteorológica de Baixo Custo

Projeto de estação meteorológica de baixo custo para coleta, armazenamento, processamento e visualização de dados ambientais por meio de Raspberry Pi, sensores físicos, banco de dados e interface web.

A solução foi construída de forma evolutiva. A primeira etapa implementou a estação meteorológica base; a etapa atual acrescenta a medição física de precipitação por meio de um pluviômetro basculante e melhorias de confiabilidade no sistema de coleta.

## Contexto do projeto

O projeto é desenvolvido em etapas independentes e complementares:

1. **Estação meteorológica base:** implementação da coleta de temperatura, umidade, pressão atmosférica e luminosidade, persistência em banco de dados e visualização web.
2. **Integração do pluviômetro:** inclusão de medição física de precipitação, tratamento dos pulsos no Raspberry Pi, armazenamento dos dados de chuva e mecanismos de tolerância a falhas.
3. **Integração de anemômetro:** etapa posterior, iniciada por outra equipe, destinada à medição local do vento.

O Colégio João XXIII disponibilizou o ambiente para testes e instalação de uma das estações e prestou apoio por meio de sua equipe de manutenção.

## Objetivo

Disponibilizar uma estação meteorológica de baixo custo, modular e expansível, capaz de:

- coletar dados ambientais localmente;
- armazenar e disponibilizar medições para consulta;
- apresentar informações meteorológicas por interface web;
- permitir comparação entre dados locais e fontes externas;
- receber novos sensores sem necessidade de reconstrução completa do sistema;
- reduzir a perda de dados durante falhas de rede ou indisponibilidade do banco principal.

## Funcionalidades atuais

- Coleta de temperatura;
- Coleta de umidade relativa do ar;
- Coleta de pressão atmosférica;
- Coleta de luminosidade;
- Medição física de precipitação por pluviômetro basculante;
- Conversão das basculadas em milímetros de chuva;
- Registro das medições em banco de dados;
- Buffer local em SQLite;
- Sincronização posterior com MariaDB;
- Previsão meteorológica de curto prazo;
- Previsão semanal;
- Histórico de medições;
- Filtros por variável meteorológica;
- Comparação com dados de API externa;
- Exportação de dados em CSV;
- Interface simplificada e interface completa.

## Arquitetura

Fluxo geral da estação:

```text
BME280 ---------\
                 \
BH1750 -----------+--> Raspberry Pi --> processamento Python --> SQLite --> MariaDB --> FastAPI --> React --> usuário
                 /
Pluviômetro -----/
```

O SQLite atua como camada local de preservação dos registros. No coletor atual, os dados são gravados localmente e, havendo conectividade, são sincronizados com o MariaDB. O registro local só deve ser removido após a confirmação do envio ao banco principal.

### Tecnologias principais

#### Hardware

- Raspberry Pi 4;
- BME280 — temperatura, umidade e pressão atmosférica;
- BH1750 — luminosidade;
- pluviômetro de báscula com reed switch;
- cabos, bornes e conexões auxiliares.

#### Software

- Python;
- FastAPI;
- React;
- MariaDB/MySQL;
- SQLite;
- `systemd` para execução automática do coletor;
- Raspberry Pi OS.

## Sensores herdados: BME280 e BH1750

Os sensores BME280 e BH1750 utilizam comunicação **I2C**, compartilhando as linhas SDA e SCL e utilizando endereços diferentes no barramento.

Pinagem documentada para a estação herdada:

| Função | Pino físico do Raspberry Pi |
|---|---:|
| 3,3 V | 1 |
| SDA | 3 |
| SCL | 5 |
| GND | 9 |

Os materiais herdados utilizam cabos CAT5e e bornes para permitir o posicionamento remoto dos sensores. O BME280 possui uma cápsula física própria para proteção e exposição adequada ao ambiente.

Para conferir se os dispositivos I2C estão sendo identificados pelo Raspberry Pi:

```bash
sudo i2cdetect -y 1
```

Na configuração documentada, normalmente devem aparecer os endereços do BME280 e do BH1750, por exemplo `76` e `23`.

## Integração do pluviômetro

A principal expansão desta etapa é a integração de um **pluviômetro basculante**.

Cada basculada movimenta um ímã que aciona um reed switch. O Raspberry Pi detecta essa transição pelo GPIO, incrementa um contador e converte a quantidade de pulsos em milímetros de precipitação.

### Ligação utilizada

| Cabo do pluviômetro | Raspberry Pi 4 | Função |
|---|---|---|
| Vermelho | Pino físico 11 — GPIO17 | Entrada do pulso |
| Verde | Pino físico 14 — GND | Terra |

O pluviômetro não utiliza o barramento I2C dos sensores herdados. Sua leitura ocorre por entrada digital GPIO.

Consulte também [README_PLUVIOMETRO.md](README_PLUVIOMETRO.md) para a documentação específica do subsistema de chuva.

## Coleta e agregação dos dados

O coletor atual realiza leituras periódicas dos sensores e mantém buffers temporários para calcular médias antes da persistência.

A gravação é realizada em ciclos de aproximadamente **5 minutos**. Para a chuva, os pulsos detectados nesse período são acumulados e convertidos para milímetros antes do salvamento.

O arquivo SQLite utilizado pelo coletor atual é:

```text
~/.config/station/buffer_sensores.db
```

A tabela local utilizada é `buffer_raspdata`.

O identificador da estação (`rcID`) é lido de:

```text
~/.config/station/rcid.txt
```

## Configuração do coletor

O `sensorscript.py` atual utiliza as seguintes variáveis de ambiente:

```text
DB_HOST
DB_PORT
DB_USER
DB_PASS
DB_NAME
RAIN_GPIO_PIN
RAIN_MM_PER_PULSE
```

Para a instalação do pluviômetro descrita neste projeto:

```text
RAIN_GPIO_PIN=17
```

### Atenção à calibração

Os materiais de calibração do projeto registram aproximadamente **0,29205 mm por basculada** para a geometria utilizada. O código atual possui `0.297` como valor de fallback quando `RAIN_MM_PER_PULSE` não é configurado.

Antes de colocar a estação em operação definitiva, defina explicitamente `RAIN_MM_PER_PULSE` com o valor de calibração adotado pela equipe e mantenha o mesmo valor na documentação e no código.

## Instalação do software no Raspberry Pi

Os documentos mais recentes do sistema herdado descrevem um instalador automatizado. A versão documentada utiliza os seguintes arquivos na mesma pasta:

```text
installstation_v6.sh
sensorscript.py
sensorcollect.service
```

> **Nota de compatibilidade:** materiais anteriores utilizam nomes como `installstation_v01.sh`, `installstation_v03.sh`, `sensor_v01.py` e `raspcollect.service`. Utilize sempre os nomes presentes na versão atual do repositório.

### Procedimento geral

1. Copie os arquivos para o Raspberry Pi;
2. Entre na pasta pelo terminal;
3. conceda permissão de execução ao instalador;
4. execute o instalador;
5. escolha a opção de instalação;
6. informe a conexão com MariaDB/MySQL;
7. informe os metadados da estação;
8. confirme a criação/recuperação do `rcID`;
9. verifique se o serviço de coleta foi ativado.

Exemplo:

```bash
chmod +x installstation_v6.sh
sudo ./installstation_v6.sh
```

O instalador herdado solicita informações como:

- IP/host do banco;
- usuário;
- senha;
- nome do banco;
- nome da estação;
- latitude e longitude;
- altitude;
- local/endereço;
- e-mail do responsável;
- contato.

### Compatibilidade com o coletor atual

Versões antigas do instalador foram documentadas como responsáveis por inserir as credenciais diretamente no script Python. O `sensorscript.py` atual, entretanto, lê as configurações do banco por **variáveis de ambiente**.

Portanto, ao reutilizar o instalador herdado, confira se a versão atual foi adaptada para fornecer `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASS` e `DB_NAME` ao serviço. Caso contrário, o instalador e o serviço precisam ser ajustados antes da implantação.

O mesmo vale para `RAIN_GPIO_PIN` e `RAIN_MM_PER_PULSE` quando o pluviômetro estiver instalado.

## Serviço de coleta

A estação utiliza um serviço `systemd` para manter o coletor em execução em segundo plano e iniciar a coleta automaticamente no boot.

A configuração herdada inclui comportamento equivalente a:

```ini
Restart=always
RestartSec=5
```

Assim, se o script for encerrado inesperadamente, o `systemd` tenta iniciá-lo novamente após alguns segundos.

Como o nome da unidade varia entre versões dos documentos, primeiro confirme o nome do arquivo presente no repositório. Exemplos encontrados na documentação:

```text
sensorcollect.service
raspcollect.service
```

Para verificar o serviço:

```bash
sudo systemctl status NOME_DO_SERVICO.service
```

Para acompanhar os logs:

```bash
journalctl -u NOME_DO_SERVICO.service -f
```

## Banco de dados

O sistema utiliza MariaDB/MySQL como banco principal. A estrutura herdada contém, entre outras, as tabelas `raspclient` e `raspdata`.

Nesta etapa do projeto não foi realizada uma remodelagem geral do banco; a integração do pluviômetro utiliza o fluxo de persistência já existente na estação.

O SQLite local não substitui o MariaDB. Ele funciona como buffer para preservar medições até que a sincronização com o banco principal possa ser concluída.

## Instalação física

A parte física da estação deve ser adaptada ao local de implantação.

A estrutura utilizada no Colégio João XXIII — incluindo tubos, suportes metálicos, tampa de PVC e tubulação de escoamento — é **uma solução específica daquele ambiente** e não é um requisito obrigatório para outras instalações.

Os requisitos gerais permanecem:

- instalar o pluviômetro em local aberto;
- minimizar interferência de árvores, prédios e outras estruturas;
- manter a boca do coletor em altura adequada;
- manter o pluviômetro perfeitamente nivelado;
- preservar a geometria da área de captação utilizada na calibração;
- garantir que a água possa escoar sem permanecer acumulada no mecanismo;
- proteger cabos e conexões contra intempéries e esforços mecânicos.

### Implementação no Colégio João XXIII

Na instalação de referência, o pluviômetro automático foi fixado em uma tampa de PVC conectada a tubos que conduzem a água para baixo. Os cabos do medidor foram prolongados até o interior do prédio, onde se encontra o Raspberry Pi.

A instalação física no telhado foi realizada pela equipe de manutenção do colégio.

![Instalação do pluviômetro no telhado](docs/images/instalacao-telhado-joao-xxiii.jpeg)

## Validação manual e uso didático

Além do pluviômetro automático, o projeto utiliza um **pluviômetro manual Incoterm** como referência visual.

A proposta é permitir a comparação entre a leitura manual e a medição automática, inclusive em atividades didáticas com os alunos.

![Pluviômetro manual de referência](docs/images/pluviometro-manual-incoterm.jpeg)

## Projeto de baixo custo

Um requisito importante do projeto é manter a estação acessível e expansível, utilizando componentes de custo reduzido e que possam ser substituídos ou adaptados sem exigir equipamentos meteorológicos de alto custo.

A estrutura de instalação pode variar de acordo com o local. O custo da solução específica do Colégio João XXIII não deve ser interpretado como custo mínimo obrigatório para replicação do pluviômetro.

## Documentação herdada

Os seguintes materiais descrevem partes importantes da primeira etapa da estação e devem ser mantidos como documentação complementar:

- `Manual de instalação do sistema de coleta na Raspberry.docx` — instalação do coletor e cadastro da estação;
- `Manual de montagem da cápsula.docx` — construção da proteção do BME280 e montagem física dos sensores herdados;
- `Manual e esquema eletrônico.docx` — barramento I2C, pinagem e ligações do BME280/BH1750;
- `README_installstation.txt` — funcionamento do instalador;
- `README_sensorcollectservice.txt` — funcionamento do serviço `systemd`.

## Equipe

Projeto desenvolvido no âmbito da Residência em TIC 55 — BRISA / UNISINOS.

### Equipe da etapa do pluviômetro

- Integrante 1
- Integrante 2
- Integrante 3
- Integrante 4
- Integrante 5

