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
        return "<no IP address>"
