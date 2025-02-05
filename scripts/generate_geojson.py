import emtvlcapi
import geojson
import logging
import asyncio
import aiohttp

logging.basicConfig(level=logging.INFO)

# Coordenadas del área de búsqueda
LAT1, LON1, LAT2, LON2 = 39.39, -0.45, 39.42, -0.43  

async def fetch_arrival_times(session, stop_id):
    """ Obtiene los tiempos de llegada de los buses para una parada """
    try:
        async with session.get(f"https://api.emtvalencia.es/arrival_times/{stop_id}") as response:
            if response.status == 204:
                return "No disponible"  # Manejar respuesta vacía
            
            data = await response.json()
            if data:
                return "; ".join([f"Línea {bus['line']}: {bus['time']} min" for bus in data])
            return "No disponible"
    except Exception as e:
        logging.error(f"Error al obtener tiempos para la parada {stop_id}: {e}")
        return "Error"

async def create_geojson():
    """ Genera el archivo GeoJSON con información en paralelo """
    logging.info(f"Obteniendo paradas en el área: ({LAT1}, {LON1}) a ({LAT2}, {LON2})")
    
    try:
        stops = emtvlcapi.get_stops_in_extent(LAT1, LON1, LAT2, LON2)

        if not stops:
            logging.warning("⚠️ No se encontraron paradas en esta área. Prueba con otras coordenadas.")
            return

        geojson_data = {
            "type": "FeatureCollection",
            "features": []
        }

        async with aiohttp.ClientSession() as session:
            tasks = [fetch_arrival_times(session, stop['id']) for stop in stops]
            arrival_results = await asyncio.gather(*tasks)

        for stop, next_buses in zip(stops, arrival_results):
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [stop['lon'], stop['lat']]
                },
                "properties": {
                    "name": stop['name'],
                    "id": stop['id'],
                    "next_buses": next_buses
                }
            }
            geojson_data['features'].append(feature)

        with open('data/stops.geojson', 'w') as f:
            geojson.dump(geojson_data, f)

        logging.info("✅ GeoJSON generado con éxito.")

    except Exception as e:
        logging.error(f"❌ Error general: {e}")

if __name__ == "__main__":
    asyncio.run(create_geojson())
