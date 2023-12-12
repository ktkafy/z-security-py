#!/usr/bin/env python
import scapy.all as scapy

def scan(ip):
    #simple way to just use the arping functionality of scapyway to just send arp request across the network
    #scapy.arping(ip)
    
    #making arp packet using scapy
    #arpRequest = scapy.ARP()
    arpRequest = scapy.ARP(pdst=ip) #added to get data of pdst directly and avoiding adding another instance for the variable
    
    #setting IP value for our arp packet to replace default value of 0.0.0.0
    #arpRequest.pdst = ip #we can use it like this arpRequest = scapy.ARP(pdst=ip)
    
    #to display the properties available in this scapy.ARP function
    #scapy.ls(scapy.ARP())
    print(arpRequest.summary())

def scan_2_send_2_boradcast_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    
    #send and receive packets with modified Ether layer so we use scapy.srp()
    #the function gives us two lists as answered and unaswered response
    #answered, unaswered = scapy.srp(arp_request_broadcast, timeout=1)
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0] #getting only first response list
    #print(answered_list.summary())
    
    print("IP\t\t\tMAC Address\n------------------------------------------")
    
    for element in answered_list:
        print(element[1].psrc + "\t\t" + element[1].hwsrc)
        print("------------------------------------------")
    
    #print(arp_request_broadcast.summary()) #show summary of our packet
    #arp_request_broadcast.show() #show details about out packet
    
    #to get available fields for scapy.Ether
    #scapy.ls(scapy.Ether())
   

#scan("10.0.2.1/24")
scan_2_send_2_boradcast_mac("10.0.2.0/24")