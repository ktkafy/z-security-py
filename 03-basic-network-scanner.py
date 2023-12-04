#!/usr/bin/env python
import scapy.all as scapy

def scan(ip):
    #simple way to just use the arping functionality of scapyway to just send arp request across the network
    #scapy.arping(ip)
    
    #making arp packet using scapy
    arpRequest = scapy.ARP()
    arpRequest = scapy.ARP(pdst=ip) #added to get data of pdst directly and avoiding adding another instance for the variable
    
    #setting IP value for our arp packet to replace default value of 0.0.0.0
    #arpRequest.pdst = ip #we can use it like this arpRequest = scapy.ARP(pdst=ip)
    
    #to display the properties available in this scapy.ARP function
    #scapy.ls(scapy.ARP())
    print(arpRequest.summary())

scan("10.0.2.1/24")