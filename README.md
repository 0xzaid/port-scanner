# Port Scanner

Port Scanner project using Python for [FreeCodeCamp](https://www.freecodecamp.org/learn/information-security/information-security-projects/port-scanner)
I have improved it by making it usable through a terminal, and I plan to add more features.

# Usage

To use port_scanner.py, open a terminal or command prompt and navigate to the directory where the program is saved. Then, run the following command:
```
python port_scanner.py <target> <port_range> -v
```

Replace <target>, <port_range>, with the desired values for each argument. For example, to scan the host "example.com" for open ports in the range 1-1024 and print detailed information about the scan results, you could run the following command:
```
python port_scanner.py example.com 1-1024 -v
```

The program will then begin scanning the specified host and port range. When the scan is complete, the program will print a list of open ports, along with any additional information specified by the verbose argument.
```
Open ports for example.com:
PORT    SERVICE
80      http
```
