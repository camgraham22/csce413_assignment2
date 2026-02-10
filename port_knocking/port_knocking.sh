# 1. Flush existing rules for a clean start
iptables -F
iptables -X

iptables -A INPUT -p tcp --dport 2222 -j DROP
iptables -A INPUT -p tcp --dport 2222 -m recent --rcheck --name Auth3 -j ACCEPT

# Knock #1: port 1234, sets Auth1
iptables -A INPUT -p tcp --dport 1234 -m recent --set --name Auth1 -j DROP

# Knock #2: Port 5678 -> If Auth1, set Auth2
iptables -A INPUT -p tcp --dport 5678 -m recent --rcheck --name Auth1 -m recent --set --name Auth2 -j DROP

# Knock #3: Port 9012 -> If Auth2, set Auth3
iptables -A INPUT -p tcp --dport 9012 -m recent --rcheck --name Auth2 -m recent --set --name Auth3 -j DROP