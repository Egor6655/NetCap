import psutil
import time
import socket



def get_network_connections():
    connections = psutil.net_connections(kind='inet')
    connections_data = []

    for conn in connections:
        try:
            proc = psutil.Process(conn.pid) if conn.pid else None

            fd = conn.fd if conn.fd else -1
            family = conn.family.name if hasattr(conn.family, 'name') else conn.family
            type_ = conn.type.name if hasattr(conn.type, 'name') else conn.type
            laddr = format_address(conn.laddr) if conn.laddr else ""
            raddr = format_address(conn.raddr) if conn.raddr else ""
            status = conn.status

            pid = conn.pid if conn.pid else -1
            process_name = proc.name() if proc else ""
            process_status = proc.status() if proc else ""
            process_cmdline = " ".join(proc.cmdline()) if proc and proc.cmdline() else ""
            process_username = proc.username() if proc else ""

            connection_info = [
                fd,  # int
                family,  # str (e.g., 'AF_INET')
                type_,  # str (e.g., 'SOCK_STREAM')
                laddr,  # str
                raddr,  # str
                status,  # str
                pid,  # int
                process_name,  # str
                process_status,  # str
                process_cmdline,  # str
                process_username  # str
            ]
            connections_data.append(connection_info)

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return connections_data

def format_address(addr):
    return f"{addr.ip}:{addr.port}" if addr.port else addr.ip

def get_network_traffic(interval=1):

    net_start = psutil.net_io_counters()
    bytes_recv_start = net_start.bytes_recv
    bytes_sent_start = net_start.bytes_sent


    time.sleep(interval)

    net_end = psutil.net_io_counters()
    bytes_recv_end = net_end.bytes_recv
    bytes_sent_end = net_end.bytes_sent

    download_speed = (bytes_recv_end - bytes_recv_start) / interval
    upload_speed = (bytes_sent_end - bytes_sent_start) / interval

    return bytes_to_human_readable(download_speed), bytes_to_human_readable(upload_speed)


def bytes_to_human_readable(bytes_value):
    bytes_value /= 1024
    return f"{bytes_value:.2f} "
    #for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
    #    if bytes_value < 1024:
    #        return f"{bytes_value:.2f} {unit}/s"
    #   bytes_value /= 1024
    #return f"{bytes_value:.2f} PB/s"
def isIpValid(address):
    try:
        socket.inet_aton(address)
        return True
    except:
        return False



