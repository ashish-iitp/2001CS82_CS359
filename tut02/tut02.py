from scapy.all import *


def arp_pcap():
    packets = sniff(count=5, filter="arp")
    wrpcap("./output/arp_2001cs82.pcap", packets)


def dns():
    pcktdump = PcapWriter("./output/dns_2001cs82.pcap")
    dns_req = IP(dst="8.8.8.8")/UDP(dport=53)/DNS(rd=1, qd=DNSQR(qname="kinopoisk.ru"))
    answer = sr1(dns_req, verbose=1)
    pcktdump.write(dns_req)
    pcktdump.write(answer)


def icmp_ping():
    packet = IP(dst="kinopoisk.ru")/ICMP()
    answer = sr1(packet)
    pcktdump = PcapWriter("./output/icmp_2001cs82.pcap")
    pcktdump.write(packet)
    pcktdump.write(answer)


def tcphandshake():
    ip=IP(dst="69.147.80.15")
    SYN=ip/TCP(sport=1500, dport=80, flags="S", seq=100)
    pcktdump = PcapWriter("./output/tcphandshake_2001cs82.pcap")
    pcktdump.write(SYN)
    SYNACK=sr1(SYN)
    ACK = ip/TCP(sport=1500, dport=80, flags="A", seq=SYNACK.ack, ack=SYNACK.seq+1)
    pcktdump.write(SYNACK)
    pcktdump.write(ACK)
    
def tcpend():
    ip=IP(dst="69.147.80.15")
    SYN=ip/TCP(sport=1500, dport=80, flags="S", seq=100)
    pcktdump = PcapWriter("./output/ftpendshake_2001cs82.pcap")
    SYNACK=sr1(SYN)
    ACK = ip/TCP(sport=1500, dport=80, flags="A", seq=SYNACK.ack, ack=SYNACK.seq+1)
    send(ACK)
    FIN=ip/TCP(sport=1500, dport=80, flags="FA", seq=SYNACK.ack, ack=SYNACK.seq + 1)
    FINACK=sr1(FIN)
    LASTACK=ip/TCP(sport=1500, dport=80, flags="A", seq=FINACK.ack, ack=FINACK.seq + 1)
    send(LASTACK)
    pcktdump.write(FIN)
    pcktdump.write(FINACK)
    pcktdump.write(LASTACK)

def ftphandshake():
    ip=IP(dst="198.246.117.106")
    SYN=ip/TCP(sport=1500, dport=80, flags="S", seq=100)
    pcktdump = PcapWriter("./output/ftphandshake_2001cs82.pcap")
    pcktdump.write(SYN)
    SYNACK=sr1(SYN)
    ACK = ip/TCP(sport=1500, dport=80, flags="A", seq=SYNACK.ack, ack=SYNACK.seq+1)
    pcktdump.write(SYNACK)
    pcktdump.write(ACK)
    FIN=ip/TCP(sport=1500, dport=80, flags="FA", seq=SYNACK.ack, ack=SYNACK.seq + 1)
    FINACK=sr1(FIN)
    LASTACK=ip/TCP(sport=1500, dport=80, flags="A", seq=FINACK.ack, ack=FINACK.seq + 1)
    send(LASTACK)
    pcktdump.write(FIN)
    pcktdump.write(FINACK)
    pcktdump.write(LASTACK)

    
    
arp_pcap()
print("done")
dns()
print("done")
icmp_ping()
print("done")
tcphandshake()
print("done")
tcpend()
print("done")
ftphandshake()