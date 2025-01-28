import emtvlcapi
import json

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

# Guardar el archivo GeoJSON con todas las paradas de Valencia
if __name__ == "__main__":
    all_stops_geojson = get_all_stops()  # Obtener todas las paradas en formato GeoJSON
    with open("data/stops.geojson", "w") as f:
        json.dump(all_stops_geojson, f, indent=4)  # Guardar el GeoJSON en un archivo
    print("Archivo GeoJSON generado: data/stops.geojson")
