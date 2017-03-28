#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__doc__="""
# SCANNER DE REDE PYTHON 3 - POR ROBISON PEREIRA MACHADO
#
# FORNEÇA O PRIMEIRO IP COMPLETO (EX: 192.168.0.1)
# DEPOIS FORNEÇA O IP FINAL, APENAS O ÚLTIMO OCTETO (EX: 254)
#
# SE FORNECERMOS O IP 192.168.0.1 E DEPOIS O VALOR 254
# eLE IRÁ ESCANEAR DO IP FINAL 1 ATÉ O 254
# NO FINAL MOSTRARÁ OS IP's E OS MAC's QUE ESTÃO CONECTADOS
# E DIRÁ O NÚMERO DE EQUIPAMENTOS ONLINE NA REDE
"""
import sys
import subprocess
import os
import subprocess
import time
import threading
from threading import Thread


class NetworkScanner(object):
	ips_online=[]
	threads=[]

	def scannear_rede(self, ip_inicial, ip_final):
		ip_base=subprocess.getoutput("echo %s 2> /dev/null | egrep -o \"([0-9]{1,3}\.){3}\"" % ip_inicial)
		ip_inicial=int(subprocess.getoutput("echo %s 2> /dev/null | egrep -o \"([0-9]{1,3})$\"" % ip_inicial))
		ip_final=int(ip_final)

		while(ip_inicial <= ip_final):
			ip=ip_base+str(ip_inicial)
			self.threads.append(threading.Thread(target=self.ping, args=(ip,)).start())
			ip_inicial += 1

	def ping(self, ip):
		time.sleep(0.2)
		ping = os.system('ping -c 1 %s > /dev/null 2> /dev/null' % ip)
		if(ping==0):
			mac_adress=subprocess.getoutput("arp -a %s 2> /dev/null | egrep -o \"([a-Z,0-9]{2}\:){5}[a-Z,0-9]{2}\"" % ip)
			self.ips_online.append((ip,mac_adress,))
		while(len(self.threads)==0):
			time.sleep(0.5)
		self.threads.pop()
		print("\n\n*****************\nTHREADS EXISTENTES >> %s\n*****************\n" % len(self.threads))
		return

def main():
	ip_inicial = input("Digite o IP inicial (completo): ")
	ip_final = input("Digite o IP final (apenas o último octeto. Ex: 254): ")


	scan = NetworkScanner()
	scan.scannear_rede(ip_inicial, ip_final)

	while(len(scan.threads)>0):
		time.sleep(0.5)
		#print("\n\n*****************\nTHREADS EXISTENTES >> %s\n*****************\n" % len(scan.threads))

	scan.ips_online.sort()
	for pc in scan.ips_online:
		print("PC ONLINE >> IP=%s - MAC=%s" % (pc[0], pc[1]))

	print("\nExistem %s dispositivos online neste momento\n\n" % len(scan.ips_online))

	return 0

if __name__ == '__main__':
	main()


