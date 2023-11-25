import subprocess
interface = "eth0"
new_mac = "00:11:22:33:44:55"

print("[+] changing mac address for {} with {}".format(interface, new_mac))

#setting with variables
subprocess.call("ifconfig {} down".format(interface),shell=True)
subprocess.call("ifconfig {} hw ether {}".format(interface, new_mac),shell=True)
subprocess.call("ifconfig {} up".format(interface), shell=True)