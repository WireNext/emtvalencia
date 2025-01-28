import emtvlcapi
import json

def create_geojson(lat1, lon1, lat2, lon2):
    stops = emtvlcapi.get_stops_in_extent(lat1, lon1, lat2, lon2)
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

def fetch_all_stops():
    # Dividir el área en 4 subáreas (ajustar según sea necesario)
    subareas = [
        (39.471964, -0.394641, 39.473000, -0.399000),
        (39.473000, -0.399000, 39.474714, -0.405906),
        (39.471964, -0.399000, 39.473000, -0.405906),
        (39.473000, -0.405906, 39.474714, -0.411000),
    ]
    
    geojson = {
        "type": "FeatureCollection",
        "features": []
    }
    
    for lat1, lon1, lat2, lon2 in subareas:
        print(f"Fetching stops in area: ({lat1}, {lon1}) to ({lat2}, {lon2})")
        # Obtener las paradas en la subárea
        stops = create_geojson(lat1, lon1, lat2, lon2)
        geojson["features"].extend(stops["features"])  # Agregar las paradas a la colección

    return geojson

# Generar y guardar el archivo GeoJSON
if __name__ == "__main__":
    all_stops_geojson = fetch_all_stops()
    with open("data/stops.geojson", "w") as f:
        json.dump(all_stops_geojson, f, indent=4)
    print("Archivo GeoJSON generado: data/stops.geojson")
