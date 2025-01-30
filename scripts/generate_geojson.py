import emtvlcapi
import geojson
import logging

# Configurar los logs para ver el proceso
logging.basicConfig(level=logging.INFO)

# Función para obtener las paradas en una zona determinada
def create_geojson():
    lat1, lon1, lat2, lon2 = 39.39, -0.45, 39.42, -0.43  # Coordenadas de Valencia

    try:
        logging.info(f"Fetching stops in area: ({lat1}, {lon1}) to ({lat2}, {lon2})")
        stops = emtvlcapi.get_stops_in_extent(lat1, lon1, lat2, lon2)

        if not stops:
            logging.error("No stops found in this area.")
            return

        geojson_data = {
            "type": "FeatureCollection",
            "features": []
        }

        for stop in stops:
            stop_id = stop['id']
            logging.info(f"Fetching arrival times for stop {stop_id}")

            try:
                arrival_times = emtvlcapi.get_arrival_times(stop_id)
                logging.info(f"API Response for stop {stop_id}: {arrival_times}")

                if arrival_times:
                    # Formatear tiempos en una lista
                    next_buses = "; ".join([f"Línea {bus['line']}: {bus['time']} min" for bus in arrival_times])
                else:
                    next_buses = "No disponible"
                    
            except Exception as e:
                logging.error(f"Error fetching arrival times for stop {stop_id}: {e}")
                next_buses = "Error"

            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [stop['lon'], stop['lat']]
                },
                "properties": {
                    "name": stop['name'],
                    "id": stop_id,
                    "next_buses": next_buses  # Añadir info de autobuses próximos
                }
            }
            geojson_data['features'].append(feature)
        
        with open('data/stops.geojson', 'w') as f:
            geojson.dump(geojson_data, f)
        logging.info("GeoJSON file generated successfully.")
    
    except Exception as e:
        logging.error(f"An error occurred: {e}")

# Llamada a la función para generar el GeoJSON
create_geojson()
