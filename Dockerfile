FROM selenium/standalone-chrome

USER root
RUN apt update && apt install -y xvfb python3-pip dnsutils
RUN python3 -m pip install selenium

USER seluser

WORKDIR /home/seluser

COPY . /home/seluser

RUN python3 -m pip install -r requirements.txt

CMD ["python3", "namecheap_selenium_dyndns.py"]
