import emtvlcapi
import json
import time

# Función para obtener paradas en una extensión de coordenadas
def get_stops_with_retry(lat1, lon1, lat2, lon2, retries=3):
    for _ in range(retries):
        # Intentar obtener las paradas
        stops = emtvlcapi.get_stops_in_extent(lat1, lon1, lat2, lon2)
        
        # Si la respuesta tiene paradas, devolverlas
        if stops:
            return stops
        
        # Si no hay resultados, esperar un poco y reintentar
        print(f"No stops found in the area: ({lat1}, {lon1}) to ({lat2}, {lon2}). Retrying...")
        time.sleep(2)  # Esperar 2 segundos antes de reintentar
    
    # Si no se encuentran paradas después de los reintentos, devolver una lista vacía
    print(f"No stops found after {retries} retries in area: ({lat1}, {lon1}) to ({lat2}, {lon2}).")
    return []

# Función para convertir las paradas a formato GeoJSON
def create_geojson(lat1, lon1, lat2, lon2):
    # Obtener las paradas con reintentos
    stops = get_stops_with_retry(lat1, lon1, lat2, lon2)
    
    if not stops:  # Si no se obtienen paradas, devolver un GeoJSON vacío
        return {
            "type": "FeatureCollection",
            "features": []
        }

    # Estructura base del GeoJSON
    geojson = {
        "type": "FeatureCollection",
        "features": []
    }

    # Convertir las paradas a formato GeoJSON
    for stop in stops:
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [float(stop['lon']), float(stop['lat'])]
            },
            "properties": {
                "name": stop['name'],
                "stopId": stop['stopId'],
                "routes": ", ".join(
                    [f"{route['SN']} - {route['LN']}" for route in stop['routes']]
                ),
                "location": stop['ubica']
            }
        }
        geojson["features"].append(feature)

    return geojson

# Función principal para obtener todas las paradas
def fetch_all_stops():
    # Definir las coordenadas para dividir la ciudad en áreas más amplias
    subareas = [
        (39.460000, -0.390000, 39.510000, -0.420000),  # Área más grande que cubre el centro de Valencia
        (39.471964, -0.394641, 39.476000, -0.400000),  # Subárea más amplia
        (39.473000, -0.399000, 39.478000, -0.405000),  # Subárea
        (39.474000, -0.405000, 39.479000, -0.410000)   # Otra subárea más amplia
    ]
    
    # Crear la estructura del GeoJSON
    geojson = {
        "type": "FeatureCollection",
        "features": []
    }
    
    # Obtener las paradas de cada subárea
    for lat1, lon1, lat2, lon2 in subareas:
        print(f"Fetching stops in area: ({lat1}, {lon1}) to ({lat2}, {lon2})")
        stops = create_geojson(lat1, lon1, lat2, lon2)
        geojson["features"].extend(stops["features"])  # Agregar las paradas obtenidas al GeoJSON
    
    return geojson

# Ejecutar la función principal y guardar el archivo GeoJSON
if __name__ == "__main__":
    all_stops_geojson = fetch_all_stops()  # Obtener todas las paradas en formato GeoJSON
    with open("data/stops.geojson", "w") as f:
        json.dump(all_stops_geojson, f, indent=4)  # Guardar el GeoJSON en un archivo
    print("Archivo GeoJSON generado: data/stops.geojson")
