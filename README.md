# Microsserviço de Estimativa de Viagem

## Introdução

Este documento descreve a arquitetura e o funcionamento de um microsserviço baseado em REST, projetado para estimar o custo e o tempo de deslocamento entre dois pontos utilizando diversas APIs de serviços REST, incluindo Google Places, Google Maps, Tomtom e Petrobrás. O objetivo é fornecer uma solução robusta e eficiente para calcular rotas e estimar custos de transporte, integrando dados de múltiplas fontes.

## Funcionalidades

O microsserviço oferece as seguintes funcionalidades:

1. **Consulta de Locais**: Utiliza a API do Google Places para encontrar e validar pontos de origem e destino.
2. **Cálculo de Rotas**: Utiliza a API do Google Maps para calcular a melhor rota entre os pontos fornecidos.
3. **Estimativa de Tráfego**: Utiliza a API do Tomtom para fornecer estimativas de tempo baseadas no tráfego em tempo real.
4. **Estimativa de Custo**: Utiliza dados da Petrobrás para estimar o custo da viagem com base nos preços atuais de combustível.

### Componentes Principais

1. **Servidor FastAPI**: Gerencia as requisições dos clientes e distribui entre os diversos serviços.
2. **Serviço de Locais**: Responsável por interagir com a API do Google Places.
3. **Serviço de Rotas**: Responsável por interagir com a API do Google Maps.
4. **Serviço de Tráfego**: Responsável por interagir com a API do Tomtom.
5. **Serviço de Preços**: Responsável por interagir com a API da Petrobrás.

### Fluxo de Dados

1. **Recepção de Dados**: O cliente envia uma requisição para a API Gateway com os pontos de origem e destino.
2. **Consulta de Locais**: O Serviço de Locais valida os pontos fornecidos utilizando a API do Google Places.
3. **Cálculo de Rotas**: O Serviço de Rotas calcula a melhor rota utilizando a API do Google Maps.
4. **Estimativa de Tempo**: O Serviço de Tráfego consulta a API do Tomtom para obter informações de tráfego em tempo real e fornecer uma estimativa precisa de tempo e distância.
5. **Estimativa de Custo**: O Serviço de Preços consulta a API da Petrobrás para estimar o custo da viagem com base nos preços atuais de combustível.
6. **Resposta ao Cliente**: As estimativas de custo e tempo são compiladas e enviadas de volta ao cliente na forma de um objeto JSON, TourItinerary.

## Integração com APIs de Serviços REST

### Google Places API

- **Endpoint**: `https://maps.googleapis.com/maps/api/place/{query_type}/json`
- **Função**: Validar e obter detalhes sobre os locais de origem e destino.

### Google Routes API

- **Endpoint**: `https://routes.googleapis.com/directions/v2:computeRoutes`
- **Função**: Calcular rotas entre os pontos fornecidos.

### Tomtom API

- **Endpoint**: `/row-RoutingManager/routingRequest`
- **Função**: Fornecer informações de distância, tempo de viagem e de tráfego em tempo real (com diferença de tempo em vias livres e congestionadas).

### Petrobrás (Webscraping)

- **Endpoint**: `"https://precos.petrobras.com.br/web/precos-dos-combustiveis/w/gasolina/"`
- **Função**: Estimar o custo da viagem com base nos preços atuais de combustível da Petrobrás.

## Instalação

Siga as etapas abaixo para executar o microsserviço:

### Pré-requisitos

- Python 3.12 ou superior
- [Ambiente Virtual](https://docs.python.org/3/library/venv.html#venv-def) (recomendado)
- Chave de API Google Maps
- Chave de API TomTom

#### Instalação de Dependências

Instale as dependências usando pip:

```bash
pip install -r requirements.txt
```

#### Configuração das variáveis de ambiente

Renomeie o arquivo `.env_sample` em `src`, para `.env` e substitua os valores das chaves.


## Execução

Pode ser que seja necessário adicionar a pasta src ao PYTHON PATH. Para isso, basta executar o seguinte comando na raiz do projeto:

```bash
export PYTHONPATH=$PWD/src
```

### Iniciar o Servidor

Para iniciar o servidor FastAPI, apenas execute o arquivo `server.py`:

```bash
uvicorn src/server:app --reload --port 3000 --host 0.0.0.0
```

Este comando inicia o seu servidor FastAPI.

#### Executar Testes

Para executar todos os testes, basta executar:

```bash
pytest
```

##### Testes dos Serviços

Para executar os testes individualmente por serviço, basta executar o caminho do arquivo de testes. O comando, por exemplo

```bash
pytes src/tests/cost
```

Executa apenas os testes do serviço de custos.
