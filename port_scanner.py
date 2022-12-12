
import re
import socket
import common_ports
import argparse
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

"""
TODO: Add support for using UDP instead of TCP   
      You can do this by passing socket.SOCK_DGRAM as the second parameter to 
      the socket.socket method, instead of socket.SOCK_STREAM
      s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      
TODO: Add support for IPv6 addresses
      You can do this by passing socket.AF_INET6 as the first parameter to
      the socket.socket method
      
TODO: Add support for using a file containing a list of hosts
      new argument -i <file_name>
      
TODO: Generate requirements.txt file
"""

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


def scan_port(port, target, open_ports, lock):
    # Use the socket module to create a connection to the target
    # on the specified port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection = s.connect_ex((target, port))

    # If the connection returns a 0, it means the port is open
    if connection == 0:
        # Acquire the lock before modifying the open_ports list
        with lock:
            open_ports.append(port)

    # close the socket
    s.close()


def get_open_ports(target, port_range, verbose=False, threads=10):
    open_ports = []
    result = ""
    valid = False

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
        # Create a thread pool with a specified number of threads
        pool = ThreadPoolExecutor(max_workers=threads)
        print(f"Scanning {target} for open ports using {threads} threads...")

        # Create a lock for synchronizing access to the list of open ports
        lock = Lock()

        # Iterate over the ports in the range
        for port in range(port_range[0], port_range[-1]+1):
            # Use the thread pool to execute the scan task on a separate thread
            pool.submit(scan_port, port, target, open_ports, lock)

        # Wait for all the threads in the pool to complete
        pool.shutdown()

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
        return str(open_ports)


def main():
    # Create the parser
    parser = argparse.ArgumentParser(
        description="Simple Port scanner developed in Python")

    # Add the arguments
    parser.add_argument("target", help="the target to scan")
    parser.add_argument("port_range", help="the range of ports to scan")
    parser.add_argument("-o", "--output", help="output file name")
    parser.add_argument(
        "-t", "--threads", help="specify the number of threads", default=10, type=int)
    parser.add_argument("-v", "--verbose",
                        help="enable verbose output", action="store_true")

    # Parse the arguments
    args = parser.parse_args()

    # convert port_range to a list of integers
    args.port_range = list(map(int, args.port_range.split('-')))

    # check if the -o option was used and a file name was given
    if args.output and args.output != "":
        # a file name was given, so write the scan results to the specified file
        with open(args.output, "w") as f:
            f.write(get_open_ports(args.target, args.port_range, args.verbose))
    else:
        # either the -o option was not used, or no file name was given
        # in either case, print the scan results to the console
        print(get_open_ports(args.target, args.port_range, args.verbose, args.threads))


if __name__ == "__main__":
    main()
