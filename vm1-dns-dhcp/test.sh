#!/bin/bash

DOMAIN="mylab.local"
HOSTNAME="web.$DOMAIN"
IP="192.168.100.4"
REVERSE_IP="4.100.168.192.in-addr.arpa"

echo "=== Cek status service BIND9 ==="
systemctl is-active --quiet bind9 && echo "BIND9 aktif" || echo "BIND9 tidak aktif"

echo
echo "=== Cek syntax file zona ==="
named-checkzone "$DOMAIN" /etc/bind/db."$DOMAIN"
named-checkzone 100.168.192.in-addr.arpa /etc/bind/db.192.168.100

echo
echo "=== Tes forward lookup (\$HOSTNAME -> IP) ==="
dig @"127.0.0.1" "$HOSTNAME" +short

echo
echo "=== Tes reverse lookup (\$IP -> HOSTNAME) ==="
dig @"127.0.0.1" -x "$IP" +short

echo
echo "=== Tes ping domain ==="
ping -c 2 "$HOSTNAME"

echo
echo "=== Cek /etc/resolv.conf ==="
cat /etc/resolv.conf | grep nameserver