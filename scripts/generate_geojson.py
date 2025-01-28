import emtvlcapi
import geojson

# Definir las coordenadas de Valencia y dividirla en zonas más pequeñas
lat_min = 39.39  # Latitud mínima
lat_max = 39.54  # Latitud máxima
lon_min = -0.45  # Longitud mínima
lon_max = -0.35  # Longitud máxima

# Definir el número de pasos para dividir la ciudad en cuadrantes más pequeños
steps_lat = 5  # Número de zonas en latitud (aquí dividimos en 5 partes)
steps_lon = 5  # Número de zonas en longitud (aquí dividimos en 5 partes)

# Calcular el tamaño de cada zona
lat_step = (lat_max - lat_min) / steps_lat
lon_step = (lon_max - lon_min) / steps_lon

# Función para dividir la ciudad en zonas más pequeñas y obtener las paradas
def divide_and_get_stops():
    all_stops = []  # Lista para almacenar todas las paradas
    for i in range(steps_lat):
        for j in range(steps_lon):
            lat1 = lat_min + i * lat_step  # Latitud inferior de la zona
            lon1 = lon_min + j * lon_step  # Longitud inferior de la zona
            lat2 = lat_min + (i + 1) * lat_step  # Latitud superior de la zona
            lon2 = lon_min + (j + 1) * lon_step  # Longitud superior de la zona
            
            # Imprimir las coordenadas de la zona que se está procesando
            print(f"Fetching stops in area: ({lat1}, {lon1}) to ({lat2}, {lon2})")
            
            # Obtener las paradas dentro del área de la zona
            stops = emtvlcapi.get_stops_in_extent(lat1, lon1, lat2, lon2)
            
            # Agregar las paradas obtenidas a la lista general
            all_stops.extend(stops)
    
    return all_stops

# Llamar a la función para obtener todas las paradas
stops = divide_and_get_stops()

# Generar el archivo GeoJSON con los datos obtenidos
with open("data/stops.geojson", "w") as geojson_file:
    geojson.dump(stops, geojson_file)

print("GeoJSON generado exitosamente con todas las paradas de Valencia.")
