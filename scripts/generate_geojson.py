import time
import logging
import emtvlcapi
import geojson

# Configura el logger
logging.basicConfig(level=logging.INFO)

# Definir un área más grande para la búsqueda (ajusta las coordenadas)
zones = [
    (39.39, -0.45, 39.42, -0.43),
    (39.42, -0.43, 39.45, -0.40),
    (39.45, -0.40, 39.47, -0.38),
    (39.47, -0.38, 39.50, -0.35),
    (39.50, -0.35, 39.52, -0.33),
    (39.52, -0.33, 39.54, -0.30),
    (39.54, -0.30, 39.56, -0.28),
    (39.56, -0.28, 39.58, -0.25),
    (39.58, -0.25, 39.60, -0.22),
]

# Función para obtener paradas con reintentos
def get_stops_with_retry(lat1, lon1, lat2, lon2):
    retries = 3
    for attempt in range(retries):
        try:
            logging.info(f"Fetching stops in area: ({lat1}, {lon1}) to ({lat2}, {lon2})")
            stops = emtvlcapi.get_stops_in_extent(lat1, lon1, lat2, lon2)
            return stops
        except Exception as e:
            logging.error(f"Attempt {attempt + 1} failed: {e}")
            if attempt == retries - 1:
                raise  # Re-lanza el error después de varios intentos
            time.sleep(2)  # Espera antes de reintentar

# Función para generar el GeoJSON
def create_geojson():
    all_stops = []
    for zone in zones:
        lat1, lon1, lat2, lon2 = zone
        stops = get_stops_with_retry(lat1, lon1, lat2, lon2)
        if stops:
            all_stops.extend(stops)
        else:
            logging.warning(f"No stops found for the area: ({lat1}, {lon1}) to ({lat2}, {lon2})")
    
    features = []
    for stop in all_stops:
        # Crear un feature por cada parada
        feature = geojson.Feature(
            geometry=geojson.Point((float(stop['lon']), float(stop['lat']))),
            properties={
                "name": stop.get("name"),
                "stopId": stop.get("stopId"),
                "routes": stop.get("routes"),
            }
        )
        features.append(feature)
    
    # Crear el archivo GeoJSON
    feature_collection = geojson.FeatureCollection(features)
    
    # Guardar el archivo
    with open('data/stops_with_bus_times.geojson', 'w') as f:
        geojson.dump(feature_collection, f)
    
    logging.info(f"GeoJSON file created with {len(features)} features.")

# Ejecutar la función para crear el GeoJSON
if __name__ == "__main__":
    create_geojson()
