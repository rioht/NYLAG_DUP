
import os
import csv
import re
import sys
import StringIO
import datetime

# Notes #

"""
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

# Metadata #

#name           type			description

keys = [

'DocNUM',		#01 alphanumeric	Docket Number
'AppRec',		#02 date			Date Application was Submitted
'Branch',		#03 text			Branch of Service
'NJP',			#04 number			Non-Judicial Punishment
'Article',		#05 text			UCMJ Article cited with Non-Judicial Punishment
'MC: Prof',		#06 number			Marine Corps Proficiency Rating
'N: Perf',		#07 Number			Navy Performance Rating
'N: Beh',		#08 number			Navy Behavioral Rating
'N: OTA',		#09 number			Navy Performance Rating Information
'LOS',			#10 alphanumeric	Length of Service up to date of discharge
'EnlTERM',		#11 number			Term of enlistment at date of discharge
'PriorDISCH',	#12 text			Prior Dishcarges before recent discharge
'DischAUTH',	#13 text			Authority for discharge to be changed
'OrgCHAR',		#14 text			Original Discharge Characterization
'OriNAR',		#15 text			Original Narrative for Discharge
'OriREC',		#16 alphanumeric	Original Reenlistment Code
'CurCHAR',		#17 text			Current Discharge Characterization
'CurNAR',		#18 text			Current Narrative for Discharge
'CurREC'		#19 alphanumeric	Current Reenlistment Code

]

"""
functions to be written:

