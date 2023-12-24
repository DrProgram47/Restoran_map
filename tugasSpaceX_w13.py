from math import radians, cos, sin, asin, sqrt
import requests

def distance(lat1, lat2, lon1, lon2):
     
    # Modul matematika bermuat fungsi bernama
    # radian yang mengonversi dari derajat ke radian.
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
      
    # formula Haversine
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
 
    c = 2 * asin(sqrt(a))
    
    # Radius bumi dalam kilometer. Gunakan 3956 untuk mil
    r = 6371
      
    # kalkulasikan hasil
    return(c * r)

def get_coordinate(address):
    access_token = 'pk.eyJ1IjoiZmFkaGlsbHgiLCJhIjoiY2w4eTloOGM1MDZ0MjN2bGcwY3k5Y3pjeSJ9.X-eiCzScHwEqjoXJUF6AXg'
    coor_url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{address}.json?access_token={access_token}"
    coor_response =  requests.get(coor_url)
    data = coor_response.json()
    # Mengambil koordinat dari hasil geocoding
    coordinates = data['features'][0]['geometry']['coordinates']
    return {'lat': coordinates[1], 'lon': coordinates[0]}

# Mengambil 20 data peluncuran terakhir
spacex_api = 'https://api.spacexdata.com/v4/launches'
response = requests.get(spacex_api)
launches = response.json()[:20]

for launch in launches:
    # Mendapatkan nama launchpad
    launchpad_id = launch['launchpad']
    launchpad_url = f'https://api.spacexdata.com/v4/launchpads/{launchpad_id}'
    launchpad_response = requests.get(launchpad_url)
    launchpad_data = launchpad_response.json()
    launchpad_name = launchpad_data['name']

    # Mendapatkan koordinat dari alamat launchpad menggunakan Mapbox Geocoding API
    launchpad_coordinates = get_coordinate(launchpad_name)
    
    spacex_coordinates = {'lon': launchpad_data['longitude'], 'lat': launchpad_data['latitude']}

    # Jarak antara dua titik geografis
    launch_distance = distance(launchpad_coordinates['lat'], spacex_coordinates['lat'],
                               launchpad_coordinates['lon'], spacex_coordinates['lon'])
    
    print(f'{launch["date_utc"]}, {launchpad_name}, {launch_distance:.2f}')