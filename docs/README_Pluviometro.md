# Pluviômetro — Integração com a Estação Meteorológica

Este documento descreve o subsistema de precipitação desenvolvido para ampliar a estação meteorológica de baixo custo.

O **núcleo do projeto do pluviômetro** é formado pelo medidor basculante, sua conexão elétrica com o Raspberry Pi e o software responsável por contabilizar, converter, armazenar e sincronizar as medições.

Os suportes, tubos e demais peças utilizadas na instalação do Colégio João XXIII são uma implementação específica daquele local e podem ser substituídos em outras instalações, desde que os requisitos técnicos de captação, nivelamento, escoamento e calibração sejam preservados.

## Objetivo

Substituir a dependência exclusiva de estimativas de chuva obtidas por API externa por medições locais realizadas por um pluviômetro físico.

O subsistema deve:

- detectar cada basculada do medidor;
- transmitir o sinal ao Raspberry Pi;
- contabilizar os pulsos;
- converter pulsos em milímetros de precipitação;
- armazenar os dados localmente;
- sincronizar as medições com o MariaDB;
- preservar registros durante falhas de comunicação;
- possibilitar comparação com uma medição manual de referência.

## Funcionamento do pluviômetro basculante

O pluviômetro possui um mecanismo de báscula. Quando uma quantidade determinada de água é coletada, a báscula muda de posição.

Um ímã integrado ao mecanismo passa próximo de um **reed switch**, alterando o estado elétrico do contato. O Raspberry Pi detecta essa mudança pelo GPIO e registra um pulso.

Fluxo simplificado:

```text
Chuva
  ↓
Área de captação
  ↓
Báscula
  ↓
Ímã + reed switch
  ↓
Pulso elétrico
  ↓
GPIO17 do Raspberry Pi
  ↓
Contador de pulsos
  ↓
Conversão para mm
  ↓
SQLite
  ↓
MariaDB
```

## Hardware essencial

Para o núcleo do subsistema são necessários:

- pluviômetro automático de báscula;
- mecanismo magnético/reed switch do próprio medidor;
- cabeamento de dois condutores;
- Raspberry Pi;
- materiais de conexão elétrica adequados.

O pluviômetro utilizado pela equipe custou aproximadamente **R$ 50,00**. Pequenos componentes de ligação, cabos e materiais eletromecânicos adicionais foram estimados em até **R$ 20,00**.

Esses valores não incluem o Raspberry Pi já pertencente à estação, nem a estrutura física específica de cada local de instalação.

## Ligação ao Raspberry Pi 4

Na instalação realizada pela equipe:

| Cabo | Pino físico | GPIO | Função |
|---|---:|---:|---|
| Vermelho | 11 | GPIO17 | Entrada de sinal do reed switch |
| Verde | 14 | GND | Terra |

![Pinagem do Raspberry Pi 4](docs/images/raspberry-pi-4-pinout.jpeg)

![Ligação do pluviômetro no Raspberry Pi](docs/images/raspberry-ligacao-pluviometro.jpeg)

O código utiliza numeração **BCM** para o GPIO. Portanto, o valor de configuração correspondente é:

```text
RAIN_GPIO_PIN=17
```

## Leitura no software

O coletor utiliza `gpiozero.Button` com resistor de pull-up e debounce por software.

A configuração atual corresponde conceitualmente a:

```python
rain_button = Button(
    RAIN_GPIO_PIN,
    pull_up=True,
    bounce_time=0.2
)

rain_button.when_pressed = _rain_pulse_callback
```

Quando uma basculada é detectada, o callback incrementa `rain_pulse_count`.

Cada pulso também pode ser registrado no log com uma mensagem semelhante a:

```text
Pulso pluviômetro detectado. Total: X
```

Isso facilita a validação da conexão física sem depender do banco de dados.

## Conversão de pulsos para precipitação

A chuva é calculada pela relação:

```text
precipitação (mm) = quantidade de pulsos × mm por pulso
```

O valor de conversão deve ser obtido por calibração da área de captação e do volume correspondente a cada basculada.

### Valor de calibração do projeto

Os cálculos registrados pela equipe consideram aproximadamente:

- área de captação: **54,7854 cm²**;
- volume por basculada: **1,6 mL**;
- fator calculado: **0,29205 mm por basculada**.

### Atenção: valor do código

O coletor atual possui `0.297` como fallback de `RAIN_MM_PER_PULSE` quando a variável não é definida.

