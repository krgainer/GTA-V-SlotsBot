import contextlib
import pyautogui
import ctypes
import time
import csv
import pytesseract
import keyboard
from statistics import mode
from PIL import Image
from modules.DXKeyPresses import useKey
import re
user32 = ctypes.windll.user32
screenResolution = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

## User Variables
maxLoss = 50000
consecutiveSpins = 4

## Unit Variables
currentGame = ""
startingChips = 000
currentChips = 0
currentBet = 0
currentProfit = 0
minBet = 0
maxBet = 0
betInterval = 0

def main():
	global currentChips, currentBet, currentProfit, startingChips, currentGame, minBet, maxBet, betInterval
	while True:
		if keyboard.is_pressed("h"):
			currentChips = int(resolveChips())
			print(currentChips)
			gamerules = identifyGameRules(input("Please enter the name of the game you are playing.\n").lower().strip())
			minBet = int(gamerules[1])
			maxBet = int(gamerules[2])
			betInterval = int(gamerules[3])
			currentBet = minBet
			targetBet = identifyBestBet(currentChips, currentBet, consecutiveSpins)
			print(targetBet)
			if targetBet == maxBet:
				pressTab()
				currentBet = maxBet
			else:
				while targetBet != currentBet:
					pressSpace()
					if currentBet + betInterval > maxBet:
						currentBet = minBet
					else:
						currentBet += betInterval
				
			for _ in range(consecutiveSpins):
				pressEnter()
				time.sleep(7)
				currentChips = currentChips - currentBet
			print("Est. balance: ",currentChips)
			print("Est. profit: ",currentChips - startingChips)
			currentChips = int(resolveChips())
			print("Real balance: ",currentChips)
			print("Real profit: ",currentChips - startingChips)

def identifyGameRules(gameName):
	gameName = gameName.lower().strip()
	with open('machineData.csv',mode="r") as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		line_count = 0
		gameFound = False
		for row in csv_reader:
			with contextlib.suppress(Exception):
				if row[0] == gameName:
					print(f'{row[0]} has a minimum bet of {row[1]} with a maximum bet of {row[2]}, going up in intervals of {row[3]}.')
					gameFound = True
					return row
		if gameFound == False:
			print(f'Game {gameName} not found.')
			while True:
				createNewGame = input("Would you like to create a new game? (y/n)\n").lower().strip()
				if createNewGame == "":
					print("Please enter a valid response.")
				elif createNewGame == "y":
					return createNewGameRules(gameName)
				elif createNewGame == "n":
					return ["GameNotFound",0,0,0]

def createNewGameRules(gameName):
	newGameName = input("Please enter the name of the new game.\nYou can also press enter to use the initally provided name").lower().strip()
	if newGameName == "":
		newGameName = gameName
	newMinBet = re.sub('[^0-9]','', input("Please enter the minimum bet of the new game.\n").lower().strip())
	newMaxBet = re.sub('[^0-9]','', input("Please enter the maximum bet of the new game.\n").lower().strip())
	newBetInterval = re.sub('[^0-9]','', input("Please enter the bet interval of the new game.\n").lower().strip())
	with open('machineData.csv', mode='a') as csv_file:
		csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		csv_file.write('\n')
		csv_writer.writerow([newGameName, newMinBet, newMaxBet, newBetInterval])
	# Remove any blank lines from the CSV file
	with open('machineData.csv', mode='r') as csv_file:
		lines = csv_file.readlines()

	with open('machineData.csv', mode='w') as csv_file:
		for line in lines:
			if line.strip():
				csv_file.write(line)
	print("New game created. Return to GTA V in the next 5 seconds.")
	time.sleep(5)
	return [newGameName, newMinBet, newMaxBet, newBetInterval]

def identifyBestBet(currentChips, currentBet, consecutiveSpins):
	possibleBet = currentBet
	bestBet = currentBet
	while possibleBet <= maxBet:
		if (currentChips - (possibleBet*consecutiveSpins*5) >= (currentChips/4)):
			bestBet = possibleBet
		possibleBet = possibleBet + betInterval
	return bestBet

def resolveChips():
	global startingChips
	# Determine the number of chips
	# Return the number of chips
	chipValues = []
	xz = 5
	while xz != 0:
		screenshot = pyautogui.screenshot("currentBal.png",region=(1464,0, 450, 62))
		currentBalRaw = pytesseract.image_to_string(Image.open('currentBal.png'), lang='eng')
		currentBal = re.sub('[^0-9]','', currentBalRaw)
		if currentBal != "":
			xz -= 1
			chipValues += [currentBal]
		else:
			print("Weird ass OCR returned")
	print("OCR returned: ",chipValues)
	currentBal = mode(chipValues)
	if startingChips == 0:
		startingChips = int(currentBal)
	return currentBal


def pressEnter():
	# Press the enter key
	useKey(0x1C)
	time.sleep(.5)

def pressTab():
	# Press the tab key
	useKey(0x0F)
	time.sleep(.5)

def pressSpace():
	# Press the space key
	useKey(0x39)
	time.sleep(.5)


main()