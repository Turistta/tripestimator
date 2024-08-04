from travel_pb2 import CostResponse, CostEstimate
import requests
from bs4 import BeautifulSoup


class CostService:
    BASE_URL = "https://precos.petrobras.com.br/web/precos-dos-combustiveis/w/gasolina/"

    def __init__(self):
        pass

    def _gas_finder(self, state):
        url = self.BASE_URL + state

        try:
            response = requests.get(url)
            response.raise_for_status()  # Verifica se houve erros na requisição
        except requests.RequestException as e:
            print(f"Erro ao fazer a requisição: {e}")
            return None
        try:
            soup = BeautifulSoup(response.text, "html.parser")
            price_txt = soup.find(id="telafinal-precofinal").get_text()
            price = float(price_txt.replace(",", "."))
        except AttributeError as e:
            print(f"Erro ao encontrar o preço na página: {e}")
            return None
        except ValueError as e:
            print(f"Erro ao converter o preço para float: {e}")
            return None
        return price

    def estimate_cost(self, state, distance_km, time_estimated, traffic_condition):
        try:
            fuel_price = self._gas_finder(state)
            if fuel_price is None:
                raise ValueError("Não foi possível obter o preço do combustível.")

            # Verificação de entrada inválida
            if distance_km <= 0:
                raise ValueError("A distância deve ser maior que zero.")
            if time_estimated <= 0:
                raise ValueError("O tempo de viagem deve ser maior que zero.")

            BASE_COST = 5.0  # Tarifa base em R$
            TIME_FACTOR = 0.5  # Custo do tempo em R$/minuto
            FUEL_CONSUME = 10  # Média de 10km/l
            TRAFFIC_CONDITION_WEIGHT = {"light": 1.0, "moderate": 1.2, "heavy": 1.5}

            # Cálculos
            fuel_cost = (distance_km / FUEL_CONSUME) * fuel_price
            time_cost = (
                time_estimated / 60
            ) * TIME_FACTOR  # Conversão de segundos para minutos
            traffic_weight = TRAFFIC_CONDITION_WEIGHT.get(traffic_condition, 1.0)
            final_cost = BASE_COST + (fuel_cost * traffic_weight) + time_cost

            if final_cost <= 0:
                return CostResponse(warnings=["Erro ao estimar o custo."])

            return CostResponse(
                cost_estimate=CostEstimate(estimated_cost=final_cost), warnings=[]
            )

        except ValueError as ve:
            return CostResponse(warnings=[f"Erro de valor: {ve}"])
        except Exception as e:
            return CostResponse(warnings=[f"Ocorreu um erro inesperado: {e}"])
