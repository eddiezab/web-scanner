#!/usr/bin/python

import re

import dns.resolver

import socket
import httplib
import ssl

class WebSite:
	
	name = ""

	sslName = ""

	ipAddr = ""

	port = 0

	responseCode = 0

	notes = []

	def __init__(self, name, ipAddr, port):
		self.name = name
		self.ipAddr = ipAddr
		self.port = port
		
		self.getHeader()

	def getHeader(self, forceHTTP=False):
		try:
			if '443' in str(self.port) and not forceHTTP:
				conn = httplib.HTTPSConnection(self.name, self.port)
			else:
				conn = httplib.HTTPConnection(self.name, self.port) 

			conn.request('HEAD', '/')
			response = conn.getresponse()
			self.responseCode = response.status

			if self.responseCode == 302:
				self.notes.append(response.getheader('Location'))
			
		except StandardError:

			conn.close()

			if not forceHTTP:
				self.getHeader(True)
			else:
				pass
		
		if not forceHTTP:
			print(self.name + "," + str(self.responseCode) + "," + '/'.join(self.notes))
		


class WebServer:
	
	vendor = ""

	ipAddr = ""

	sites = []

	ports = []

	def __init__(self, ipAddr):
		self.ipAddr = ipAddr

		self.checkCommonPorts()

		ipAddr = ipAddr.split('.')
		ipAddr.reverse()
		ipAddr = '.'.join(ipAddr)
		ipAddr = ipAddr + '.in-addr.arpa'

		try:
			for response in dns.resolver.query(ipAddr, 'PTR'):
				url = re.sub('\.$', '', str(response))
				if self.isValid(url):
					self.sites.append(url)
		except dns.resolver.NXDOMAIN:
			self.sites.append(self.ipAddr)

		for site in self.sites:
			for port in self.ports:
				website = WebSite(site, self.ipAddr, port)

		self.exportToCSV()

	def isValid(self, siteUrl):
		return True;

	def checkCommonPorts(self):
		commonPorts = [80, 8080, 443, 8443]

		for port in commonPorts:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.settimeout(2)
			try:
				s.connect((self.ipAddr, port))
				s.shutdown(2)
				self.ports.append(str(port))
			except:
				pass
			

	def exportToCSV(self):
		for site in self.sites:
			for port in self.ports:
				print(site + "," + self.ipAddr + "," + port)

if __name__ == "__main__":
	webServer = WebServer('127.0.0.1')
