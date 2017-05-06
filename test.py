"""
    Simple test script for proxy_dns.
    Required args:
    - domain
    - qtype
    Options:
    --tcp (sends tcp packets instead udp if enabled)
    
    Example command:
    "python3 google.com A" or "python3 google.com A --tcp" 
"""


from argparse import ArgumentParser
from dnslib import DNSRecord, DNSQuestion, QTYPE, RCODE
from utils import parse_settings, is_blacked


if __name__ == '__main__':
    arg_p = ArgumentParser(description="proxy_dns test")

    arg_p.add_argument('--tcp', action='store_true', default=False)
    arg_p.add_argument('domain')
    arg_p.add_argument('qtype', default='A')

    args = arg_p.parse_args()

    settings = parse_settings('settings.ini')
    blacklist = settings['BLACKLIST'].keys()
    black_code = settings['COMMON']['black_code']
    addr, port = settings['COMMON']['proxy'].split(':')

    question = DNSQuestion(args.domain, getattr(QTYPE, args.qtype))
    request = DNSRecord(q=question)
    response = request.send(addr, int(port), tcp=args.tcp)
    reply = DNSRecord.parse(response)

    blacked_flag = is_blacked(question.qname, blacklist)
    rcode_flag = reply.header.rcode == getattr(RCODE, black_code)

    if blacked_flag:
        print('--- {} is in the blacklist.'.format(question.qname))
        if rcode_flag:
            print('--- and reply has right rcode.')
            print('---- VICTORY :)')
        else:
            print('--- but reply has wrong rcode.')
            print('---- DEFEAT :(')
    else:
        print('--- {} is not in the blacklist'.format(question.qname))

