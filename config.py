import logging


def get_server_ip():
    file = "configs/network.conf"
    ip = "127.0.0.1"
    try:
        with open(file) as f:
            ip = f.readline().strip()
    except OSError:
        logging.warning(f"couldn't read file {file} - using IP {ip}")
    return ip

# TODO: use format like yaml for config
