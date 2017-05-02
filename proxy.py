from dnslib import DNSRecord, RCODE, QTYPE, RR
from dnslib.server import DNSHandler, BaseResolver
from struct import pack, unpack
from socket import socket, AF_INET, SOCK_STREAM, SOCK_DGRAM
from utils import is_blacked


class UnresolvedDNSHandler(DNSHandler):

    def get_reply(self, data):
        addr = self.server.resolver.addr
        port = self.server.resolver.port

        request = DNSRecord.parse(data)
        self.server.logger.log_request(self, request)
        for question in request.questions:
            if is_blacked(question.qname, self.server.resolver.blacklist):
                reply = request.reply()
                #reply.add_answer(*RR.fromZone('{} IN TXT {}'.format(question.qname, self.server.resolver.answ)))
                reply.header.rcode = getattr(RCODE, 'NXDOMAIN')
                return reply.pack()

        if self.protocol == 'tcp':
            response = self._send_data(pack('!H', len(data)) + data)[2:]
        else:
            response = self._send_data(data)

        reply = DNSRecord.parse(response)
        self.server.logger.log_reply(self, reply)

        return response

    def _send_data(self, data):
        addr = self.server.resolver.addr
        port = self.server.resolver.port

        if self.protocol == 'tcp':
            sock = socket(AF_INET, SOCK_STREAM)
            sock.connect((addr, port))
            sock.sendall(data)
            response = sock.recv(4096)
            data_length = unpack('!H', bytes(response[:2]))[0]
            while len(response) - 2 < data_length:
                response += sock.recv(4096)
        else:
            sock = socket(AF_INET, SOCK_DGRAM)
            sock.sendto(data,(addr, port))
            response = sock.recv(4096)

        sock.close()

        return response


class Resolver(BaseResolver):

    def __init__(self, addr, port, answ, blacklist):
        self.addr = addr
        self.port = port
        self.answ = answ
        self.blacklist = blacklist