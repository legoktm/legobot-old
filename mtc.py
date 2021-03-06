#!/usr/bin/python
"""

(C) Legoktm, 2008-2011

 Distributed under the terms of the MIT license.

__version__ = '$Id$'

Note: Still in development stage
Status: Approved for a 5 day trial
TODO: Convert to PythonWikiBot
"""
import urllib, re, time
import os, sys
sys.path.append(os.environ['HOME'] + '/stuffs/pywiki/pywikipedia')

import wikipedia, pagegenerators, catlib
from image import *
from upload import UploadRobot

#SITES
wikien = wikipedia.getSite(code = 'en', fam = 'wikipedia')
commons = wikipedia.getSite(code = 'commons', fam = 'commons')

#FIX ERRORS that CommonsHelper makes
def fixdescrip(des):
#	des = re.compile(r'\[\[wikipedia:Category:(.*?)\]\]', re.IGNORECASE).sub(r'[[Category:\1]]', name)
	des = re.compile(r'\[\[wikipedia:commons:Category:(.*?)\]\]', re.IGNORECASE).sub(r'[[Category:\1]]', des)
	des = re.compile(r'\[\[commons:Category:(.*?)\]\]', re.IGNORECASE).sub(r'[[Category:\1]]', des)
	des = re.compile(r'\[\[wikipedia:commons:(.*?)\]\]', re.IGNORECASE).sub(r'[[\1]]', des)
	des = re.compile(r'\[\[:en:commons:(.*?)\]\]', re.IGNORECASE).sub(r'[[\1]]', des)
	des = re.compile(r'index.php\?title=Image', re.IGNORECASE).sub(r'index.php?title=File', des)
	des = re.compile(r'\[http://en.wikipedia.org en.wikipedia\]', re.IGNORECASE).sub(r'[[:en:w|en.wikipedia]]', des)
	des = re.compile(r'was stated to be made', re.IGNORECASE).sub(r'was made', des)
	if re.search('category', des, re.I):
		des = re.compile(r'\{\{subst:Unc\}\} <!\-\- Remove this line once you have added categories \-\->', re.IGNORECASE).sub(r'', des)	
	if re.search(':en:category:', des, re.I):
		print 'NO CATEGORY FOUND!'
		return False
	if re.search('subst:Unc', des, re.I):
		print 'Uncategorized'
		return False
	return des
#Get the description from CH
def ch2(name):
	params = {
		'language'    : 'en',
		'image'       : name.titleWithoutNamespace(),
		'project'     : 'wikipedia',
		'username'    : 'Legobot',
		'doit'        : 'Get_text',
		}
	print 'The parameters are:\n%s' %(str(params))
	params = urllib.urlencode(params)
	f = urllib.urlopen("http://toolserver.org/~magnus/commonshelper.php", params)
	ch2text = f.read()
	f.close()
	tablock = ch2text.split('<textarea ')[1].split('>')[0]
	descrip = ch2text.split('<textarea '+tablock+'>')[1].split('</textarea>')[0]
	print 'Recieved info from CommonsHelper about %s:' %(name.title())
	descrip = fixdescrip(descrip)
	if descrip == False:
		return False
	print descrip
	time.sleep(15)
	return descrip

#Upload the image
def upload(name):
	descrip = ch2(name)
	if descrip == False:
		return False
	print 'Uploading %s to commons:commons.' %(name.title())
	#wikipedia.showDiff('', descrip)
	time.sleep(20)
	bot = UploadRobot(name.fileUrl(), description=descrip, useFilename=name.fileUrl(), keepFilename=True, verifyDescription=False, targetSite = commons)

	bot.run()
	print '%s was uploaded to commons:commons.' %(name.title())
		
#	except:
#		log = open('ErrorLog.txt', 'r')
#		logtext = log.read()
#		log.close()
#		log = open('ErrorLog.txt', 'w')
#		print 'An error occured while trying to upload %s' %(str(name))
#		log.write(logtext + '\nAn error occured while trying to upload %s' %(str(name)))
#		log.close()
#		return False
#Edit enwiki page to reflect movement

def ncd(name):
	name = name.title()
	page = wikipedia.Page(wikien, name)
	wikitext = page.get()
	state0 = wikitext
	wikitext = re.compile(r'\{\{Commons ok\}\}', re.IGNORECASE).sub(r'', wikitext)
	wikitext = re.compile(r'\{\{Copy to Wikimedia Commons\}\}', re.IGNORECASE).sub(r'', wikitext)
	wikitext = re.compile(r'\{\{Move to commons\}\}', re.IGNORECASE).sub(r'', wikitext)
	wikitext = re.compile(r'\{\{To commons\}\}', re.IGNORECASE).sub(r'', wikitext)
	wikitext= re.compile(r'\{\{Copy to Wikimedia Commons by BotMultichill\}\}', re.IGNORECASE).sub(r'', wikitext)
	if '{{Now' in wikitext:
		print '{{subst:ncd}} already added, will only remove {{mtc}} template.'	
	else:
		wikitext = '{{subst:ncd}}\n' + wikitext
	wikipedia.showDiff(state0, wikitext)
	time.sleep(15)
	page.put(wikitext, u'File is now available on Wikimedia Commons.')
def moveimage(name):
	#HACK
	name = str(name)
	name = name.title()
	name = wikipedia.ImagePage(wikien, name)
	if wikipedia.Page(commons, name.title()).exists():
		print '%s is already on the commons.' %(name.title())
		ncd(name)
		return
	uploadres = upload(name)
	if uploadres == False:
		return False
	ncd(name)




#Use the gen and go!
def findimages():
	wikien = wikipedia.getSite(code = 'en', fam = 'wikipedia')
	commons = wikipedia.getSite(code = 'commons', fam = 'commons')
	transclusionPage = wikipedia.Page(wikien, 'Template:Commons ok')
	gen = pagegenerators.ReferringPageGenerator(transclusionPage, onlyTemplateInclusion = True)
#	category = catlib.Category(wikien, 'Copy to Wikimedia Commons')
#	gen = pagegenerators.CategorizedPageGenerator(category, recurse=True)
	for page in gen:
		if page.namespace() == 6:
			print page
			moveimage(page)
		else:
			print '%s is not in the image namespace.' %(str(page))
if __name__ == "__main__":
	try:
		findimages()
	finally:
		wikipedia.stopme()
