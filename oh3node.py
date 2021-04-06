#!/usr/bin/python

import logging
import subprocess
import time
from datetime import datetime

# VARS - Change me!

nodecall = "OH3SPN"
nodessid = "-7"
nodeloc = "Akaa, Finland, KP11VE"
sysopcall = "OH3SPN"
sysopemail = "steve@oh3spn.fi"
sysoppacket = "OH3SPN@PE1RRR.#NBW.NLD.EURO"

# VARS (private)
nodename = "oh3node"
nodever = "0.1c"

# logfile
logging.basicConfig(filename='oh3node.log', encoding='utf-8', level=logging.DEBUG)

# first contact
curtime = datetime.now()
logging.debug('CONNECT: %s', curtime)

# try to guess call from netstat
# ax25d doesn't pass anything useful regarding source of connection
# we assume the last incoming connection is the correct call:-

def setsrccall():
  global srccall
  srccall = subprocess.call("/usr/bin/netstat --ax25 | tail -n +4 | awk '{ print $1 }' | head -1", stdout=subprocess.PIPE, shell=True)
  if not srccall:
    srccall = "unknown"
  logging.debug('CONNECT: guessed SRC %s', srccall)

def welcome():
  print("Welcome", srccall," to node", nodecall, nodessid,".")
  print("Experimental", nodename, "version:", nodever, "by OH3SPN")
  curtime = datetime.now()
  # subprocess.run("/usr/bin/date", stdout=subprocess.PIPE, text=True)
  print("Local time: ", curtime)

# confirm call

def confirmcall():
  global srccall
  print("Enter your call [", srccall,"]:")
  srccall = input (":") or srccall
  print("\nHello ", srccall, ".\n")
  logging.debug('CONNECT: actual call: %s', str(srccall))

def usage():
  print("Commands: MHeard, MSG, HElp, INfo, CONnections, BYe")

def mheard():
  mheard = subprocess.run("/usr/bin/mheard | awk '{print $1}' | head -9 | tail -8", shell=True, stdout=subprocess.PIPE, text=True)
  print("Last 8 stations heard:")
  mheard = mheard.stdout.splitlines()
  for x in range(len(mheard)):
    print(mheard[x])

def info():
  print("Experimental node, under development.")
  print(nodename, "version:", nodever, "by OH3SPN")
  print("Location: ", nodeloc)
  print("Email: ", sysopemail)
  print("Packet: ", sysoppacket)

def message():
  print("Leave message for sysop (", sysopcall,")? [Y/N]")
  cmd = input(": ")
  if cmd in ['y', 'Y', 'yes', 'YES']:
    to_sysop = input("Input message: ")
    logging.debug('SYSOP: %s', to_sysop)
    print("Message saved.")

def connections():
  ax25cons = subprocess.run("/usr/bin/netstat --ax25 | awk '{print $1}'", shell=True, stdout=subprocess.PIPE, text=True)
  ax25cons = ax25cons.stdout.splitlines()
  print("ax.25 connections:-")
  for x in range(2,len(ax25cons)):
    print(ax25cons[x])

def goodbye():
  print("Goodbye", srccall, " - please visit again.")
  logging.debug('GOODBYE: %s', str(srccall))
  exit()

### MAIN CODE ###
# On incoming connection, find SRC (and confirm) call, welcome user and provide menu/commands.

setsrccall()
welcome()
confirmcall()
usage()

while True:
  cmd = input("> ")
  logging.debug('ACTION: %s selected %s', srccall, cmd)
  if cmd in ['mheard', 'mh', 'MH', 'MHEARD']:
    mheard()
  if cmd in ['info', 'inf', 'in', 'INFO', 'IN', 'INF']:
    info()
  if cmd in ['msg', 'MSG']:
    message()
  if cmd in ['help', 'he', 'HELP', 'HE']:
    print("Commands: MHeard, MSG, HElp, INfo, CONnections, BYe")
  if cmd in ['CON', 'con', 'CONNECTIONS', 'connections']:
    connections()
  if cmd in ['bye', 'by', 'BYE', 'BY', 'quit', 'b', 'B']:
    goodbye()

