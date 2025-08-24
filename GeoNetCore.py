import requests as rq
import BackendCore
import folium
import webbrowser
import os


def getIPLocation():
    data = BackendCore.get_network_connections()
    print(data[4])
    coordinates = {}
    for item in data:
        rawIp = item[4]
        try:

            ip =rawIp.split(":",1)[0]
            print(ip)
            if BackendCore.isIpValid:
                response = rq.get("http://ip-api.com/json/" + ip + "?lang=ru")
                geoData = response.json()
                if response.status_code == 404:
                    print("Oops")
                result = response.json()
                if result["status"] == "fail":
                    pass

                recent_Lat = None
                for key, value in result.items():
                    print(str(key) + "  :  " + str(value))
                    if key == "lat":
                        recent_Lat = value
                    if key == "lon":
                        coordinates[recent_Lat]=value

        except Exception:
            pass
    print(coordinates)
    return coordinates




def setLocationDataToHtml():
    coordinates = getIPLocation()
    print(coordinates)
    GeoIpMap = folium.Map(
        zoom_start=4
    )

    markerGroup = folium.map.FeatureGroup()

    for lat,lon in coordinates.items():
        markerGroup.add_child(
            folium.features.CircleMarker(
                [lat, lon], radius=5,
                color='red', fill_color='White'
            )
        )
    GeoIpMap.add_child(markerGroup)
    GeoIpMap.save("locations.html")
    webbrowser.open('file://' + os.getcwd()+"/locations.html")