Para evitar divergência entre documentação e medição, configure explicitamente o valor adotado pela calibração:

```text
RAIN_MM_PER_PULSE=0.29205
```

ou substitua esse valor pelo resultado de uma nova calibração caso a geometria da área de captação seja alterada.

## Ciclo de coleta

O pluviômetro não gera necessariamente uma linha no banco para cada basculada.

O coletor acumula os pulsos e, em ciclos de aproximadamente **5 minutos**, calcula a precipitação total do intervalo:

```text
pulsos detectados no intervalo
        ↓
RAIN_MM_PER_PULSE
        ↓
precipitação acumulada no período
        ↓
registro meteorológico
```

Depois do cálculo, o contador do intervalo é zerado para iniciar a próxima janela de coleta.

## Persistência e buffer local

O coletor atual utiliza SQLite como buffer local:

```text
~/.config/station/buffer_sensores.db
```

Tabela:

```text
buffer_raspdata
```

Ela armazena, entre outros campos:

- `rcID`;
- temperatura;
- umidade;
- pressão;
- luminosidade;
- precipitação (`Pluv`);
- data/hora da gravação local.

O fluxo implementado é:

1. calcular a leitura do período;
2. gravar o registro no SQLite;
3. verificar conectividade;
4. tentar conexão com MariaDB;
5. enviar registros pendentes;
6. confirmar a transação;
7. remover do SQLite apenas o registro enviado com sucesso.

Dessa forma, uma interrupção de rede não precisa causar perda imediata das medições.

## Configuração necessária

O coletor atual utiliza as seguintes variáveis relevantes:

```text
RAIN_GPIO_PIN=17
RAIN_MM_PER_PULSE=0.29205
```

Também são necessárias as configurações do banco:

```text
DB_HOST
DB_PORT
DB_USER
DB_PASS
DB_NAME
```

> Os documentos herdados descrevem versões do instalador que inseriam credenciais diretamente no script Python. O coletor atual utiliza variáveis de ambiente. Ao utilizar o instalador legado, confirme que ele foi atualizado para fornecer essas configurações ao serviço.

## Requisitos gerais de instalação

A estrutura de suporte pode variar, mas alguns requisitos devem ser mantidos.

### Localização e obstáculos

O pluviômetro deve permanecer em local aberto e com a menor interferência possível de árvores, prédios, paredes e outras estruturas.

Como referência de projeto, foi adotada a regra de manter distância equivalente a aproximadamente duas a quatro vezes a altura dos obstáculos próximos quando isso for viável no local.

### Altura

A boca do coletor deve ser instalada em uma altura adequada para reduzir interferências do solo, respingos e obstáculos próximos. No projeto foi adotada como referência uma faixa de aproximadamente **1 m a 1,5 m**, sempre que as condições do local permitirem.

Em instalações elevadas, como a do Colégio João XXIII, a geometria e a exposição do ponto de coleta devem ser avaliadas de acordo com as condições reais do prédio.

### Nivelamento

O medidor deve permanecer perfeitamente nivelado e mecanicamente estável.

Inclinação, vibração ou movimento do suporte podem alterar a quantidade de água necessária para realizar a basculada e comprometer a medição.

### Área de captação

A área utilizada durante a calibração precisa ser preservada.

Se o funil, tampa, bocal ou qualquer outro componente modificar a área efetiva de captação, o valor de `RAIN_MM_PER_PULSE` deve ser recalculado e validado novamente.

### Escoamento

A água precisa sair do sistema depois de passar pelo mecanismo de medição.

O projeto do suporte deve evitar represamento, retorno de água ou acúmulo que possa interferir nas basculadas seguintes.

## Instalação de referência — Colégio João XXIII

O Colégio João XXIII ofereceu o local para testes e apoio de sua equipe de manutenção. A escola **não foi a idealizadora do projeto**.

A instalação realizada no colégio foi adaptada ao prédio e ao ponto disponível no telhado.

### Estrutura utilizada

O medidor basculante foi fixado sobre uma **tampa de PVC DN200**. Essa tampa foi integrada a uma estrutura com tubos que permitem que a água, após passar pelo pluviômetro, seja conduzida para baixo.

Foram utilizados na montagem local:

- tubo bicromatizado para antena de 1 polegada;
- suporte de antena para telhado;
- suporte tipo cavalete;
- tampa PVC DN200/200 mm;
- tubulação de escoamento;
- cabos e materiais auxiliares de fixação.

Esses componentes **não fazem parte obrigatória do núcleo do pluviômetro**. Eles foram escolhidos para resolver as necessidades específicas da instalação no prédio.

