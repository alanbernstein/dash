'''
complete daemon to listen for button presses, listen for specific MACs
and report to server with string associated with that MAC
'''
# todo:
# - set this up as a proper daemon, that can't die

from scapy.all import *
import urllib2
# color meanings
# B blink                    wifi setup mode
# B solid                    wifi setup successful
# B blink -> R solid 5s      wifi setup failed
# W blink -> G solid         order successful
# W blink -> R solid         order failed
# R solid 5s                 not set up


server_url = 'http://www.insignificantbits.net/cgi-bin/dash.py?press='
buttons = {'74:c2:46:1a:2a:28': 'michael',
           '74:c2:46:0b:9e:b1': 'oven',
           '74:75:48:f7:e5:85': 'unassigned-1'}

def arp_display(pkt):
    if not pkt.__contains__(ARP): # fix i had to add
        return
    if pkt[ARP].op == 1: #who-has (request)
        if pkt[ARP].psrc == '0.0.0.0': # ARP Probe
            if pkt[ARP].hwsrc in buttons.keys():
                print(buttons[pkt[ARP].hwsrc])
                report_to_server(buttons[pkt[ARP].hwsrc])
            else:
                print "ARP Probe from unknown device: " + pkt[ARP].hwsrc


def report_to_server(button_name):
    url = server_url+button_name
    print(url)
    resp = urllib2.urlopen(url).read()
    print(resp)
    #if resp.status_code == 200:
    #    return
    #else:
    #    print('error: %s' % resp.status_code)


print sniff(prn=arp_display, filter="arp", store=0, count=0)
