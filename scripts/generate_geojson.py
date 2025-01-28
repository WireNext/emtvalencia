import emtvlcapi
import json
import time

# Función para obtener paradas en una extensión de coordenadas
def get_stops_with_retry(lat1, lon1, lat2, lon2, retries=3):
    for _ in range(retries):
        try:
            # Intentar obtener las paradas
            stops = emtvlcapi.get_stops_in_extent(lat1, lon1, lat2, lon2)
            
            # Si la respuesta tiene paradas, devolverlas
            if stops:
                return stops
            
            # Si no hay resultados, esperar un poco y reintentar
            print(f"No stops found in the area: ({lat1}, {lon1}) to ({lat2}, {lon2}). Retrying...")
            time.sleep(2)  # Esperar 2 segundos antes de reintentar
        except Exception as e:
            print(f"Error retrieving stops: {e}")
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
        # Centro de Valencia
        (39.460000, -0.390000, 39.510000, -0.420000),  # Área más grande que cubre el centro de Valencia
        
        # Zona sur
        (39.395000, -0.380000, 39.460000, -0.410000),  # Incluye barrios como Benicalap y Cruz Cubierta
        
        # Zona norte
        (39.480000, -0.430000, 39.510000, -0.370000),  # Incluye la zona de la Malva-rosa, Albufera
        
        # Zona playa y alrededores
        (39.375000, -0.400000, 39.420000, -0.430000),  # Costa y playa (Malva-rosa, Albufera)
        
        # Zona oeste
        (39.460000, -0.460000, 39.510000, -0.490000)   # Zona más alejada hacia el oeste de la ciudad
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
