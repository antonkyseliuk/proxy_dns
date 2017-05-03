from time import sleep
from utils import parse_settings
from proxy import Resolver
from dnslib.server import DNSServer, DNSLogger, DNSHandler


settings = parse_settings('settings.ini')
addr, port = settings['COMMON']['upstream'].split(':')

resolver = Resolver(addr,
                    int(port),
                    settings['COMMON']['black_code'],
                    settings['BLACKLIST'].keys())
logger = DNSLogger("request,reply,truncated,error", False)

udp_server = DNSServer(resolver,
                       handler=DNSHandler,
                       logger=logger)
udp_server.start_thread()

tcp_server = DNSServer(resolver,
                       tcp=True,
                       handler=DNSHandler,
                       logger=logger)
tcp_server.start_thread()

while udp_server.isAlive():
    sleep(1)
