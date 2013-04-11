#!/usr/bin/python

import re

import dns.resolver

class WebServer:

  ipAddr = ""

	sites = []

	def __init__(self, ipAddr):
		self.ipAddr = ipAddr

		ipAddr = ipAddr.split('.')
		ipAddr.reverse()
		ipAddr = '.'.join(ipAddr)
		ipAddr = ipAddr + '.in-addr.arpa'

		for response in dns.resolver.query(ipAddr, 'PTR'):
			url = re.sub('\.$', '', str(response))
			if self.isValid(url):
				self.sites.append(url)
		self.exportToCSV()

	def isValid(self, siteUrl):
		return True;

	def exportToCSV(self):
		for site in self.sites:
			print(site + "," + self.ipAddr)

if __name__ == "__main__":
	webServer = WebServer('127.0.0.1')
