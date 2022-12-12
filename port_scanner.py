
import re
import socket
import common_ports
import argparse


def is_valid_ip(hostname):
    # First, we check if the hostname is an IP address
    # If it is, we check if the IP address is valid
    if len(hostname.split('.')) == 4:
        # The hostname is an IP address, so we check if it is valid
        for octet in hostname.split('.'):
            try:
                octet = int(octet)
            except ValueError:
                # If the octet cannot be converted to an integer, it is not valid
                return False

            if not 0 <= octet <= 255:
                # If the octet is not in the range 0-255, it is not valid
                return False

        # If all checks pass, the IP address is valid
        return True

    # If the hostname is not an IP address, we perform a DNS lookup
    try:
        # If the DNS lookup succeeds, the hostname is valid
        socket.gethostbyname(hostname)
        return True
    except socket.error:
        # If the DNS lookup fails, the hostname is not valid
        return False


def get_open_ports(target, port_range, verbose=False):
    open_ports = []
    result = ""
    valid = False

    # create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    if is_valid_ip(target):
        valid = True
    else:
        # check if target is hostname or an address
        if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', target):
            return "Error: Invalid IP address"
        elif re.match(r'^[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', target):
            return "Error: Invalid hostname"
        else:
            return "Error: Invalid hostname or IP address"

    if valid:
        # Use a for loop to iterate over the range of ports
        for port in range(port_range[0], port_range[-1]+1):
            # Use the socket module to create a connection to the target
            # on the current port in the loop
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            connection = s.connect_ex((target, port))

            # If the connection returns a 0, it means the port is open
            if connection == 0:
                # Add the open port to the list of open ports
                open_ports.append(port)

            # close the socket
            s.close()

    if verbose:
        # get the hostname
        try:
            hostname = socket.gethostbyaddr(target)[0]
        except:
            hostname = None

        # get url
        try:
            target = socket.gethostbyname(hostname)
        except:
            target = target

        # print the results
        if hostname is not None:
            result += f"Open ports for {hostname} ({target}):\n"
        else:
            result += f"Open ports for {target}:\n"

        result += "PORT\tSERVICE\n"
        for port in open_ports:
            result += f"{port}\t{common_ports.ports_and_services[port]}\n"

        return result
    else:
        return open_ports


def main():
    # Create the parser
    parser = argparse.ArgumentParser(description="Port scanner")

    # Add the arguments
    parser.add_argument("target", help="the target to scan")
    parser.add_argument("port_range", help="the range of ports to scan")
    parser.add_argument("-v", "--verbose",help="enable verbose output", action="store_true")

    # Parse the arguments
    args = parser.parse_args()

    # convert port_range to a list of integersp
    args.port_range = list(map(int, args.port_range.split('-')))

    # Run the port scanner with the given arguments
    print(get_open_ports(args.target, args.port_range, args.verbose))


if __name__ == "__main__":
    main()
