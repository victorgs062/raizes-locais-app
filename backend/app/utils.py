import math

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calcula a distância do grande círculo entre dois pontos na superfície da Terra 
    usando a fórmula de Haversine.

    Parâmetros:
    - lat1 (float): Latitude do ponto 1.
    - lon1 (float): Longitude do ponto 1.
    - lat2 (float): Latitude do ponto 2.
    - lon2 (float): Longitude do ponto 2.

    Retorno:
    - float: A distância em quilômetros. Retorna 0.0 se algum dos pontos for None.
    """
    if None in (lat1, lon1, lat2, lon2):
        return 0.0

    # Converter latitude e longitude de graus para radianos
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Fórmula de Haversine
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371 # Raio da Terra em quilômetros.
    
    return c * r

def calculate_co2_savings(distance_km: float, weight_kg: float = 1.0) -> float:
    """
    Estima a economia de CO2 ao comprar localmente em comparação com produtos industrializados.

    Parâmetros:
    - distance_km (float): A distância entre o produtor e o consumidor em km.
    - weight_kg (float): O peso do produto em kg (padrão 1.0).

    Retorno:
    - float: A quantidade de CO2 economizada em kg (arredondada em 2 casas decimais).
    
    Regra de negócio:
    - Assume-se que alimentos industrializados viajam em média 1500km.
    - Assume-se que a emissão média de um caminhão é de 0.15 kg de CO2 por tonelada-km.
    - Se a distância local for maior ou igual a 1500km, a economia é zero.
    """
    avg_industrial_distance_km = 1500.0
    
    # Se a distância local for maior que a industrial, não há economia
    if distance_km >= avg_industrial_distance_km:
        return 0.0
    
    distance_saved = avg_industrial_distance_km - distance_km
    
    # Emissões = distância * peso(em toneladas) * fator de emissão
    weight_tons = weight_kg / 1000.0
    emission_factor = 0.15 # kg CO2 por tonelada-km
    
    co2_saved_kg = distance_saved * weight_tons * emission_factor
    
    return round(co2_saved_kg, 2)
