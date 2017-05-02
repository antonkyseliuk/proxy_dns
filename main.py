from time import sleep
from utils import parse_settings
from proxy import Resolver, UnresolvedDNSHandler
from dnslib.server import DNSServer, DNSLogger


settings = parse_settings('settings.ini')
addr, port = settings['COMMON']['upstream'].split(':')

resolver = Resolver(addr,
                    int(port),
                    settings['COMMON']['answer'],
                    settings['BLACKLIST'])
handler = UnresolvedDNSHandler
logger = DNSLogger("request,reply,truncated,error", False)
print("Starting DNS proxy")
udp_server = DNSServer(resolver, handler=handler, logger=logger)
udp_server.start_thread()

tcp_server = DNSServer(resolver, tcp=True, handler=handler)
tcp_server.start_thread()

while udp_server.isAlive():
    sleep(1)
