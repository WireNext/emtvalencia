import asyncio
import aiohttp
import emtvlcapi
import geojson
import logging
import os
import time

logging.basicConfig(level=logging.INFO)

API_URL = "https://api.emtvalencia.es/"  # Asegúrate de que esta URL sea correcta

async def fetch_arrival_times(session, stop):
    """ Función asíncrona para obtener los tiempos de llegada de una parada """
    stop_id = stop['id']
    try:
        async with session.get(f"{API_URL}/getArrivalTimes?stopId={stop_id}") as response:
            if response.status == 200:
                arrival_times = await response.json()
                logging.info(f"API Response for stop {stop_id}: {arrival_times}")

                if arrival_times:
                    next_buses = "; ".join([f"Línea {bus['line']}: {bus['time']} min" for bus in arrival_times])
                else:
                    next_buses = "No disponible"
            else:
                next_buses = "Error"
                
    except Exception as e:
        logging.error(f"Error fetching arrival times for stop {stop_id}: {e}")
        next_buses = "Error"

    return {
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

async def create_geojson():
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

        async with aiohttp.ClientSession() as session:
            tasks = [fetch_arrival_times(session, stop) for stop in stops]
            results = await asyncio.gather(*tasks)

        geojson_data['features'] = results

        geojson_path = "data/stops.geojson"

        # FORZAR QUE EL ARCHIVO SE SOBREESCRIBA
        if os.path.exists(geojson_path):
            os.remove(geojson_path)  # Borra el archivo viejo

        with open(geojson_path, 'w') as f:
            geojson.dump(geojson_data, f)

        logging.info("GeoJSON file updated successfully.")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

async def main():
    while True:
        await create_geojson()
        logging.info("Waiting 30 seconds before next update...")
        await asyncio.sleep(30)

# Ejecutar el loop asíncrono
asyncio.run(main())
