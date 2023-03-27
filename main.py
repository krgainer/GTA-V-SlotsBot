import pyautogui
import ctypes
import time
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
startingBal = 0
currentBal = 0
currentProfit = 0


def main():
	time.sleep(5)
	print(resolveChips())
	

def currentGame(gameName):
	gameName = gameName.lower()



def resolveChips():
	# Determine the number of chips
	# Return the number of chips
	screenshot = pyautogui.screenshot("currentBal.png",region=(1464,0, 450, 62))
	currentBalRaw = pytesseract.image_to_string(Image.open('currentBal.png'), lang='eng')
	currentBal = re.sub('[^0-9]','', currentBalRaw)
	if startingBal == 0:
		startingBal = currentBal
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