import emtvlcapi
import json

# Función para obtener los tiempos de autobús para una parada específica
def get_bus_times_for_stop(stop_id):
    try:
        # Obtener los tiempos de autobús para una parada específica
        bus_times = emtvlcapi.get_bus_times(stop_id)
        return bus_times
    except Exception as e:
        print(f"Error al obtener los tiempos de autobús para la parada {stop_id}: {e}")
        return []

# Función para obtener todas las paradas en la ciudad de Valencia (sin dividir en subáreas)
def get_all_stops():
    # Definir las coordenadas de Valencia en su totalidad
    lat1, lon1 = 39.360000, -0.500000  # Coordenadas aproximadas del suroeste de Valencia
    lat2, lon2 = 39.550000, -0.300000  # Coordenadas aproximadas del noreste de Valencia

    # Obtener las paradas dentro de este rectángulo
    stops = emtvlcapi.get_stops_in_extent(lat1, lon1, lat2, lon2)

    # Si no se encuentran paradas, devolver un GeoJSON vacío
    if not stops:
        return {
            "type": "FeatureCollection",
            "features": []
        }

    # Crear el GeoJSON
    geojson = {
        "type": "FeatureCollection",
        "features": []
    }

    # Convertir las paradas a formato GeoJSON
    for stop in stops:
        stop_id = stop['stopId']
        
        # Obtener los tiempos de autobús para esta parada
        bus_times = get_bus_times_for_stop(stop_id)

        # Preparar la lista de horarios de autobús
        bus_times_info = []
        for time in bus_times:
            bus_info = {
                "line": time.get("linea", ""),
                "destination": time.get("destino", ""),
                "minutes_left": time.get("minutos", ""),
                "arrival_time": time.get("horaLlegada", "")
            }
            bus_times_info.append(bus_info)

        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [float(stop['lon']), float(stop['lat'])]
            },
            "properties": {
                "name": stop['name'],
                "stopId": stop['stopId'],
                "routes": ", ".join([f"{route['SN']} - {route['LN']}" for route in stop['routes']]),
                "location": stop['ubica'],
                "bus_times": bus_times_info  # Añadir los tiempos de los autobuses
            }
        }
        geojson["features"].append(feature)

    return geojson

# Guardar el archivo GeoJSON con todas las paradas y sus tiempos de autobús
if __name__ == "__main__":
    all_stops_geojson = get_all_stops()  # Obtener todas las paradas en formato GeoJSON
    with open("data/stops_with_bus_times.geojson", "w") as f:
        json.dump(all_stops_geojson, f, indent=4)  # Guardar el GeoJSON en un archivo
    print("Archivo GeoJSON generado: data/stops_with_bus_times.geojson")
