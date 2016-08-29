import os


for line in open("tunein-station.m3u"):
  os.system("timeout 30 wget %s" % line) 
  # os.system("curl -O %s" % line) ##If no wget and need curl