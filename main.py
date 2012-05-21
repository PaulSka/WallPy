# -*- coding: utf-8 -*-
import mechanize
import random
import re
from BeautifulSoup import BeautifulSoup
import os
import time
import config
import pickle

#Random seed	
random.seed()

global mBrowser

# Setup mechanize Browser
mBrowser = mechanize.Browser()
mBrowser.set_handle_robots(False)
#Use some user-agent
mBrowser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]


def fetchWallbase():
	"""
	Fetching wallbase.cc
	Return links
	"""
		
	#Open Url (##TODO set config for parameter)
	mBrowser.open("http://wallbase.cc/%s/0/%s%s%s/eqeq/0x0/0/%s%s%s/60/%s" %(config.WALLBASE_TYPE, config.WALLBASE_WG, config.WALLBASE_W, 
	config.WALLBASE_HR, config.WALLBASE_SWF, config.WALLBASE_SKETCHY, config.WALLBASE_NSFW, config.WALLBASE_TIME))

	links = []
	
	#Fetching links
	for link in mBrowser.links(url_regex="wallbase.cc/wallpaper/"):
		links.append(link.url)

	return links

def getUrl(linksUrl):
	"""
	Choose random links in linksUrl
	Return one Url
	"""

	def openWallpaperHistory():
		"""
		Open Wallpaper History
                """
                if not os.path.exists(config.WALLPAPER_HISTORY):
                        HISTORY = []
                        pickle.dump(HISTORY, open(config.WALLPAPER_HISTORY, "wb"))

                HISTORY = pickle.load(open(config.WALLPAPER_HISTORY))

		return HISTORY

	def checkWallpaper(wallpaperName, wallpaperHistory):
		"""
		Check if wallpaper is allready downloaded
		"""

		if wallpaperName in wallpaperHistory:
			return True
		else:
			wallpaperHistory.append(wallpaperName)
			pickle.dump(wallpaperHistory, open(config.WALLPAPER_HISTORY, "wb"))
			return False

	def randomUrl(linksUrl):
		"""
		Random links and get the first element
		"""
		randomUrl = random.sample(linksUrl, 1)[0]
		return randomUrl
	
	link = randomUrl(linksUrl)
	wallpaperHistory = openWallpaperHistory()
	while checkWallpaper(link, wallpaperHistory):
		link = randomUrl(linksUrl)
	return link
	
def getWallpaperUrl(randomUrl):
	"""
	Get the True Url from randomUrl
	Return url
	"""
	#Open the url and get the source wallpaper
	response = mBrowser.open(randomUrl)
	soup = BeautifulSoup(response.read())
	imgUrl = soup.find("div", { "id" : "bigwall" }).findNext('img')['src']
	return imgUrl
	
def saveWallpaper(imgUrl):
	"""
	Save the wallpaper from imgUrl
	Return Wallpaper name
	"""
	
	#Save the wallpaper
	response = mBrowser.open(imgUrl)
	wallpaperName = os.path.basename(imgUrl).replace('-', '')
	file = open(os.path.join(config.WALLPAPER_PATH, wallpaperName), "wb")
	file.write(response.get_data())
	file.close()
	return wallpaperName
	
while True:
	print "Fetching wallbase ..."
	links = fetchWallbase()
	print "Random links"
	link = getUrl(links)	
	print "Get source wallpaper ..."
	imgUrl = getWallpaperUrl(link)
	wallpaperName = saveWallpaper(imgUrl)
	print "Saving %s wallpaper" %wallpaperName
	time.sleep(config.TIMER)

