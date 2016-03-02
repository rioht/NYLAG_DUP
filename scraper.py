#!/usr/bin/env python

import sys
import requests
import StringIO
import os
from time import sleep
from bs4 import BeautifulSoup


"""
Scraper

  Should step through the directories located at http://boards.law.af.mil/
  and download the documents. 

  File Types:
  .txt
  .doc
  .pdf
  .rtf

  Relevant URLS:

  http://boards.law.af.mil/					General Overview URL

  http://boards.law.af.mil/AF_DRB.htm 		US Air Force Discharge Review Board
  	Air Force:								FD-2008-00305.pdf

  http://boards.law.af.mil/ARMY_DRB.htm 	US ARMY Discharge Review Board
  	Army:									AR20120000555.txt

  http://boards.law.af.mil/NAVY_DRB.html    US Navy Discharge Review Board
  	Marines:								MD1000002.rtf
  	Navy:									ND1100002.rtf

  http://boards.law.af.mil/CG_DRB.html      US Coast Guard Discharge Review Board
  	Coast Guard:							2013 001.pdf


"""
# Supporting Functions #

def url_decode(foo):

	try:

		xx = foo.replace("%20", " ")
		yy = xx.replace("%28", "(")
		decoded_url = yy.replace("%29", ")")

	except:

		pass

	return decoded_url


# Functions #

def usar_scrape():
	year = str(sys.argv[2])
	sess = requests.Session()
	adapter = requests.adapters.HTTPAdapter(max_retries=10)
	sess.mount("http://boards.law.af.mil/ARMY_DRB_CY" + year + ".htm", adapter)
	r = requests.get("http://boards.law.af.mil/ARMY_DRB_CY" + year + ".htm")
	z = r.text
	soup = BeautifulSoup(z, "html.parser")
	zz = soup.find_all('a')
	os.makedirs('USARCY' + year)
	os.chdir('USARCY' + year)

	for x in zz:

		file_link = 'http://boards.law.af.mil/' + x['href']
		foo = x['href']

		convert_foo = str(foo[-17:])
		print convert_foo
		
		if file_link.endswith('txt'):
			file_download = requests.get(file_link)
			holder = StringIO.StringIO()
			holder.write(file_download.text)
			results = holder.getvalue().encode('utf-8')
			holder.close()

			with open(convert_foo, 'wb') as f:
				f.write(results)
				#sleep(2)

		else:
			print 'pass'

def uscg_scrape():

	year = str(sys.argv[2])
	sess = requests.Session()
	adapter = requests.adapters.HTTPAdapter(max_retries=10)
	decoded_url = "a string"

	if year == "2015":
		
		sess.mount("http://boards.law.af.mil/CG_DRB_" + year + " - Discharge Review Board (DRB) .htm", adapter)
		r = requests.get("http://boards.law.af.mil/CG_DRB_" + year + " - Discharge Review Board (DRB) .htm")
		z = r.text
		soup = BeautifulSoup(z, "html.parser")
		zz = soup.find_all('a')
		os.makedirs('USCGCY' + year)
		os.chdir('USCGCY' + year)

	else:
		print "nope"
		
		r = requests.get("http://boards.law.af.mil/CG_DRB_" + year + "%20-%20Discharge%20Review%20Board%20%28DRB%29.htm")
		z = r.text
		soup = BeautifulSoup(z, "html.parser")
		zz = soup.find_all('a')
		os.makedirs('USCGCY' + year)
		os.chdir('USCGCY' + year)

	for x in zz:

		file_link = 'http://boards.law.af.mil/' + x['href']
		foo = x['href']

		convert_foo = str(foo[-14:])
		print url_decode(convert_foo)

		# write a function needs to take the %001 and decode it.
		# is there a wget for python that I should be using?
		# check my reference texts for ideas on properly parsing PDFs

		if file_link.endswith('pdf'):

			file_download = requests.get(url_decode(file_link))
			holder = StringIO.StringIO()
			holder.write(file_download.text)
			results = holder.getvalue().encode('utf-8')
			holder.close()

			with open(url_decode(convert_foo), 'wb') as f:
				f.write(results)
				sleep(2)
		else:
			print 'pass'
		
def usmc_scrape():
	year = str(sys.argv[2])
	r = requests.get("http://boards.law.af.mil/ARMY_DRB_CY" + year + ".htm")
	z = r.text
	soup = BeautifulSoup(z, "html.parser")
	zz = soup.find_all('a')
	os.makedirs('USMCCY' + year)
	os.chdir('USMCCY' + year)

	for x in zz:

		file_link = 'http://boards.law.af.mil/' + x['href']
		foo = x['href']

		convert_foo = str(foo[-17:])
		url_decode(convert_foo)
		print decoded_url
		
		if file_link.endswith('txt'):
			file_download = requests.get(file_link)
			holder = StringIO.StringIO()
			holder.write(file_download.text)
			results = holder.getvalue().encode('utf-8')
			holder.close()

			with open(convert_foo, 'wb') as f:
				f.write(results)
				sleep(2)
		else:
			print 'pass'

def usnr_scrape():
	year = str(sys.argv[2])
	r = requests.get("http://boards.law.af.mil/ARMY_DRB_CY" + year + ".htm")
	z = r.text
	soup = BeautifulSoup(z, "html.parser")
	zz = soup.find_all('a')
	os.makedirs('USNRCY' + year)
	os.chdir('USNRCY' + year)

	for x in zz:

		file_link = 'http://boards.law.af.mil/' + x['href']
		foo = x['href']

		convert_foo = str(foo[-17:])
		print convert_foo
		
		if file_link.endswith('txt'):
			file_download = requests.get(file_link)
			holder = StringIO.StringIO()
			holder.write(file_download.text)
			results = holder.getvalue().encode('utf-8')
			holder.close()

			with open(convert_foo, 'wb') as f:
				f.write(results)
				sleep(2)
		else:
			print 'pass'

# Main #

if __name__ == '__main__':
	if sys.argv[1] == 'usar':
		var = usar_scrape()
	elif sys.argv[1] == 'uscg':
		var = uscg_scrape()
	elif sys.argv[1] == 'usmc':
		var = usmc_scrape()
	elif sys.argv[1] == 'usnr':
		var = usnr_scrape()
	else:
		print "implement other stuff here."
	print "job done"