import requests
import json
import time
from bs4 import BeautifulSoup

import re
from PIL import Image
import pytesseract
import pyscreenshot as ImageGrab

start = time.time()
payload = {'apikey': '709e37ac8788957'}

#This axis measurements varies. Manually fix it.
im=ImageGrab.grab(bbox=(50,342,400,715))  #50,342,400,715 (Loco) 50,242,420,515 (Brainbaazi)
im.save('screenshot.png')

filename = 'screenshot.png'
data = {}

def run_string():
	with open(filename,'rb') as f:
		global data
		r = requests.post('https://api.ocr.space/parse/image',files = {filename : f},data = payload)
		data = json.loads(r.text)
run_string()
print(data['ParsedResults'][0]['ParsedText'])
mac = data['ParsedResults'][0]['ParsedText'][:-3]

question = "".join(data['ParsedResults'][0]['ParsedText'].splitlines()[:-3])

# question = """Largest desert in India"""
# x,y,z = ["Thar","Sahara","thor"]

search_q = "https://www.google.co.in/search?q=" + question.replace('ELIMINATED','').strip().replace(" ","+")
	
x,y,z = mac.splitlines()[-3:]
response = requests.get(search_q)

soup = BeautifulSoup(response.text,'lxml')
#just = soup.text.lower().split()

just = re.findall(r'\b[a-z]{2,15}\b', soup.text.lower())

def first():
	cn =0
	first_q = x.lower().split()
	for occurance in first_q:
		cn+= just.count(occurance)
	#cn+=soup.text.count(x.lower())		
	return cn

def second():
	cn =0
	second_q = y.lower().split()
	for occurance in second_q:
		cn+= just.count(occurance)
	#cn+=soup.text.count(y.lower())	
	return cn

def third():
	cn =0
	third_q = z.lower().split()
	for occurance in third_q:
		cn+= just.count(occurance)
	#cn+=soup.text.count(z.lower())	
	return cn

count = [first(),second(),third()]
print(count)

print("\n\nTime taken: " + str(time.time()-start))
