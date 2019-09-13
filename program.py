import sys
import csv
import cv2
import keyboard
import requests
import time
import urllib.request
import urllib.request as urllib2
import os
import numpy as np

from tkinter import *
from enum import Enum
from requests import get
from PIL import Image, ImageOps


def nothing(x):
    pass

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

		#choose color
		#cv2.namedWindow("Tracking")
		#cv2.createTrackbar("Red", "Tracking", 0, 255, nothing)
		#cv2.createTrackbar("Green", "Tracking", 0, 255, nothing)
		#cv2.createTrackbar("Blue", "Tracking", 0, 255, nothing)

		#middle_screen_x = 600;
		#middle_screen_y = 350;
		#range_size = 20;

		while True:

			ret, frame = cap.read()

			#analisis
			'''
			hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

			r = cv2.getTrackbarPos('Red','Tracking')
			g = cv2.getTrackbarPos('Green','Tracking')
			b = cv2.getTrackbarPos('Blue','Tracking')

			hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 
			lower_red = np.array([r-50,g-50,b-50]) 
			upper_red = np.array([r+50,g+50,b+50]) 

			mask = cv2.inRange(hsv, lower_red, upper_red) 
			bmask = cv2.GaussianBlur(mask, (5,5),0)
			
			moments = cv2.moments(bmask)
			m00 = moments['m00']
			x, y = 600, 350
			if m00 != 0:
				x = int(moments['m10']/m00)
				y = int(moments['m01']/m00)

			res = cv2.bitwise_and(frame,frame, mask=bmask)
			cv2.imshow("Camera", res)

			if x <= 580:
				cc.Rotate('left')
				continue
			if x >= 620:
				cc.Rotate('left')
				continue
			if y <= 320:
				cc.Rotate('up')
				continue
			if y >= 370:
				cc.Rotate('down')
				continue
			cc.Rotate('stop')
			'''
			cv2.imshow("Camera", frame)

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

	IP = '' 
	s = '' #infraRedLompState (can be open/close)

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
		choice = input("Current RTSP: "+url+";\nChange it?[y/n]")
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



Program.Main() #Start point
