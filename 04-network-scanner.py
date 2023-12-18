#!/usr/bin/env python
import scapy.all as scapy
import argparse

def getArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="Target IP/IP Range.")
    options = parser.parse_args()
    return options

def scanWithBroadcastARP(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    
    #the function gives us two lists as answered and unaswered response
    #answered, unaswered = scapy.srp(arp_request_broadcast, timeout=1)
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0] #getting only first response list
        
    clientList = []
    for element in answered_list:
        #in a tradition fashion just printing out
        #print(element[1].psrc + "\t\t" + element[1].hwsrc)
        
        #use dictionary and list together
        clientDictionary = {"ip": element[1].psrc, "mac":element[1].hwsrc}
        clientList.append(clientDictionary)
        
    return(clientList)
    #print(arp_request_broadcast.summary()) #show summary of our packet
    #arp_request_broadcast.show() #show details about out packet
    
    #to get available fields for scapy.Ether
    #scapy.ls(scapy.Ether())

def printResult(reusltsList):
    print("IP\t\t\tMAC Address\n------------------------------------------")
    for client in reusltsList:
        print(client["ip"] + "\t\t" + client["mac"])

#captures the value of the list that's being returned in function in a variable
options = getArguments()
scanResult = scanWithBroadcastARP(options.target)

printResult(scanResult)