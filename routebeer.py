'''
    Routebeer 0001
    
    A handy, cross-platform utility for adding manual IP routes in bulk.

    Copyright Vincent Brubaker-Gianakos
    Some Rights Reserved

    This work is licensed under a Creative Commons Attribution 3.0 United States License.
    
    http://creativecommons.org/licenses/by/3.0/us/
    
    THE WORK (AS DEFINED BELOW) IS PROVIDED UNDER THE TERMS OF THIS CREATIVE COMMONS PUBLIC LICENSE ("CCPL" OR "LICENSE").
    THE WORK IS PROTECTED BY COPYRIGHT AND/OR OTHER APPLICABLE LAW.
    ANY USE OF THE WORK OTHER THAN AS AUTHORIZED UNDER THIS LICENSE OR COPYRIGHT LAW IS PROHIBITED.
    
    BY EXERCISING ANY RIGHTS TO THE WORK PROVIDED HERE, YOU ACCEPT AND AGREE TO BE BOUND BY THE TERMS OF THIS LICENSE.
    TO THE EXTENT THIS LICENSE MAY BE CONSIDERED TO BE A CONTRACT, THE LICENSOR GRANTS YOU THE RIGHTS CONTAINED HERE IN
    CONSIDERATION OF YOUR ACCEPTANCE OF SUCH TERMS AND CONDITIONS.
'''

import sys
import os
from os import popen
from string import split, join
from re import match
import socket

def ValidIPV4(addr):
    try:
        socket.inet_aton(addr)
        return True
    except socket.error:
        return False

def ValidMAC(addr):
    return match("[0-9a-f]{2}([-:][0-9a-f]{2}){5}$", addr.lower())

platform = os.uname()[0]

if (platform == 'Darwin'):
    def Usage():
        print " ".join(["Darwin", "Usage:", "python" , os.path.basename(sys.argv[0]), "gateway [address, address, address]"])
    def Main():
        if(len(sys.argv) == 2):
            if(sys.argv[1] == "print"):
                print popen("netstat -rn").read()
            else:
                Usage()
        elif (len(sys.argv) >= 3):
            arg_gateway = sys.argv[1]
            arg_addresses = sys.argv[2:]
            for addr in arg_addresses:
                shell = " ".join(['sudo', 'route', 'add', addr + "/32", arg_gateway])
                print shell
                print popen(shell).read()
        else:
            Usage()
else:
    def GetRoutes():
        return_vals = popen("route print").read()
        if return_vals:
            return [elem.strip().split() for elem in return_vals.split("\n") if match("^[0-9]", elem.strip()) and ValidIPV4(elem.strip().split()[0])]
     
    def GetInterfaces():
        return_vals = popen("route print").read()
        if return_vals:
            return [[x for x in elem.strip().split('...') if x] for elem in return_vals.split("\n") if len([x for x in elem.strip().split('...') if x]) > 2]
    
    def Usage():
        print " ".join(["Windows", "Usage:", "python", os.path.basename(sys.argv[0]), " interface metric gateway [address, address, address]"])

    def Main():
        if(len(sys.argv) == 2):
            if(sys.argv[1] == "print"):
                print popen("route print").read()
            else:
                Usage()
        elif (len(sys.argv) >= 5):
            arg_interface = sys.argv[1]
            arg_metric = sys.argv[2]
            arg_gateway = sys.argv[3]
            arg_addresses = sys.argv[4:]
            select_interface = None
            interfaces = GetInterfaces()
            for interface in interfaces:
                if(interface[2].find(arg_interface) == 0):
                    print "Matched interface: " + interface[2]
                    select_interface = interface
            if(select_interface == None):
                print "Unknown interface \"" + arg_interface + "\""
            routes = GetRoutes()
            for addr in arg_addresses:
                shell = " ".join(['route', '-p', 'ADD', addr, "MASK", "255.255.255.255", arg_gateway, "IF", select_interface[0]])
                print shell
                print popen(shell).read()
        else:
            Usage()
Main()