import FrontendCore
import BackendCore

def main():
    print("NetCap 0.1 started...")
    BackendCore.get_network_connections()
    window = FrontendCore.Frontend("NetCap")
    window.guiMainLoop()






if __name__ == '__main__':
    main()


