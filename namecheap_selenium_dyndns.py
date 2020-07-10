import os
from time import sleep
from subprocess import check_output

from dotenv import load_dotenv

from NamecheapIpChanger import NamecheapIpChanger
from ExternalIp import ExternalIp

load_dotenv()

class DomainNotFoundException(Exception):
    pass

def get_current_ip_dns():
    #TODO disable output from nslookup
    output = check_output(['nslookup', os.getenv('NAMECHEAP_DOMAIN_NAME'), '8.8.8.8'])
    output = output.decode('utf-8')
    print(output)
    ip = None
    lines = output.split('\n')
    for i, line in enumerate(lines):
        if line.find('Name:') == 0:
            ip_line = lines[i+1]
            ip = [x for x in ip_line.split(' ') if x != ''][1]
            break
    if ip == None:
        raise DomainNotFoundException('Domain name is not found on 8.8.8.8 dns server')
    return ip

def main():
    CHECK_PERIOD = 15 * 60
    external_ip = None
    while True:
        try:
            current_ip = get_current_ip_dns()
            external_ip = str(ExternalIp)
        except (DomainNotFoundException, ExternalIp.ExternalIpNotFoundError) as e:
            print(e)
            sleep(60)
            continue
        if current_ip != external_ip:
            ip_changer = NamecheapIpChanger()
            ip_changer.change_ip()
            ip_changer.cleanup()
            sleep(10 * 60)
        sleep(CHECK_PERIOD)



if __name__ == "__main__":
    main()
