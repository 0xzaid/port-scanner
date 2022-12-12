# Port Scanner

Port Scanner project using Python for [FreeCodeCamp](https://www.freecodecamp.org/learn/information-security/information-security-projects/port-scanner)
I have improved it by making it usable through a terminal, and I plan to add more features.

# Install

Open your terminal or command prompt.  
Navigate to the directory where you want to clone the project.

Use the command ```git clone``` followed by the project's URL from GitHub.
```git clone https://github.com/0xzaid/port-scanner.git```

This will create a new directory with the project's name in the current directory.
Navigate to the project's directory using the "cd" command.
```cd port-scanner```

The project should is now on your machine.

# Usage

To use port_scanner.py, open a terminal or command prompt and navigate to the directory where the program is saved. Then, run the following command:
```
python port_scanner.py <target> <port_range> -o <file_name> -t <no_of_threads> -v
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

To ask for help:
```
python port_scanner.py -h
```
This results in:
```
usage: port_scanner.py [-h] [-o OUTPUT] [-t THREADS] [-v] target port_range

Simple Port scanner developed in Python

positional arguments:
  target                the target to scan
  port_range            the range of ports to scan

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        output file name
  -t THREADS, --threads THREADS
                        specify the number of threads
  -v, --verbose         enable verbose output
```
