# Microsserviço de Estimativa de Viagem

## Introdução

Este documento descreve a arquitetura e o funcionamento de um microsserviço baseado em gRPC, projetado para estimar o custo e o tempo de deslocamento entre dois pontos utilizando diversas APIs de serviços REST, incluindo Google Places, Google Maps, Waze e Petrobrás. O objetivo é fornecer uma solução robusta e eficiente para calcular rotas e estimar custos de transporte, integrando dados de múltiplas fontes.

## Funcionalidades

O microsserviço oferece as seguintes funcionalidades:

1. **Consulta de Locais**: Utiliza a API do Google Places para encontrar e validar pontos de origem e destino.
2. **Cálculo de Rotas**: Utiliza a API do Google Maps para calcular a melhor rota entre os pontos fornecidos.
3. **Estimativa de Tempo**: Utiliza a API do Waze para fornecer estimativas de tempo baseadas no tráfego em tempo real.
4. **Estimativa de Custo**: Utiliza a API da Petrobrás para estimar o custo da viagem com base nos preços atuais de combustível.

## Arquitetura

O microsserviço é composto por vários módulos, cada um responsável por interagir com uma das APIs de serviços REST. A arquitetura segue o padrão de microsserviços, garantindo escalabilidade, manutenção e facilidade de desenvolvimento. O uso do gRPC possibilita a troca de dados em tempo real e escalável.

### Componentes Principais

1. **gRPC Gateway**: Gerencia as requisições dos clientes e distribui entre os diversos microsserviços.
2. **Serviço de Locais**: Responsável por interagir com a API do Google Places.
3. **Serviço de Rotas**: Responsável por interagir com a API do Google Maps.
4. **Serviço de Tráfego**: Responsável por interagir com a API do Waze.
5. **Serviço de Preços**: Responsável por interagir com a API da Petrobrás.

### Fluxo de Dados

1. **Recepção de Dados**: O cliente envia uma requisição ao gRPC Gateway com os pontos de origem e destino.
2. **Consulta de Locais**: O Serviço de Locais valida os pontos fornecidos utilizando a API do Google Places.
3. **Cálculo de Rotas**: O Serviço de Rotas calcula a melhor rota utilizando a API do Google Maps.
4. **Estimativa de Tempo**: O Serviço de Tráfego consulta a API do Waze para obter informações de tráfego em tempo real e fornecer uma estimativa precisa de tempo e distância.
5. **Estimativa de Custo**: O Serviço de Preços consulta a API da Petrobrás para estimar o custo da viagem com base nos preços atuais de combustível.
6. **Resposta ao Cliente**: As estimativas de custo e tempo são compiladas e enviadas de volta ao cliente via gRPC Gateway.

## Integração com APIs de Serviços REST
### Google Places API

- **Endpoint**: `/maps/api/place/`
- **Função**: Validar e obter detalhes sobre os locais de origem e destino.

### Google Maps API

- **Endpoint**: `/maps/api/directions/`
- **Função**: Calcular rotas entre os pontos fornecidos.

### Waze API

- **Endpoint**: `/row-RoutingManager/routingRequest`
- **Função**: Fornecer informações de distância, tempo de viagem e de tráfego em tempo real (com diferença de tempo em vias livres e congestionadas).

### Petrobrás (Webscrapping)

- **Endpoint**: `"https://precos.petrobras.com.br/web/precos-dos-combustiveis/w/gasolina/"`
- **Função**: Estimar o custo da viagem com base nos preços atuais de combustível da Petrobrás.

## Instalação

Siga as etapas abaixo para executar o microsserviço:

### Pré-requisitos

- Python 3.12 ou superior
- Ambiente virtual (recomendado)

#### Instalação de Dependências
Instale as dependências usando pip:
   ```bash
   pip install -r src/requirements.txt
```

## Execução

Pode ser que seja necessário adicionar a pasta src ao PYTHON PATH. Para isso, basta executar o seguinte comando na raíz do projeto:

```bash
export PYTHONPATH=$PWD/src
```

### Iniciar o Servidor

Para iniciar o servidor gRPC, execute o seguinte comando:

```bash
python src/server/server.py
```

Este comando inicia o seu servidor gRPC.

#### Executar Testes

##### Teste do Serviço de Custo

```bash
python src/tests/cost_service_test.py
```

##### Teste do Serviço de Localização

```bash
python src/tests/place_service_test.py
```

##### Teste do Serviço de Rota

```bash
python src/tests/route_service_test.py
```

##### Teste do Serviço de Tráfego

```bash
python src/tests/traffic_service_test.py
```

