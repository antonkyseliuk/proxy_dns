# proxy_dns
Simple DNS proxy server written in Python (v. 3.*).

For start proxy execute main.py with python3.
Requires no args or options.

For start test execute test.py with python3.
Required args:
- domain
- qtype

Options:
--tcp (sends tcp packets instead udp if enabled)

Example commands:
- python3 google.com A
- python3 google.com A --tcp
