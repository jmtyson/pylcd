#!/usr/bin/python
#Pyserial is used to talk to the LCD using the TX pin of the Raspberry Pi
import serial
#used to pack variable number commands for serial to use
import struct
#the time module is used for the sleep function, this gives the LCD screen time to process incoming commands.
import time
#Python Imaging Library is used to process 5X8 black on white pictures to use as custom characters.
from PIL import Image

"""
Author: Jeffrey McClain Tyson
Date: 6/27/2014
Name: pyrasplcd
Purpose: This python module is used to talk to the Parallax Serial LCD module (based on the 2x16 version, 4x20 is untested).  
Using this module you have access to the three different baud rates (2,400; 9,600; 19,200) for control of the screen.  
Features:
Turn the back light on and off (If your model allows it)
Clear the Screen
Set note scale and length in order to play sounds (If your model allows it)
Set and display using made characters
Change the cursor mode

Future Additions: A class for Adafruits USB/Serial back pack LCD screen for dual screen use.
"""
class ParallaxLCD:

	serial = None

	#The only constructor for ParallaxLCD.  Must provide a baud rate this device is set to.
	#mode: The mode is based on the dip switches on the back of the LCD screen.  Mode must be a integer.
	def __init__(self, mode):
		if mode == 0:
			self.serial = serial.Serial('/dev/ttyAMA0', 2400)
		elif mode == 1:
			self.serial = serial.Serial('/dev/ttyAMA0', 9600)
		elif mode == 2:
			self.serial = serial.Serial('/dev/ttyAMA0', 19200)
	
	#backLightOn method will turn the back light on.
	def backLightOn(self):
		self.serial.write('\x11')
		time.sleep(.05)
	
	#backLightOff method will turn the back light off.
	def backLightOff(self):
		self.serial.write('\x12')
		time.sleep(.05)
	
	#clearScreen method will clear the screen.
	def clearScreen(self):
		self.serial.write('\x0C')
		time.sleep(.05)
	
	#setScale method will set the scale the speaker will play in.
	#scale: This integer sets the scale the speaker will play.
	def setScale(self, scale):
		#220Hz
		if scale == 3:
			self.serial.write('\xD7')
		#440Hz
		elif scale == 4:
			self.serial.write('\xD8')
		#880Hz
		elif scale == 5:
			self.serial.write('\xD9')
		#1760Hz
		elif scale == 6:
			self.serial.write('\xDA')
		#3520Hz
		elif scale == 7:
			self.serial.write('\xDB')
		time.sleep(.05)
	
	#setNoteLenth will set how long the note will be held.
	#length: This string is used to set how long a not will be held.
	def setNoteLenth(self, length):
		if length == '1/64':
			self.serial.write('\xD0')
		elif length == '1/32':
			self.serial.write('\xD1')
		elif length == '1/16':
			self.serial.write('\xD2')
		elif length == '1/8':
			self.serial.write('\xD3')
		elif length == '1/4':
			self.serial.write('\xD4')
		elif length == '1/2':
			self.serial.write('\xD5')
		elif length == '1':
			self.serial.write('\xD6')
		time.sleep(.05)
	
	#playNote will play a note through the build in speaker.
	#note: A string used to tell which note to play.
	def playNote(self, note):
		if note == 'A':
			self.serial.write('\xDC')
		elif note == 'A#':
			self.serial.write('\xDD')
		elif note == 'B':
			self.serial.write('\xDE')
		elif note == 'C':
			self.serial.write('\xDF')
		elif note == 'C#':
			self.serial.write('\xE0')
		elif note == 'D':
			self.serial.write('\xE1')
		elif note == 'D#':
			self.serial.write('\xE2')
		elif note == 'E':
			self.serial.write('\xE3')
		elif note == 'F':
			self.serial.write('\xE4')
		elif note == 'F#':
			self.serial.write('\xE5')
		elif note == 'G':
			self.serial.write('\xE6')
		elif note == 'G#':
			self.serial.write('\xE7')
		else:
			self.serial.write('\xE8')
	
	#setCustChat takes a 5x8 black on white picture and turns it into a character.
	#customSlot: The space in memory used to store the character (0-7).
	#chrFile: The picture file used to load into memory.
	def setCustChar(self, customSlot, chrFile):
		if customSlot > 7:
			print "Please use only 0 through 7 for a custom slot"
			pass
		
		picture = Image.open(chrFile)
		pictureSize = picture.size
		pixelList = []
		
		for y in range(pictureSize[1]):
			pixelRow = [0,0,0]
			for x in range(pictureSize[0]):
				pixel = picture.getpixel((x,y))
				if pixel == (0,0,0):
					pixelRow.append(1)
				else:
					pixelRow.append(0)
			pixelList.append(pixelRow)
		
		self.serial.write(struct.pack('B', 248+customSlot))
		for position in range(len(pixelList)):
			custByte = str(''.join(map(str,pixelList[position])))
			custByte= int(custByte, 2)
			self.serial.write(struct.pack('B', custByte))
	
	#dispCustChar displays the custom character added using the setCustChar function
	#customSlot: The slot in memory where the wanted character is at.
	def dispCustChar(self, customSlot):	
		self.serial.write(struct.pack('B', 0+customSlot))
	
	#cursorGoTo allows a user to move the cursor at a needed spot.
	#line: This integer is the line you want to move to.
	#column: This integer is the column position you want to move to.
	def cursorGoTo(self, line, column):
		position = 128
		if(line > 3 and line < 0) and (column > 19 and column < 0):
			pass
		else:
			if(line == 1):
				position = (position +  20) + column
			elif(line == 2):
				position = (position +  40) + column
			elif(line == 3):
				position = (position +  60) + column
			else:
				position = position + column
		self.serial.write(struct.pack('B', position))
		time.sleep(.05)
	
	#turnOff turns the LCD screen off.
	def turnOff(self):
		self.serial.write('\x15')
		time.sleep(.05)
	
	#turnOn turns the LCD screen on, and allows a user to pick how the screen shows a cursor.
	#mode: mode is a integer that allows a user to pick how a cursor shows on screen.
	def turnOn(self, mode):
		#Mode 0 Turns the display on, with cursor off and no blinking box
		if mode == 0:
			self.serial.write('\x16')
		#Mode 1 Turns the display on, with cursor off and a blinking box
		elif mode == 1:
			self.serial.write('\x17')
		#Mode 2 Turns the display on, with cursor on and no blinking box
		elif mode == 2:
			self.serial.write('\x18')
		#Mode 3 Turns the display on, with cursor on and a blinking box
		elif mode == 3:
			self.serial.write('\x19')
		else:
			pass
	
	#sendText prints text to the LCD screen based on where the cursor currently is.
	#text: A string that is printed to the LCD screen.
	def printText(self, text):
		self.serial.write(text.encode())
	
	#sendTextAtLine allows a user to print text at a given line.
	#line: A integer that lets you pick the line to print to starting at the beginning of that line.
	#text: A string printed to the LCD screen.
	def printTextAtLine(self, line, text):
		self.cursorGoTo(line,0)
		self.printText(text)

