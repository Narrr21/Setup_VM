#!/usr/bin/env python3
import requests
import subprocess
import sys
import socket
import time

class NetworkClient:
    def __init__(self):
        self.domain = "web.mylab.local"
        self.port = "80"
        
    def configure_network_manual(self):
        """Configure network manually"""
        print("=== Manual Network Configuration ===")
        ip = input("Enter IP address (e.g., 192.168.100.20): ")
        netmask = input("Enter netmask (default: 255.255.255.0): ") or "255.255.255.0"
        gateway = input("Enter gateway (e.g., 192.168.100.1): ")
        dns = input("Enter DNS server (e.g., 192.168.100.1): ")
        
        network_config = f"""# This file describes the network interfaces available on your system
# and how to activate them. For more information, see interfaces(5).

source /etc/network/interfaces.d/*

# The loopback network interface
auto lo
iface lo inet loopback

# The primary network interface - Manual configuration
auto enp0s3
iface enp0s3 inet static
    address {ip}
    netmask {netmask}
    gateway {gateway}
    dns-nameservers {dns}
"""
        
        try:
            with open('/tmp/interfaces', 'w') as f:
                f.write(network_config)
            
            subprocess.run(['sudo', 'cp', '/tmp/interfaces', '/etc/network/interfaces'], check=True)
            print("Manual configuration saved. Restarting network...")
            subprocess.run(['sudo', 'systemctl', 'restart', 'networking'], check=True)
            time.sleep(3)
            print("Manual configuration applied successfully!")
            return True
        except Exception as e:
            print(f"Error configuring network manually: {e}")
            return False
    
    def configure_network_dhcp(self):
        """Configure network using DHCP"""
        print("=== DHCP Network Configuration ===")
        
        network_config = """# This file describes the network interfaces available on your system
# and how to activate them. For more information, see interfaces(5).

source /etc/network/interfaces.d/*

# The loopback network interface  
auto lo
iface lo inet loopback

# The primary network interface - DHCP mode
auto enp0s3
iface enp0s3 inet dhcp
"""
        
        try:
            with open('/tmp/interfaces', 'w') as f:
                f.write(network_config)
            
            subprocess.run(['sudo', 'cp', '/tmp/interfaces', '/etc/network/interfaces'], check=True)
            print("DHCP configuration saved. Restarting network...")
            subprocess.run(['sudo', 'systemctl', 'restart', 'networking'], check=True)
            time.sleep(2)
            
            print("Requesting IP from DHCP server...")
            subprocess.run(['sudo', 'dhclient', 'enp0s3'], check=True)
            time.sleep(2)
            print("DHCP configuration applied successfully!")
            return True
        except Exception as e:
            print(f"Error configuring network with DHCP: {e}")
            return False
    
    def show_network_info(self):
        """Show current network configuration"""
        try:
            print("=== Current Network Configuration ===")
            
            result = subprocess.run(['ip', 'addr', 'show', 'enp0s3'], 
                                  capture_output=True, text=True, check=True)
            print("Network Interface:")
            for line in result.stdout.split('\n'):
                if 'inet ' in line and '127.0.0.1' not in line:
                    print(f"  IP: {line.strip()}")
            
            result = subprocess.run(['ip', 'route', 'show'], 
                                  capture_output=True, text=True, check=True)
            print("Routing:")
            for line in result.stdout.split('\n'):
                if 'default' in line:
                    print(f"  Gateway: {line.strip()}")
            
            try:
                with open('/etc/resolv.conf', 'r') as f:
                    print("DNS Configuration:")
                    for line in f:
                        if line.strip() and not line.startswith('#'):
                            print(f"  {line.strip()}")
            except:
                print("  Could not read DNS configuration")
            
            print("\nDNS Resolution Test:")
            try:
                ip = socket.gethostbyname(self.domain)
                print(f"  {self.domain} -> {ip}")
            except Exception as e:
                print(f"  {self.domain} -> FAILED ({e})")
                
        except Exception as e:
            print(f"Error getting network info: {e}")
    
    def test_connection(self):
        """Test connection to web server"""
        try:
            url = f"http://{self.domain}:{self.port}"
            print(f"=== Testing Connection to {url} ===")
            
            try:
                resolved_ip = socket.gethostbyname(self.domain)
                print(f"DNS Resolution: {self.domain} -> {resolved_ip}")
            except Exception as e:
                print(f"DNS Resolution FAILED: {e}")
                return
            
            print("Making HTTP request...")
            response = requests.get(url, timeout=10)
            
            print(f"Connection Successful!")
            print(f"Status Code: {response.status_code}")
            print(f"Response Headers:")
            for header, value in response.headers.items():
                print(f"  {header}: {value}")
            
            print(f"\n=== Web Page Content ===")
            print(response.text)
            print("=" * 50)
            
        except requests.exceptions.ConnectTimeout:
            print("Connection timeout - Server might be down")
        except requests.exceptions.ConnectionError as e:
            print(f"Connection error: {e}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
    
    def run(self):
        """Main program loop"""
        while True:
            print("\n" + "="*60)
            print("           MyLab Network Client - VM3")
            print("="*60)
            print("1. Configure Network (Manual IP)")
            print("2. Configure Network (DHCP)")  
            print("3. Show Network Information")
            print("4. Test Web Connection")
            print("5. Exit")
            print("="*60)
            
            choice = input("Select option (1-5): ").strip()
            
            if choice == '1':
                self.configure_network_manual()
            elif choice == '2':
                self.configure_network_dhcp()
            elif choice == '3':
                self.show_network_info()
            elif choice == '4':
                self.test_connection()
            elif choice == '5':
                print("Goodbye!")
                break
            else:
                print("Invalid option! Please select 1-5.")
            
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    print("Starting MyLab Network Client...")
    client = NetworkClient()
    client.run()