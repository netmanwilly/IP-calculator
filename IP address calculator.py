#objective:
#calculate the following:
#   Network Address
#   Host Address Range
#   Broadcast address
#   Next Network Address
#write results into a file
#notes
#need to seperate functions a little more so that testing can be done in a more lego-like fashion
#steps for code
#   1. divide IP and subnet mask
#   2. Check if subnet is correct in either CIDR notation or dotted decimal
#   3. convert both IP and subnet mask to binary
#   4. figure out network address based on binary
#   5. find out the range of usable IPs range and broadcast address
#   6. Convert and store information back into a file
def subnet_mask(ip: str):
    ip_split = ip.split(" ")

    #checks if subnet mask was entered as an prefix
    if "/" in ip_split[1]:
        subnet_mask_converted = int(ip_split[1].replace("/", ""))
        if subnet_mask_converted < 0 or subnet_mask_converted > 32:
            raise ValueError("Subnet mask is incorrect")
        subnet_list = []
        while subnet_mask_converted > 0:
            binary = [128, 64, 32, 16, 8, 4, 2, 1]
            binary_digit = 0
            if subnet_mask_converted >= 8:
                binary_range = 8
            else:
                binary_range = subnet_mask_converted

            for x in range(binary_range):
                binary_digit += binary[x]
                subnet_mask_converted -= 1

            subnet_list.append(str(binary_digit))
            
        while len(subnet_list) < 4:
            subnet_list.append("0")
        subnet_mask = (".".join(subnet_list))

        return subnet_mask
                    
    else:
        subnet = ip_split[1].split(".")
        for x in subnet:
            if int(x) < 0 or int(x) > 255:
                raise ValueError("Subnet Mask is incorrect")
            
    
        return ip_split[1]
        


#converts IP address and subnet to binary
def ip_subnet_binary(ip: str):
    #converts  and returns subnet to dotted decimal
    subnet = subnet_mask(ip)
    #splits input to divide ip and subnet
    ip_address = ip.split(" ")[0]
    #splits each by dot
    ip_split = ip_address.split(".")
    subnet_split = subnet.split(".")
    #converts dotted decimal to binary
    ip_binary = []
    subnet_binary = []
    for x in ip_split:
        ip_binary.append(to_binary(int(x)))
    for x in subnet_split:
        subnet_binary.append(to_binary(int(x)))

    return (ip_binary, subnet_binary)
        
#finds the network address
def network_address(ip: str):
    binary = ip_subnet_binary(ip)
    #split IP and subnet binary list
    ip = binary[0]
    subnet = binary[1]
    network_add = []
    network_add_converted = []
    #print(ip)
    #print(subnet)
    #compares each digit in binary list to calculate network address
    for i in range(4):
        network = ""
        for x in range(8):
            if subnet[i][x] == "1":
                network += ip[i][x]
            else:
                network += "0"
            
        network_add.append(network)


    #print(network_add)

    return (network_add, subnet)

def ip_range(ip: str):
    ip = network_address(ip)
    #lists of addresses in binary notation
    network = ip[0]
    subnet = ip[1]
    broadcast = []
    
    #calculate broadcast address using binary 
    for i in range(4):
        broadcast_octet = ""
        for x in range(8):
            if subnet[i][x] == "1":
                broadcast_octet += network[i][x]
            elif subnet[i][x] == "0":
                broadcast_octet += "1"
        
        broadcast.append(broadcast_octet)

    #new list to store dotted decimal notation
    converted = []
    first = []
    last = []
    broadcast_address = []
    #loops to convert binary back to decimal dotted notation
    for x in network:
        converted.append(to_dotted_decimal(x))
    for x in network:
        first.append(to_dotted_decimal(x))
    for x in broadcast:
        last.append(to_dotted_decimal(x)) 
    for x in broadcast:
        broadcast_address.append(to_dotted_decimal(x))
    #add one to network address to get first usable
    first[-1] += 1
    #subtract one from broadcast to get last usbale
    last[-1] -= 1

    return (converted, first, last, broadcast_address, cidr_notation(".".join(subnet)))

def final_print(ip: str):
    ip_information = ip_range(ip)
    #seperate each list into a unique list
    network = ip_information[0]
    first_usuable = ip_information[1]
    last_usable = ip_information[2]
    broadcast = ip_information[3]
    cidr = [ip_information[4]]
    #converts list into strings
    network_address = [str(x) for x in network]
    first_usable_address = [str(x) for x in first_usuable]
    last_usable_address = [str(x) for x in last_usable]
    broadcast_address = [str(x) for x in broadcast]

    #combines list into ip address
    network_address_result = ".".join(network_address)
    first_usable_result = ".".join(first_usable_address)
    last_usable_result = ".".join(last_usable_address)
    broadcast_result = ".".join(broadcast_address)

    with open("Result", "a") as result:

        result.write("Results: \n")
        result.write(f"Network Address: {network_address_result} {cidr} \n")
        result.write(f"First Usable Address: {first_usable_result} \n")
        result.write(f"Last Usable Address: {last_usable_result} \n")
        result.write(f"Broadcast Address: {broadcast_result} \n")
        result.write(f"\n")
    
    print("Results store in file.")


def cidr_notation(subnet_mask: str):
    subnet = subnet_mask.count("1")
    return f"/{subnet}"

def to_binary(number: int):
    binary = [128, 64, 32, 16, 8, 4, 2, 1]
    conversion = ""
    i = 0
    while number > 0:
        if number >= binary[i]:
            conversion += "1"
            number -= binary[i]
        else:
            conversion += "0"
        i += 1
    if len(conversion) < 8:
        conversion += "0" * (8 - len(conversion))

    
    return conversion

def to_dotted_decimal(number: str):
    binary = [128, 64, 32, 16, 8, 4, 2, 1]
    conversion = 0
    for x in range(8):
        if number[x] == "1":
            conversion += binary[x]
    
    return conversion


def main():
    user = str(input("Please type in an IP address and Subnet Mask: "))
    final_print(user)

if __name__ == "__main__":
    #subnet = print(final_print("192.168.1.102 /12"))
    #subnet = print(final_print("192.168.1.62 /16"))
    #subnet = print(final_print("192.168.1.82 /20"))
    #subnet = print(final_print("192.168.1.65 /26"))
    #subnet = print(final_print("192.168.1.2 /17"))
    #subnet = print(final_print("192.168.1.37 /8"))
    main()
