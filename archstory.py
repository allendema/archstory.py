#!/usr/bin/python3

from bs4 import BeautifulSoup
from time import sleep
import requests
import os

query = input("Enter a username: ")
url = "https://www.insta-stories.com/en/stories/"

mix = url + str(query)
print(mix)

path = query
try:
	os.mkdir(path)
except FileExistsError:
	print("This user has a folder in your System.")

os.chdir(path)


r = requests.get(mix) # Will add headers in the future.

if r.ok:
	print("\033[1;32;40m The site to get IG stories is Responding :)  \n")
	
else:
	print("\033[31m Connection not established!")
	
soup = BeautifulSoup(r.content, "html.parser")

stories = soup.find_all("div", class_ = "story", src="")
sleep(0.5)

# This uses an external site to get to the Story links.
# Media will be donwloaded from the servers of IG, which are not privacy friendly.

try:
	for story in stories:
		file_url = story.a["onclick"]
		replacer = file_url.replace("window.download('", "").replace("'); return false;", "")
		file_name = replacer.split("&")[-5].replace("_nc_ohc=", "")[:7]
		
		#print(file_url)
	
		print(replacer)
			
		r = requests.get(replacer, stream=True)

		if r.status_code == 200:
			with open(file_name, 'wb') as f:
				for chunk in r:
					f.write(chunk)
				print(f"\033[33m\nGetting stories of:\033[33m @{query}")
		else:
			print("Cannot make connection to download media!")
		
except KeyError:
	print("This user has no Stories in the last 24h.")
except KeyboardInterrupt:
	print("You are stoppping me...!")
	while True:
		sys.exit()
else:
	print("\nAt least one Story found. Successfully Downloaded.")
