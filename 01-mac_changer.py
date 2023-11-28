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

#interface
parser.add_option("-i", "--interface", dest="interface", help="interface to change its MAC address") #here we say user either can use -i or --interface

#mac address
parser.add_option("-m", "--mac", dest="new_mac", help="new MAC address") #here we say user either can use -i or --interface

#to capture these variables, we're gonna take wathever parser gets
(options, arguments) = parser.parse_args()

#take those options in action
interface = options.interface
new_mac = options.new_mac

print("[+] changing mac address for {} with {}".format(interface, new_mac))

subprocess.call("ifconfig {} down".format(interface),shell=True)
subprocess.call("ifconfig {} hw ether {}".format(interface, new_mac),shell=True)
subprocess.call("ifconfig {} up".format(interface), shell=True)