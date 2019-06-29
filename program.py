import csv
import cv2
import keyboard
import requests
import sys
import time
import urllib.request
import urllib.request as urllib2
import os

from tkinter import *
from enum import Enum
from requests import get

ip = ''

class Program:

	def Main():
		rtsp = RTSPWorker().GetRTSP()
		print(rtsp)
		Stream().ShowStream(rtsp)


class Stream:
	def ShowStream(self, rtsp):
		cap = cv2.VideoCapture(rtsp)
		cc = CameraCommands()
		while True:
			ret, frame = cap.read()
			cv2.imshow('Camera', frame)

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


class CameraCommands:

	def Rotate(self, side):
		password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
		top_level_url = "http://192.168.1.118/web/cgi-bin/hi3510/ptzctrl.cgi?-step=0&-act="+side
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
		top_level_url = "http://192.168.1.118/cgi-bin/hi3510/param.cgi?cmd=setinfrared&cururl=http%3A%2F%2F192.168.1.118%2Fdisplay.html&-infraredstat="+self.s
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
		choice = input("Current RTSP: "+url+";\nChange it?[y/n]")
		if (choice == 'n'):
			return url
		if (choice == 'y'):
			url = input("Print new RTSP: ")
			SerializeRTSP(url)
			return url
	
	def DeserializeRTSP(self):
		with open('data.csv', newline='') as f:
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