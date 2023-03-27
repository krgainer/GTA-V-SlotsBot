import pyautogui
import ctypes
import time
import csv
import pytesseract
from PIL import Image
import re
user32 = ctypes.windll.user32
screenResolution = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

## User Variables
maxLoss = 50000
consecutiveSpins = 10

## Unit Variables
currentGame = ""
startingChips = 000
currentChips = 0
currentProfit = 0
minBet = 0
maxBet = 0
betInterval = 0

def main():
	time.sleep(5)
	currentChips = resolveChips()
	print(currentChips)
	gamerules = identifyGameRules("diamond miner")
	minBet = gamerules[1]
	maxBet = gamerules[2]
	betInterval = gamerules[3]
	print(gamerules)
	

def identifyGameRules(gameName):
	gameName = gameName.lower()
	with open('machineData.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		line_count = 0
		gameFound = False
		for row in csv_reader:
			if row[0] == gameName:
				print(f'\t{row[0]} has a minimum bet of {row[1]} with a maximum bet of {row[2]}, going up in intervals of {row[3]}.')
				gameFound = True
				return row
		if gameFound == False:
			print(f'Game {gameName} not found.')
			return False

def resolveChips():
	global startingChips
	# Determine the number of chips
	# Return the number of chips
	screenshot = pyautogui.screenshot("currentBal.png",region=(1464,0, 450, 62))
	currentBalRaw = pytesseract.image_to_string(Image.open('currentBal.png'), lang='eng')
	currentBal = re.sub('[^0-9]','', currentBalRaw)
	if startingChips == 0:
		startingChips = currentBal
	return currentBal


def pressEnter():
	# Press the enter key
	pyautogui.press("enter")

def pressTab():
	# Press the tab key
	pyautogui.press("tab")

def pressSpace():
	# Press the tab key
	pyautogui.press("tab")

main()