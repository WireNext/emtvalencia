import emtvlcapi
import geojson
import logging
import os

logging.basicConfig(level=logging.INFO)

def create_geojson():
    lat1, lon1, lat2, lon2 = 39.39, -0.45, 39.42, -0.43  

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
                    "next_buses": next_buses
                }
            }
            geojson_data['features'].append(feature)
        
        geojson_path = 'data/stops.geojson'

        # FORZAR QUE EL ARCHIVO SE SOBREESCRIBA
        if os.path.exists(stops.geojson):
            os.remove(stops.geojson)  # Borra el archivo viejo

        with open(stops.geojson, 'w') as f:
            geojson.dump(geojson_data, f)

        logging.info("GeoJSON file generated successfully.")

        # COMPROBAR SI REALMENTE SE ESCRIBIÓ
        with open(geojson_path, 'r') as f:
            content = f.read()
            logging.info(f"File content: {content[:500]}")  # Muestra solo los primeros 500 caracteres
    
    except Exception as e:
        logging.error(f"An error occurred: {e}")

# Llamada a la función
create_geojson()
