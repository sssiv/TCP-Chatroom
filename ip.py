import netifaces as ni

# Gets local machine address and holds Host IP and Port
class IPv4:
    def __init__(self):
        self.host = self.local_ip()  # Local Host 
        self.port = 12345            # Port isn't reserved so I chose it

    # Finds your IP by scanning your NIC
    def local_ip(self):
        # Get all network interfaces (keys from the interfaces dictionary)
        interfaces = ni.interfaces()
        
        # itr's through network interfaces
        for interface in interfaces:
            # Get all addresses for each interface
            addrs = ni.ifaddresses(interface)

            # Look for IPv4 addresses
            if ni.AF_INET in addrs:
                # Get the first IPv4 address
                # The first IP the system responds with is usually the main IP
                ipv4_info = addrs[ni.AF_INET][0]

                # the IP is found in the addr column
                address = ipv4_info['addr']
                
                # Check if the address is on the same subnet as your known IP
                if address.startswith('192.168.1.'):
                    return address
        # Fallback to localhost
        return '127.0.0.1'  