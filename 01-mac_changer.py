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

def change_mac(interface, new_mac):
    print("[+] changing mac address for {} with {}".format(interface, new_mac))

    subprocess.call("ifconfig {} down".format(interface),shell=True)
    subprocess.call("ifconfig {} hw ether {}".format(interface, new_mac),shell=True)
    subprocess.call("ifconfig {} up".format(interface), shell=True)

def get_arguments():
    #get all necessary data from user in arguments
    parser = optparse.OptionParser()

    #interface
    parser.add_option("-i", "--interface", dest="interface", help="interface to change its MAC address") #here we say user either can use -i or --interface

    #mac address
    parser.add_option("-m", "--mac", dest="new_mac", help="new MAC address") #here we say user either can use -i or --interface

    #we use return so that the parsed arguments are available through the program
    #return parser.parse_args() #commented due to filter out those scenarios in which user has not entered value for the arguments
    
    #see if user has entered a value for arguments
    (options,arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[+] please specify your desired interface. use --help to see argument's name")
    elif not options.new_mac:
        parser.error("[+] please specify your desired MAC address. use --help to see argument's name")
    return options

"""
#to capture these variables passed for the program, we're gonna take wathever parser gets
#this is done when we use tradiotional way and not using function
(options, arguments) = parser.parse_args()
as we are using return inside the function, we now may use the code like below to get result of parser.parse_args()
"""
#when we were using without filtering for arguments:
(options,arguments) = get_arguments()

#use only options when we have filtered out those which have all neccessary arguments
options = get_arguments()

"""
take those options in action; when using function we don't need to announce them
interface = options.interface
new_mac = options.new_mac
"""

change_mac(options.interface,options.new_mac)