### Instalação pela equipe de manutenção

A montagem no ponto elevado e a fixação da estrutura foram realizadas pela equipe de manutenção da escola.

![Equipe de manutenção realizando a instalação](docs/images/instalacao-telhado-joao-xxiii.jpeg)

### Extensão dos cabos

Os dois fios do reed switch foram prolongados da região do telhado até o interior do prédio.

No interior, foram ligados ao Raspberry Pi 4 conforme a pinagem apresentada anteriormente.

![Raspberry Pi após a integração com o pluviômetro](docs/images/raspberry-instalado.jpeg)

## Pluviômetro manual de referência

Além do sistema automático, foi adotado um pluviômetro manual Incoterm, com custo aproximado de **R$ 22,00**.

![Pluviômetro manual de referência](docs/images/pluviometro-manual-incoterm.jpeg)

Ele possui duas finalidades principais:

1. disponibilizar uma medição visual independente para comparação com o valor eletrônico;
2. permitir atividades didáticas nas quais os alunos possam observar a chuva acumulada e comparar a leitura manual com a estação automática.

Essa abordagem está alinhada ao objetivo de desenvolver uma estação meteorológica de baixo custo com aplicação educacional.

## Custos da instalação de referência

Os valores abaixo correspondem à instalação realizada no Colégio João XXIII e **não representam o custo mínimo obrigatório para replicar o pluviômetro**.

| Item | Valor aproximado |
|---|---:|
| Tubo bicromatizado 1" x 2 m | R$ 45,00 |
| Suporte de antena para telhado | R$ 48,00 |
| Suporte tipo cavalete | R$ 22,55 |
| Tampa PVC DN200 | R$ 48,52 |
| Pluviômetro basculante | R$ 50,00 |
| Pequenos componentes/cabos | até R$ 20,00 |
| Pluviômetro manual | R$ 22,00 |
| **Total da configuração de referência** | **até R$ 256,07** |

O Raspberry Pi e os sensores herdados não estão incluídos nesse total.

## Testes recomendados

### 1. Teste mecânico

Faça basculadas manuais e confirme que o mecanismo retorna corretamente a cada posição.

### 2. Teste do reed switch/GPIO

Com o coletor em execução, faça várias basculadas e acompanhe o log.

O contador deve continuar aumentando:

```text
Pulso pluviômetro detectado. Total: 1
Pulso pluviômetro detectado. Total: 2
Pulso pluviômetro detectado. Total: 3
...
```

### 3. Teste do ciclo de 5 minutos

Conte manualmente os pulsos de um intervalo e compare com o valor gravado:

```text
pulsos × RAIN_MM_PER_PULSE = precipitação esperada
```

### 4. Teste do SQLite

Confira os últimos registros do buffer:

```bash
sqlite3 ~/.config/station/buffer_sensores.db \
  "SELECT * FROM buffer_raspdata ORDER BY id DESC LIMIT 10;"
```

### 5. Teste sem rede

Interrompa somente a conectividade de rede de forma controlada e verifique se os registros continuam sendo preservados no SQLite.

### 6. Teste de sincronização

Restabeleça a rede e confira se os registros pendentes são enviados ao MariaDB e removidos do buffer somente após o envio bem-sucedido.

### 7. Comparação manual

Durante chuva real, compare a precipitação do sistema automático com o pluviômetro manual instalado como referência.

## Logs e serviço

O sistema herdado utiliza um serviço `systemd` para manter o coletor ativo e reiniciá-lo caso o processo seja encerrado.

Os materiais do projeto utilizam nomes diferentes para a unidade entre versões (`sensorcollect.service` e `raspcollect.service`). Utilize o nome presente no repositório instalado.

Status:

```bash
sudo systemctl status NOME_DO_SERVICO.service
```

Logs em tempo real:

```bash
journalctl -u NOME_DO_SERVICO.service -f
```

Para localizar eventos do pluviômetro:

```bash
journalctl -u NOME_DO_SERVICO.service | grep -i "pluviômetro"
```

## Observações de manutenção

- Não altere a área de captação sem recalibrar o fator de conversão;
- verifique periodicamente se o mecanismo basculante está livre;
- mantenha o coletor nivelado;
- confira se os cabos não estão tensionados ou com mau contato;
- mantenha as conexões elétricas protegidas;
- confira os logs caso as medições deixem de aparecer;
- valide periodicamente a leitura automática com a medição manual.