1.  scan directory and check files
2.  make queries in file
3.  append (open and create a csv sometime, duh) the results to a spreadsheet.
"""
# Functions - Assisting Functions #

#ARMY

def USAR_SCAN(foo):
	datum = []
	content = open(foo, "r")
	raw = content.read()
	holder = StringIO.StringIO()
	holder.write(raw)
	text = holder.getvalue()#.encode('utf-8')
	holder.close()

	# 01 alphanumeric	Docket Number

	try:

		datum.append(str(foo))

	except Exception as e:

		print e
		print "Error on 01"
		datum.append("ERROR")

	# 02 date			Date Application was Submitted

	try:

		AppRec1 = re.findall(r'Application Date:  (.*)', text)
		AppRec2 = re.findall(r'Application Receipt Date:(.*\s)', text)
		AppRec3 = re.findall(r'Application Date:\t(.*)', text)

		if len(AppRec1) == 1:
			datum.append(AppRec1[0].strip())
		elif len(AppRec2) == 1:
			datum.append(AppRec2[0].strip())
		elif len(AppRec3) == 1:
			datum.append(AppRec3[0].strip())
		else:
			datum.append("ERROR")

	except Exception as e:

		print e
		print "Error on 02"
		datum.append("ERROR")

	#03 text			Branch of Service

	try:

		BranchAR = re.search(r'Army Discharge Review Board', text, flags=re.IGNORECASE)


		if BranchAR.group(0) == 'Army Discharge Review Board':
			datum.append("USAR")
		else:
			datum.append("ERROR")

	except:

		print e
		print "Error on 03"
		datum.append("ERROR")

	#04 number			Non-Judicial Punishment

	try:

		#njp15 = 
		datum.append("Placeholder04")

	except Exception as e:

		print e
		print "Error on 04"
		datum.append("ERROR")
			
	#Find Article 15s, but exclude those after Legend:

	#05 text			UCMJ Article cited with Non-Judicial Punishment

	datum.append("Placeholder05")
	
	#06 number			Marine Corps Proficiency Rating

	datum.append("NA.06")
			
	#07 Number			Navy Performance Rating

	datum.append("NA.07")

	#08 number			Navy Behavioral Rating

	datum.append("NA.08")
			
	#09 number			Navy Performance Rating Info

	datum.append("NA.09")

	#10 alphanumeric	Length of Service up to date of discharge

	try:

		slength1 = re.findall(r'h. Total Service:(.*)', text)

		if len(slength1) == 1:
			datum.append(slength1[0].strip())

		else:

			try:
				
				slength2 = re.findall(r'Highest Grade Achieved/MOS/Total Service:(.*)', text)
				
				if len(slength2) == 1:

					slength2split = str.split(slength2[0], '/')
					datum.append(slength2split[-1])

				else:

					try:
						
						slength3 = re.findall(r'Total Service:(.*)', text)
						
						if len(slength3) == 1:

							datum.append(slength3[0].split())

						else:

							datum.append("ERROR")

					except Exception as e:

						print e
						print "Error on 10"
						datum.append("ERROR")

			except Exception as e:

				print e
				print "Error on 10"
				datum.append("ERROR")


	except Exception as e:

		print e
		print "Error on 10"
		datum.append("ERROR")


	#11 number			Term of enlistment at date of discharge

	try:

		enlength1 = re.findall(r'Date/Period of Enlistment:(.*)', text)

		if len(enlength1) == 1:
			datum.append(enlength1[0])

		else:

			try:
				
				enlength2 = re.findall(r'Current Enlistment Date/Term:(.*)', text)

				if len(enlength2) == 1:
					datum.append(enlength2[0].strip())

				else:

					try:

						enlength3 = re.findall(r'Date/Period of Entry on Active Duty:(.*)', text)

						if len(enlength3) == 1:
							datum.append(enlength3[0])

					except Exception as e:

						print e
						print "Error on 11"
						datum.append("ERROR")

			except Exception as e:

				print e
				print "Error on 11"
				datum.append("ERROR")


	except Exception as e:

		print e
		print "Error on 11"
		datum.append("ERROR")

	#12 text			Prior Dishcarges before recent discharge

	try:

		priord1 = re.findall(r'Previous Discharges:(.*)', text)
		
		if len(priord1) == 1:

			datum.append(str.replace(priord1[0].strip(), '\t', ' '))

		else:

			try:

				priord2 = re.findall(r'Prior Service/Characterizations:(.*)', text)

				if len(priord2) == 1:

					datum.append(str.replace(priord2[0].strip(), '\t', ' '))

			except Exception as e:

				print e
				print "Error on 12"
				datum.append("ERROR")

	except Exception as e:

		print e
		print "Error on 12"
		datum.append("ERROR")

	#13 text			Authority for discharge to be changed

	try:

		audich1 = re.findall(r'Date of Discharge:(.*)', text, flags=re.IGNORECASE)

		if len(audich1) > 0:

			date = audich1[0].strip()

			then = datetime.datetime.strptime(date, "%d %B %Y")

			now = datetime.datetime.now()

			diff = now - then

			demarcation = datetime.timedelta(days=5475)

			if diff < demarcation:

				datum.append("DRB")

			else:

				datum.append("BCMR")

		else:

			datum.append("ERROR")

	except Exception as e:

		print e
		print "Error on 13"
		datum.append("ERROR")

	#14 text			Original Discharge Characterization

	try:

		ogdich1 = re.findall(r'Discharge Received:(.*)', text, flags=re.IGNORECASE)
		
		try:


			if len(ogdich1) >= 1:

				datum.append(ogdich1[0].strip())

			else:

				try:

					ogdich2 = re.findall(r'Separation Decision Date/Characterization:(.*)', text)
					
					if len(ogdich2) >= 1:

						ogdich2split = str.split(ogdich2[0], '/')
						datum.append(ogdich2split[-1].strip())

					else:
						
						datum.append("ERROR")

				except Exception as e:

					print e
					print "Error on 14"
					datum.append("ERROR")

					
		except Exception as e:

			print e
			print "Error on 14"
			datum.append("ERROR")
			
	except Exception as e:

		print e
		print "Error on 14"
		datum.append("ERROR")

	#15 text			Original Narrative for Discharge

	try:
		
		ognarr1 = re.findall(r'Reason/Authority/SPD/RE Code:(.*)', text)

		if len(ognarr1) == 1:

			datum.append(str.replace(ognarr1[0].strip(), '\t', ''))

		else:

			try:

				ognarr2 = re.findall(r'Reason/Authority/Codes/Characterization:(.*)', text)

				if len(ognarr2) >= 1:

					datum.append(ognarr2[0].strip())

				else:

					try:

						ognarr3 = re.findall(r'Reason/Authority/SPD/RE:(.*)', text)

						if len(ognarr3) > 0:

							datum.append(ognarr3[0].strip())

						else:

							datum.append("ERROR")

					except Exception as e:

						print e
						print "Error on 15"
						datum.append("ERROR")

			except Exception as e:

				print e
				print "Error on 15"
				datum.append("ERROR")

	except Exception as e:

		print e
		print "Error on 15"
		datum.append("ERROR")

	#16 alphanumeric	Original Reenlistment Code

	try:

		ogreco1 = re.findall(r'Reason/Authority/SPD/RE Code:(.*)', text)

		if len(ogreco1) == 1:

			ogreco1RE = re.findall(r'\bRE-\d\b', text)
			datum.append(ogreco1RE[0].strip())

		else:

			try:

				ogreco2 = re.findall(r'Reason/Authority/SPD/RE:(.*)', text)

				if len(ogreco2) == 1:

					ogreco2RE = re.findall(r'\bRE-\d\b', text)
					datum.append(ogreco2RE[0].strip())

				else:

					try:

						ogreco3 = re.findall(r'Reason/Authority/Codes/Characterization:(.*)', text)

						if len(ogreco3) == 1:

							try:

								ogreco3RE = re.findall(r'\bRE-\d\b', text)
								datum.append(ogreco3RE[0].strip())

							except Exception as e:

								#print e
								#print "Error on 16"
								datum.append("ERROR")

						else:

							datum.append("ERROR")

					except Exception as e:

						print e
						print "Error on 16"
						datum.append("ERROR")

			except Exception as e:

				print e
				print "Error on 16"
				print datum.append("ERROR")

	except Exception as e:

		print e
		print "Error on 16"
		datum.append("ERROR")

	#17 text			Current Discharge Characterization

	try:

		cudich1 = re.findall(r'Change Characterization to:(.*)', text, flags = re.IGNORECASE)

		if len(cudich1) == 1:
			datum.append(cudich1[0].strip())

		else:

			datum.append("ERROR")

	except Exception as e:

		print e
		print "Error on 17"
		datum.append("ERROR")

	#18 text			Current Narrative for Discharge

	try:

		cunadi1 = re.findall(r'Change Reason to:(.*)', text, flags = re.IGNORECASE)

		if len(cunadi1) == 1:
			datum.append(cunadi1[0].strip())

		else:

			datum.append("ERROR")

	except Exception as e:

		print e
		print "Error on 18"
		datum.append("ERROR")

	#19 alphanumeric	Current Reenlistment Code

	try:

		cureco1 = re.findall(r'Change RE Code to:(.*)', text, flags = re.IGNORECASE)

		if len(cureco1) == 1:
			datum.append(cureco1[0].strip())

		else:

			try:

				cureco2 = re.findall(r'Change SPD/RE Code to:(.*)', text, flags = re.IGNORECASE)
				

				if len(cureco2) == 1:
					datum.append(cureco2[0].strip())

				else:

					try:

						cureco3 = re.findall(r'Change RE-Code to:(.*)', text, flags = re.IGNORECASE)

						if len(cureco3) == 1:
							datum.append(cureco3[0].strip())

						else:

							try:

								cureco4 = re.findall(r'SPD/RE Code Change to:(.*)', text, flags = re.IGNORECASE)

								if len(cureco4) == 1:
									datum.append(cureco4[0].strip())

								else:

									datum.append("ERROR")

							except Exception as e:

								print e
								print "Error on 19"
								datum.append("ERROR")
				
					except Exception as e:

						print e
						print "Error on 19"
						datum.append("ERROR")

			except Exception as e:

				print e
				print "Error on 19"
				datum.append("ERROR")

	except Exception as e:

		print e
		print "Error on 19"
		datum.append("ERROR")

	# Clear array for next file check

	print "\n"
	print datum
	
	append_csv("placeholder", datum)
	#return datum

	"""
			#regex patterns go here - just do a regex, then store in array
			for line in content:
				if "Application" in line:
					print line
	"""

# regex functions here #

# make a list of all rtf, text, and pdf files

# main function #


def scan_directory():

	open_csv("placeholder")

	file_list = os.listdir(os.getcwd())

	for file in file_list:

		if file.endswith('.txt'):
			#print "Text file identified, calling ARMY parsing function."
			USAR_SCAN(file)
			#append_csv("placeholder", datum)
		else:

			#what to do if no files found
			print file + " is not a valid file type...scanning for next file."


			"""
				for line in content:

					if "Application Receipt Date:" in line:
						print line

					else:

						datum.append("FAIL")
			"""

			print "Finished reading directory: Scanned " + str(len(file_list)) + " total files."


def open_csv(foo):
	with open(foo + '.csv', 'wb') as f:
		writer = csv.writer(f, delimiter = ',')
		writer.writerow(keys)

def append_csv(foo, source):
	with open(foo + '.csv', 'a') as f:
		writer = csv.writer(f, delimiter = ',')
		writer.writerow(source)
		source = []


def open_catalog_csv(foo):
	with open(foo + '.csv', 'wb') as f:
		writer = csv.writer(f, delimiter = ',')
		writer.writerow(keys)

def get_folders_count(foo):

	if foo <= 20:
		var_folders = 1
	else:
		if foo % 20 == 0:
			var_folders = foo / 20
		else:
			var_folders = (foo / 20) + 1

	return var_folders

def makedirs(foo):
	try:
		for i in xrange(1, foo, 1):
			os.makedirs(os.path.split(os.getcwd())[1] + " Vol. 0" + str(i))
	except Exception as e:
		print e
		pass

def sort_filelist():
	for dirName, subdirList, fileList in os.walk(os.getcwd()):
		filelist = [f for f in fileList if not f[0] == '.']
		if 'sort.csv' in fileList:
			fileList.remove('sort.csv')
		if 'sort.py' in fileList:
			fileList.remove('sort.py')
		sorted_list = sorted(filelist, key=os.path.getmtime)

		return sorted_list

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def copy_files(foo):
	count = 0
	dirs = []
	errorcheck = os.path.split(os.getcwd())
	for dirName, subdirList, fileList in os.walk(os.getcwd()):
		dirs.append(dirName)
		if os.getcwd() in dirs:
			dirs.remove(os.getcwd())
			"""
			To prevent files from being copied recursively,
			the following control flow stops the function.
			However, a folder is still created.
			"""
		if " Vol. 01" in errorcheck[1]:
			return

	for i in xrange(0, len(foo), 1):
		for ii in xrange(0, len(foo[i]), 1):
			if str(foo[i][ii]).lower().endswith('.mp3'):
				count = count + 1
				if count > 20:
					count = 1
				if count < 10:
					shutil.copy2(str(foo[i][ii]), dirs[i] + "/" + "0" + str(count) + " " + str(foo[i][ii]))
				else:
					shutil.copy2(str(foo[i][ii]), dirs[i] + "/" + str(count) + " " + str(foo[i][ii]))	

# Functions - Main Functions #

def catalog():
	count = 0
	dirs = []
	sourceData = []

	for dirName, subdirList, fileList in os.walk(os.getcwd()):
		dirs.append(dirName)
		if os.getcwd() in dirs:
			dirs.remove(os.getcwd())

	for directory in dirs:
		os.chdir(directory)
		open_catalog_csv(os.path.split(os.getcwd())[1])
		for dirName, subdirList, fileList in os.walk(os.getcwd()):
			fileList = [f for f in fileList if not f[0] == '.']
			for filename in fileList:
				if filename.endswith('.mp3') or filename.endswith('.MP3') \
				or filename.endswith('.Mp3') or filename.endswith('.mP3'):
					
					count = count + 1
					if count > 20:
						count = 1
					y = os.path.join(dirName, filename)
					af = eyed3.load(y)
					splitstring = str.split(filename, '_')
					if '.mp3' in splitstring[0]:
						splitstring = str.split(splitstring[0], '-')
					sourceData.append("WW") #territory
					sourceData.append(str.split(os.path.split(os.getcwd())[1])[0]) #genre
					sourceData.append("Songs of Love: " + str.replace(os.path.split(os.getcwd())[1], ' Vol.', ', Vol.')) #album title
					sourceData.append("Various Artists") #album artist
					capital = re.findall('[A-Z][^A-Z]*', splitstring[0])
					try:
						randomizer = random.sample(range(0, len(keywords)), 3)
						sourceData.append(capital[0] + " Loves " + keywords[(randomizer[0])] \
						+ "," + " " + keywords[(randomizer[1])] + "," + " " + \
						"and " + keywords[(randomizer[2])]) #track title
					except:
						sourceData.append("TITLE ERROR")
					try: #track artist
						splitstring2 = str.split(splitstring[1], '.mp3')
						singlestring = re.findall('[' '][aA-zZ]*', filename)
						if splitstring2[0][0].isupper() and splitstring2[0][1].isupper():
							sourceData.append(splitstring2[0][0] + '. ' + splitstring2[0][1:])

						elif splitstring2[0][0].isupper() and splitstring2[0][1] == '.':
							sourceData.append(splitstring2[0][0] + '. ' + splitstring2[0][2:])

						else:
							sourceData.append(splitstring2[0])

					except IndexError:
						# this section below to handle a few specific cases.
						try:

							if re.search(r'__', filename):
								double__split = re.findall('[' '][aA-zz]*', filename)
								double__split2 = str.split(double__split[3],'__')
								sourceData.append(double__split2[1])

							elif 'Wolfert' in filename:
								sourceData.append("Wolfert")

							elif '_' and '__' and '-' not in filename:
								nosymbolsplit = str.split(filename, '.')
								nosymbolsplit2 = re.findall('[A-Z][^A-Z]*', nosymbolsplit[0])
								sourceData.append(nosymbolsplit2[1])

							else:
								sourceData.append("TrackArtistPH")
								print "exception1"
								print filename
								print splitstring
								print splitstring2

						except:
							sourceData.append("TrackArtistPH")
							print "exception2"
							print filename
							print splitstring
							print splitstring2

					except:	
						sourceData.append("TrackArtistPH")
						print "exception3"

					sourceData.append(count) #sequence
					try:
						sourceData.append(af.info.time_secs) # duration
					except Exception as e:
						sourceData.append(0)
						print e
					sourceData.append("The Medicine of Music") # label
					sourceData.append("")
					sourceData.append("")
					sourceData.append("")
					sourceData.append("")
					sourceData.append("")
					sourceData.append("")
					append_csv(os.path.split(os.getcwd())[1], sourceData)
					sourceData = []

def organize():

	for dirName, subdirList, fileList in os.walk(os.getcwd()):
		fileList = [f for f in fileList if not f[0] == '.']
		if 'sort.csv' in fileList:
			fileList.remove('sort.csv')
		if 'sort.py' in fileList:
			fileList.remove('sort.py')
		if 'keywords.csv' in fileList:
			fileList.remove('keywords.csv')
		if os.getcwd() != dirName:
			os.chdir(dirName)
			if os.path.split(os.getcwd())[1] + '.csv' in fileList:
				fileList.remove(os.path.split(os.getcwd())[1] + '.csv')

			var_folders = get_folders_count(len(fileList))
			
			try:
				makedirs(var_folders + 1)
			except Exception as e:
				print e
				pass
			
			sorted_list = sort_filelist()
			chunked_list = list(chunks(sorted_list, 20))

			try:
				copy_files(chunked_list)
			except Exception as e:
				print e
				pass

			catalog()

# Main #

if __name__ == '__main__':
	#comment the two lines below for dev/actual vers
	#z = os.getcwd()
	#os.chdir(z + "/../../..")
	scan_directory()
	print "job done"
