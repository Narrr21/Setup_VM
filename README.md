# DNS Network Simulation

## Network Topology

- **VM 1 (DNS/DHCP Server)**: `192.168.100.1/24`
- **VM 2 (HTTP Server)**: `192.168.100.2/24`
- **VM 3 (Client)**: DHCP assigned or manual configuration
- **VM 4 (Reverse Proxy)**: `192.168.100.4/24`
- **Network**: Internal isolated network `192.168.100.0/24`

## Prerequisites

### Hardware Requirements
- Host machine with at least 4GB RAM
- 40GB available disk space
- VirtualBox or VMware installed

### Software Requirements
- VirtualBox or VMware Workstation
- Debian 12 Server ISO
- 4 Virtual Machines with specifications:
  - RAM: 512MB - 1GB per VM
  - Storage: 8-10GB per VM
  - Network: Internal Network (isolated from internet)

## Quick Start

1. **Set up VirtualBox network**:
   - Create Internal Network named "lab-network"
   - Configure all VMs to use this internal network

2. **Install Debian 12 on all VMs**:
   - Use minimal installation (no desktop environment)
   - Install only SSH server and standard utilities

3. **Configure each VM** following the detailed guides below
4. **Something similar in all VM** 
   - All VM have network config
   - change `/etc/network/interfaces` of all VM to their respective network/interfaces (explained later in Installation)

## VM Configuration

### VM 1 - DNS Server + DHCP Server

**Extra file**
- isc-dhcp-server
- bind9, bind9utils, bind9-doc

**Primary Functions:**
- DNS resolution for `mylab.local` domain
- DHCP IP address assignment
- Network gateway functionality

**Key Services:**
- BIND9 DNS Server
- ISC DHCP Server

**Configuration Files:**
- `/etc/bind/named.conf.local`
- `/etc/bind/db.mylab.local`
- `/etc/bind/db.192.168.100`
- `/etc/dhcp/dhcpd.conf`
**Optional (Just Test)**
- add nameserver 127.0.0.1 to `/etc/resolv.conf`
- add test.sh, and run it.

### VM 2 - HTTP Server

**Extra file**
- nginx

**Primary Functions:**
- Web server hosting on port 8080
- Backend service for reverse proxy

**Key Services:**
- Nginx Web Server

**Configuration Files:**
- `/etc/nginx/sites-available/default`
- `var/www/index.html`

### VM 3 - Client

**Extra file**
- python3 python3-pip
- requests (use pip)

**Primary Functions:**
- Network client with CLI interface
- Network configuration testing
- Web service connectivity testing

**Key Features:**
- Python-based CLI application
- Manual and DHCP network configuration options
- Built-in connectivity testing tools
- DNS resolution verification

**Configuration Files:**
- `/etc/client-app/clients.py`

### VM 4 - Reverse Proxy

**Extra file**
- python3 python3-pip iptables-persistent
- flask, request (use pip)

**Primary Functions:**
- HTTP reverse proxy server
- Firewall and security enforcement
- Traffic filtering and logging

**Key Services:**
- Python Flask-based reverse proxy
- iptables firewall rules

**Configuration Files:**
- `/etc/reverse-proxy/firewall_setup.sh`
- `/etc/reverse-proxy/reverse_proxy.py`

## Installation Guide

### Step 1: Initial Setup

1. **Create VirtualBox Internal Network**:
   - Open VirtualBox Manager
   - Go to File > Host Network Manager
   - Create new internal network named "lab-network"

2. **VM Installation**:
   - Install Debian 12 on all 4 VMs
   - Use minimal installation (uncheck desktop environments)
   - Select only "SSH server" and "standard system utilities"
   - Create non-root user for each VM

### Step 2: Network Configuration

Configure static IP addresses on each VM by editing `/etc/network/interfaces`:

**VM 1 (DNS/DHCP Server)**:
```bash
auto enp0s3
iface enp0s3 inet static
    address 192.168.100.1
    netmask 255.255.255.0
    network 192.168.100.0
    broadcast 192.168.100.255
```

**VM 2 (HTTP Server)**:
```bash
auto enp0s3
iface enp0s3 inet static
    address 192.168.100.2
    netmask 255.255.255.0
    gateway 192.168.100.1
    dns-nameservers 192.168.100.1
```
**VM 3 (Client)**: # base using dhcp
```bash
auto enp0s3
iface enp0s3 inet dhcp
```

**VM 4 (Reverse Proxy)**:
```bash
auto enp0s3
iface enp0s3 inet static
    address 192.168.100.4
    netmask 255.255.255.0
    gateway 192.168.100.1
    dns-nameservers 192.168.100.1
```

### Step 3: Service Configuration

#### VM 1 - DNS and DHCP Services

1. **Install BIND9**:
   ```bash
   sudo apt update
   sudo apt install bind9 bind9utils bind9-doc
   ```

2. **Configure DNS zones using provided configuration files**

3. **Install DHCP Server**:
   ```bash
   sudo apt install isc-dhcp-server
   ```

4. **Start services**:
   ```bash
   sudo systemctl enable bind9 isc-dhcp-server
   sudo systemctl start bind9 isc-dhcp-server
   ```

#### VM 2 - HTTP Server

1. **Install Nginx**:
   ```bash
   sudo apt install nginx
   ```

2. **Configure Nginx to listen on port 8080**

3. **Deploy custom web page**

#### VM 3 - Client

1. **Install Python dependencies**:
   ```bash
   sudo apt install python3 python3-pip
   pip3 install requests
   ```

2. **Deploy client application**:
   ```bash
   cp vm3-client/client.py ~/
   chmod +x ~/client.py
   ```

#### VM 4 - Reverse Proxy

1. **Install dependencies**:
   ```bash
   sudo apt install python3 python3-pip iptables-persistent
   pip3 install flask requests
   ```

2. **Deploy reverse proxy application**

3. **Configure firewall rules**

4. **Set up systemd service for auto-start**

# DONE
## AUTHOR
- Nadhif Al Rozin