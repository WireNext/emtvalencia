import emtvlcapi
import geojson
import logging

# Configurar los logs para ver el proceso
logging.basicConfig(level=logging.INFO)

# Función para obtener las paradas en una zona determinada
def create_geojson():
    # Definir las coordenadas de la zona (puedes ajustar las coordenadas a tu gusto)
    lat1, lon1, lat2, lon2 = 39.39, -0.45, 39.42, -0.43  # Ejemplo de coordenadas de Valencia

    try:
        # Obtener las paradas en esa zona
        logging.info(f"Fetching stops in area: ({lat1}, {lon1}) to ({lat2}, {lon2})")
        stops = emtvlcapi.get_stops_in_extent(lat1, lon1, lat2, lon2)

        # Comprobar si se obtuvieron resultados
        if not stops:
            logging.error("No stops found in this area.")
            return

        # Crear el objeto GeoJSON
        geojson_data = {
            "type": "FeatureCollection",
            "features": []
        }

        for stop in stops:
            stop_id = stop['id']
            
            # Obtener tiempos de llegada del próximo autobús
            try:
                arrival_times = emtvlcapi.get_arrival_times(stop_id)
                next_bus_time = arrival_times[0]['time'] if arrival_times else "No disponible"
            except Exception as e:
                logging.error(f"Error fetching arrival times for stop {stop_id}: {e}")
                next_bus_time = "Error"

            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [stop['lon'], stop['lat']]
                },
                "properties": {
                    "name": stop['name'],
                    "id": stop_id,
                    "next_bus": next_bus_time  # Añadir la hora de llegada del próximo bus
                }
            }
            geojson_data['features'].append(feature)
        
        # Guardar el archivo GeoJSON
        with open('data/stops.geojson', 'w') as f:
            geojson.dump(geojson_data, f)
        logging.info("GeoJSON file generated successfully.")
    
    except Exception as e:
        logging.error(f"An error occurred: {e}")

# Llamada a la función para generar el GeoJSON
create_geojson()
