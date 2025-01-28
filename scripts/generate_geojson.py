import emtvalencia
import json

def create_geojson(lat1, lon1, lat2, lon2):
    # Obtener paradas dentro del área especificada
    stops = emtvalencia.get_stops_in_extent(lat1, lon1, lat2, lon2)

    # Formatear los datos en GeoJSON
    geojson = {
        "type": "FeatureCollection",
        "features": []
    }

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


if __name__ == "__main__":
    # Define las esquinas del rectángulo (latitud y longitud)
    lat1, lon1 = 39.471964, -0.394641
    lat2, lon2 = 39.474714, -0.405906

    # Generar GeoJSON
    geojson_data = create_geojson(lat1, lon1, lat2, lon2)

    # Guardar en un archivo
    with open("data/stops.geojson", "w") as f:
        json.dump(geojson_data, f, indent=4)

    print("Archivo GeoJSON generado: data/stops.geojson")
