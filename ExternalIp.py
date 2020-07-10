#!/usr/bin/env python3

import urllib3
import json

class ExternalIp:

    class ExternalIpNotFoundError(Exception):
        pass

    CHECK_SERVICES = (
        # URL, decode method
        ('http://ifconfig.me', 'raw'),
        ('http://httpbin.org/ip', 'json'),
        ('http://ip.42.pl/raw', 'raw'),
    )

    def __init__(self):

        http = urllib3.PoolManager()
        decoded_data = None
        for url, decode_method in self.CHECK_SERVICES:
            try:
                r = http.request('GET', url)
            except Exception:
                continue
            if r.status != 200:
                continue
            decoded_data = r.data.decode('utf-8')
            if decode_method == 'json':
                decoded_data = json.loads(decoded_data)['origin']
            break
        if not decoded_data:
            raise ExternalIp.ExternalIpNotFoundError('Unable to get external IP')
        self.ip = decoded_data

    def __str__(self):
        return self.ip

if __name__ == "__main__":
    print(str(ExternalIp()))
    ExternalIp.CHECK_SERVICES = ExternalIp.CHECK_SERVICES[1:]
    print(ExternalIp.CHECK_SERVICES)
    print(str(ExternalIp()))
    ExternalIp.CHECK_SERVICES = ExternalIp.CHECK_SERVICES[1:]
    print(ExternalIp.CHECK_SERVICES)
    print(str(ExternalIp()))
