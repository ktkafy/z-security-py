import subprocess
import optparse #module to let us use arguments and parse them and use them
#in a fashion mode to get input directly from user
"""interface = input("[+]enter the desired interface: ")
new_mac = input("[+]enter your desired MAC address: ")

print("[+] changing mac address for {} with {}".format(interface, new_mac))

#setting with variables
subprocess.call("ifconfig {} down".format(interface),shell=True)
subprocess.call("ifconfig {} hw ether {}".format(interface, new_mac),shell=True)
subprocess.call("ifconfig {} up".format(interface), shell=True)
"""

#get all necessary data from user in arguments
parser = optparse.OptionParser()
parser.add_option("-i", "--interface", dest="interface") #here we say user either can use -i or --interface
