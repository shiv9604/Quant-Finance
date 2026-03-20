''' 
In this programme for security reasons to avoid clicks on the fraud sites Ip defanger is used...
192.168.1.2 the . is replaces with [.] in the defanged ip..
'''

def defanged(ip):
    # ip = input("Enter the Ip adress : ")
    return ip.replace(".","[.]")

ip = input("Enter the Ip : ")
print("Your defanged ip adress is :",defanged(ip))