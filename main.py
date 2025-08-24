import FrontendCore
import BackendCore
import folium

import GeoNetCore


def main():

    print("NetCap 0.1 started...")
    BackendCore.get_network_connections()
    window = FrontendCore.Frontend("NetCap")
    window.guiMainLoop()
    rMap = folium.Map()
    rMap.save("footprint.html")

    #only for tests
    #GeoNetCore.setLocationToHtml()






if __name__ == '__main__':
    main()


