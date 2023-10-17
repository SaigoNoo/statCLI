# statCLI
*Control your server over SSH with a CLI*

## What is statCLI
StatCLI is a script writed in Python. It use the known library **Paramiko**, who
allow to do some actions on a host over the SSH protocol. The main idea here is to
access to your server, run commands, return the results as strings to this script and
have a *kind* of monitoring tool.

### **This script hasn't been released to be officaly released as a public tool. It has been done for my school to show my skills for a test. If you love the idea, feel free to use it but credit me please !**
## Install the requirments:
Used library:
- paramiko
```bash
pip3 install -r requirments.txt
```

## **Use the script:**
It's realy easy:
```text
usage: main.py [-h] [--all] [--ram] [--os] [--cpu] [--network] [--users]

Commands to choose which informations show

options:
  -h, --help     show this help message and exit
  --all, -a      Get all informations from this script
  --ram, -r      Get informations about your RAM (free command)
  --os, -o       Get informations about your OS (lsb_release -a command)
  --cpu, -c      Get informations about your CPU (lscpu command & top)
  --network, -n  Get informations about your NIC (nstat & netplan)
  --users, -u    Get informations about users in the system
```

## Why some commands don't return anything or a right error ?
It's because the user I writed in the credentials file is a user with privileges and without password need.
If you want, create a user on UNIX / Linux:
```bash
sudo adduser statcli
```
(You will need to set a password)...
```bash
sudo nano /etc/sudoers
```
And write it in:
```text
statcli     ALL=(ALL)   NOPASSWD: free, lsb_release, lscpu, top, cat, nstat, groups 
```
With this, statcli will be able to run everything with root rights and only the free (etc...) without password.
The all commands will require a password !
