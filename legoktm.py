#!usr/bin/python
#
# (C) Legoktm 2008-2011, MIT License
#
import wikipedia, pagegenerators, catlib
import re, sys
from wikipedia import *
#status updater
#syntax: legoktm.newstatus("Status", "User:Username/Status", "[y]es/[n]o prompt)
site = wikipedia.getSite()
def newstatus(status, page, prompt):
	site = wikipedia.getSite()
	statuspage = wikipedia.Page(site, page)
	print "Current status is " + statuspage.get()
	if statuspage.get() != status:
		if prompt == "y":
			ask = raw_input("Should we update your status to " + status + "? [y]es, [n]o ")
    			if ask == "y":
					summary = 'Updating my status'
    				statuspage.put(status, summary)
    	else:
    		summary = 'Updating my status'
    		statuspage.put(status, summary)
    else:
    		print "Don't have to update status,\nas it already is " + status
#shortcut for raw_input()
#syntax: legoktm.ri(text)
def ri(text):
	return raw_input(text)
#uploads source code to wiki
#variables: wikipage=page to upload code to and code=file code is in
#syntax: legoktm.upload(wikipage, code)
def upload(wikipage, code):
	prompt = raw_input("Should we update the code? [y]es, [n]o " )
	if prompt == "y":
		summary = 'Updating source'
		scriptpage = wikipedia.Page(site, wikipage)
        file = open(code, 'r')
        text = file.read()
        file.close()
        text = '<source lang="python">\n' + text + '</sou' + 'rce>' # Split to confuse MW parser
        if scriptpage.get() != text:
            scriptpage.put(text, summary)
	else:
		print "Source not updated"	
#adds certain text to a log page
#syntax: leogktm.log(pagecreated, logpage, newtext)
#input newtext as a variable
def log(page, log, newtext):
	logpage = Page(site, log)
	newtext = newtext + logpage.get()
	summary = 'Adding ' + page + ' to log'
	print summary
	logpage.put(newtext, summary)
	print "Done adding " + page + " to log."

#converts number to month
#needs to use a variable
#syntax: legoktm.month(var, newvar)
def month(var):
	if var == "1":
		var = "January"
	elif var == "2":
		var = "February"
	elif var == "3":
		var = "March"
	elif var == "4":
		var = "April"
	elif var == "5":
		var = "May"
	elif var == "6":
		var = "June"
	elif var == "7":
		var = "July"
	elif var == "8":
		var = "August"
	elif var == "9":
		var = "September"
	elif var == "10":
		var = "October"
	elif var == "11":
		var = "November"
	elif var == "12":
		var = "December"
	else:
		print "Their is no month with the number of " + var
	print var
	return var
#checks if a certain page exists, if it does, wikilink it
#syntax: legoktm.pagecheck("pagename")
def pagecheck(name):
	site = wikipedia.getSite()
	wppage = wikipedia.Page(site, name)
	if wppage.exists() == True:
		name = "[[" + name + "]]"
		print name + " exists."
	else:
		print name + "does not exist."
	return name
#unicodify	
def unicodify(text):
    if not isinstance(text, unicode):
        return text.decode('utf-8')
    return text
def wikilink(link):
	link = "[[" + link + "]]"
	return link
def delink(link):
	import re
	link = re.compile(r'\[\[(.*?)\]\]', re.IGNORECASE).sub(r'\1', str(link))
	return link
def templink(link):
	link = '{{' + link + '}}'
	return link
def delinktemp(link):
	import re
	link = re.compile(r'\{\{(.*?)\}\}', re.IGNORECASE).sub(r'\1', str(link))
	return link
def addsection(page, content, summary):
	site = wikipedia.getSite()
	wppage = wikipedia.Page(site, page)
	text = wppage.get()
	text = text + content
	wikipedia.showDiff(wppage.get(), text)
	try:
		page.put(text, summary, minorEdit=False)
	except wikipedia.NoPage:
		page.put(text, summary, minorEdit=False)
	except wikipedia.IsRedirectPage:
		return
	except, e:
		print "ERROR: Except was raised during writing"
		print e
		sys.exit()
