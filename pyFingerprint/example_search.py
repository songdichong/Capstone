#!/usr/bin/env python
# -*- coding: utf-8 -*-
#https://github.com/bastianraschke/pyfingerprint
'''
Original Author: bastianraschke
Weblink: https://github.com/bastianraschke/pyfingerprint
Last Updated Date: Feb 15, 2019
Contents of file:
	1. Search a fingerprint record
'''
"""
PyFingerprint
Copyright (C) 2015 Bastian Raschke <bastian.raschke@posteo.de>
All rights reserved.

"""

import hashlib
from pyfingerprint.pyfingerprint import PyFingerprint
import time
import requests
## Search for a finger
##
def search_fingerprint():
		## Tries to initialize the sensor
		try:
				f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
				#~ file1 =  open("loginstate.txt","a+")
				if ( f.verifyPassword() == False ):
						raise ValueError('The given fingerprint sensor password is wrong!')

		except Exception as e:
				print('The fingerprint sensor could not be initialized!')
				print('Exception message: ' + str(e))
				#~ exit(1)
		## Gets some sensor information
		print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))
				## Tries to search the finger and calculate hash
		try:
				print('Waiting for finger...')

				## Wait that finger is read
				while ( f.readImage() == False ):
						pass

				## Converts read image to characteristics and stores it in charbuffer 1
				f.convertImage(0x01)
				
				## Searchs template
				result = f.searchTemplate()
				print (result)
				positionNumber = result[0]
				accuracyScore = result[1]

				if ( positionNumber == -1 ):
						print('No match found!')
						#~ search_fingerprint()
					#~ exit(0)
				else:
						print('Found template at position #' + str(positionNumber))
						print('The accuracy score is: ' + str(accuracyScore))
				#~ file1.write(str(positionNumber)+'\n')
				url = "http://0.0.0.0:4310/login"
				data = {'userID': positionNumber}
				r = requests.post(url, data)
				## OPTIONAL stuff
				##
				## Loads the found template to charbuffer 1
				f.loadTemplate(positionNumber, 0x01)
				print("1")
				print(result)
				## Downloads the characteristics of template loaded in charbuffer 1
				characterics = str(f.downloadCharacteristics(0x01)).encode('utf-8')
				print("2")
				print(result)
				## Hashes characteristics of template
				print('SHA-2 hash of template: ' + hashlib.sha256(characterics).hexdigest())
				time.sleep(1)
				
		except Exception as e:
				print('Operation failed!')
				print('Exception message: ' + str(e))
				#~ exit(1)
		
		
if __name__=="__main__":
		search_fingerprint()
		
