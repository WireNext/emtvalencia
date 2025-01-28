import emtvlcapi
import geojson
import logging

# Configurar los logs para ver el proceso
logging.basicConfig(level=logging.INFO)

# Función para obtener las paradas en una zona determinada
def create_geojson():
    # Definir las coordenadas de la zona (puedes ajustar las coordenadas a tu gusto)
    lat1, lon1, lat2, lon2 = 39.39, -0.45, 39.42, -0.43  # Ejemplo de coordenadas de Valencia
    
    # Obtener las paradas en esa zona
    logging.info(f"Fetching stops in area: ({lat1}, {lon1}) to ({lat2}, {lon2})")
    stops = emtvlcapi.get_stops_in_extent(lat1, lon1, lat2, lon2)

    # Crear el objeto GeoJSON
    geojson_data = {
        "type": "FeatureCollection",
        "features": []
    }

    for stop in stops:
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [stop['lon'], stop['lat']]  # Asegúrate de usar las claves correctas de longitud y latitud
            },
            "properties": {
                "name": stop['name'],  # Nombre de la parada
                "id": stop['id'],      # ID de la parada (puedes agregar más datos si lo deseas)
            }
        }
        geojson_data['features'].append(feature)
    
    # Guardar el archivo GeoJSON
    with open('data/stops.geojson', 'w') as f:
        geojson.dump(geojson_data, f)

# Llamada a la función para generar el GeoJSON
create_geojson()
