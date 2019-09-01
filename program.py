import pip
import sys
import csv
import cv2
import keyboard
#import pygame
import requests
import time
import urllib3.request
import urllib3.request as urllib2
import os

from tkinter import *
from enum import Enum
from requests import get


class Program:

	@staticmethod
	def Main():

		rtsp = RTSPWorker().GetRTSP()
		print(rtsp)

		ip = RTSPWorker().GetIP(rtsp)
		print(ip)

		Stream().ShowStream(rtsp, ip)


class Stream:

	def ShowStream(self, rtsp, ip):
		cap = cv2.VideoCapture(rtsp)
		cc = CameraCommands()
		cc.SetIP(ip)
		while True:
			ret, frame = cap.read()
			try:
				cv2.imshow('Camera', frame)
			except:
				continue

			if keyboard.is_pressed('d'):
				cc.Rotate('right')
			if keyboard.is_pressed('w'):
				cc.Rotate('up')
			if keyboard.is_pressed('s'):
				cc.Rotate('down')
			if keyboard.is_pressed('a'):
				cc.Rotate('left')
			if keyboard.is_pressed('q'):
				cc.Rotate('stop')
			if keyboard.is_pressed('e'):
				cc.Infraredstat()

			cv2.waitKey(10)
'''
			if event.type == pygame.KEYDOWN:

				if event.key == pygame.K_LEFT:
					cc.Rotate('left')
				if event.key == pygame.K_RIGHT:
					cc.Rotate('right')
				if event.key == pygame.K_UP:
					cc.Rotate('up')
				if event.key == pygame.K_DOWN:
					cc.Rotate('down')

			if event.type == pygame.KEYUP:

				cc.Rotate('stop')

'''

			


class CameraCommands:

	IP = ''

	def SetIP(self, val):
		self.IP = val


	def Rotate(self, side):
		password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
		top_level_url = "http://"+self.IP+"/web/cgi-bin/hi3510/ptzctrl.cgi?-step=0&-act="+side
		print(top_level_url)
		password_mgr.add_password(None, top_level_url, "admin", "admin")
		handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
		opener = urllib.request.build_opener(handler)
		opener.open(top_level_url)
		urllib.request.install_opener(opener)

	s = ''
	def Infraredstat(self):
		if self.s == 'open':
			self.s = 'close'
		else:
			self.s = 'open'
		password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
		top_level_url = "http://"+self.IP+"/cgi-bin/hi3510/param.cgi?cmd=setinfrared&cururl=http%3A%2F%2F"+self.IP+"%2Fdisplay.html&-infraredstat="+self.s
		password_mgr.add_password(None, top_level_url, "admin", "admin")
		handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
		opener = urllib.request.build_opener(handler)
		opener.open(top_level_url)
		urllib.request.install_opener(opener)


class RTSPWorker:

	def GetRTSP(self):
		deserialized = self.DeserializeRTSP()
		rtsp = self.CheckRtspExistence(deserialized)
		return rtsp

	def CheckRtspExistence(self, url):
		choice = raw_input("Current RTSP: "+url+";\nChange it?[y/n]")
		if (choice == 'n'):
			return url
		if (choice == 'y'):
			url = input("Print new RTSP: ")
			SerializeRTSP(url)
			return url
	
	def GetIP(self, rtsp):
		text = rtsp
		left = '@'
		right = '/11'
		return str(text[text.index(left)+len(left):text.index(right)])

	def DeserializeRTSP(self):
		with open('data.csv') as f:
			reader = csv.reader(f)
			for row in reader:
				url = str(row)
				url = url.replace("[", "")
				url = url.replace("]", "")
				url = url.replace("'", "")
				url = url.replace(",", "")
				url = url.replace(" ", "")
				return url

	def SerializeRTSP(self, rtsp):
		with open('data.csv', 'w', newline='') as a:
			writer = csv.writer(a)
			writer.writerow(rtsp)


Program.Main()
