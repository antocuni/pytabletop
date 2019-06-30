from kivy.utils import platform

def int_to_ip(ipnum):
    oc1 = int(ipnum / 16777216) % 256
    oc2 = int(ipnum / 65536) % 256
    oc3 = int(ipnum / 256) % 256
    oc4 = int(ipnum) % 256
    return '%d.%d.%d.%d' %(oc4,oc3,oc2,oc1)

if platform == 'android':
    def getIP():
        from jnius import autoclass
        NetworkInterface = autoclass("java.net.NetworkInterface")
        en = NetworkInterface.getNetworkInterfaces()
        while en.hasMoreElements():
            intf = en.nextElement()
            enumIpAddr = intf.getInetAddresses()
            while enumIpAddr.hasMoreElements():
                inetAddress = enumIpAddr.nextElement()
                address = inetAddress.getHostAddress()
                if not inetAddress.isLoopbackAddress() and len(address) < 18:
                    return address
        return "<no IP address>"

else:
    def getIP():
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except:
            IP = "<no IP address>"
        finally:
            s.close()
        return IP
