#!/usr/bin/env python3

import fitz
import re

doc = fitz.open("meet-program.pdf")

eventNum = None
eventName = None
heatNum = None
numHeats = None
stage = None
lane = None
team = None
relay = None
name = None
age = None
seedTime = None

firstIndent = "  "
secondIndent = "    "

# This doesn't work for events that don't have age groups: "#1 Girls 200 Yard Freestyle"
#!eventPattern = r"#(?P<eventNum>[0-9]+) (?P<gender>\w+) (?P<ageGroup>.+) (?P<distance>[0-9]+ \w+) (?P<stroke>.*)"
eventPattern = r"^#(?P<eventNum>[0-9]+) (?P<eventName>.+)"
headerPattern = r"(?P<header>Team|Relay|Lane|Seed Time|Age|Name)"
heatPattern = r"Heat *(?P<heatNum>[0-9]+) of (?P<numHeats>[0-9]+) *(?P<stage>\w+)"
heatContinuationPattern = r"Heat *(?P<heatNum>[0-9]+)"
relayNamePattern = r"(?P<name>[\w ,\.]+) (?P<age>[0-9]+)"
titlePattern = r".*Meet Program.*"

for page in doc:
	
	text = page.get_text("blocks")
	#print(text)
	
	for row in text:
		
		# A row is a tuple like this: (18.0, 82.0386734008789, 102.17560577392578, 90.0107421875, '#1 Girls 200 Yard Freestyle\n', 1, 0)
		# We only care about the string at index 4
		data = row[4]
		
		#!print(data.replace("\n", "\\n"))
		#!print()
		
		matches = re.findall(titlePattern, data)
		if matches != []:
			# Ignore the title line
			continue
		
		matches = re.findall(eventPattern, data)
		if matches != []:
			# Event line
			#!print(matches)
			#!print(line)
			matches = re.findall(eventPattern, data)
			#!print(matches)
			eventNum, eventName = matches[0]
			print()
			print("#{} - {}".format(eventNum, eventName))
		else:
			matches = re.findall(headerPattern, data)
			if matches != []:
				# Header line
				#!print(data)
				#!print(matches)
				# Do nothing with this right now. Eventually collect the headers for an event to know what to display
				pass
			else:
				matches = re.findall(heatPattern, data)
				if matches != []:
					# Heat line
					#!print(data.replace("\n", "\\n"))
					#!print(matches)
					#!print()
					fields = data.split("\n")
					#!print(fields, len(fields))
					
					heatStr = fields[0]
					matches = re.findall(heatPattern, heatStr)
					heatNum, numHeats, stage = matches[0]
					print()
					print("Heat {} of {}".format(heatNum, numHeats))
					
					if len(fields) == 7:
						# Relay individual line
						team, seedTime, age, name, lane = fields[1:6]
						print(firstIndent, lane, name, age, team, seedTime)
					elif len(fields) == 6:
						# For relays team = relay and name = team
						relay, seedTime, team, lane = fields[1:5]
						# Relay team line
						print(firstIndent, lane, team, relay, seedTime)
					else:
						print("Error! Can't parse: {}".format(data))
					
				else:
					#!print(data.replace("\n", "\\n"))
					#!print(data.split('\n'))
					fields = data.split('\n')
					
					if len(fields) == 3:
						# Relay name lines
						matches = re.findall(relayNamePattern, data)
						if matches != []:
							# Relay name line
							#!print(matches)
							for match in matches:
								name, age = match
								print(secondIndent, name, age)
					
					elif len(fields) == 5:
						# Relay team line
						relay, seedTime, team, lane = fields[:4]
						print(firstIndent, lane, team, relay, seedTime)
					elif len(fields) == 6:
						# Individual line
						team, seedTime, age, name, lane = fields[:5]
						print(firstIndent, lane, name, age, team, seedTime)
					elif len(fields) == 7:
						# Heat heading (for event that started on previous page)
						heatStr, team, seedTime, age, name, lane = fields[:6]
						matches = re.findall(heatContinuationPattern, heatStr)
						if matches != []:
							heatNum = matches[0]
							print()
							print("Heat {} of {}".format(heatNum, numHeats))
						
						# Individual line
						print(firstIndent, lane, name, age, team, seedTime)
						
					else:
						#!print(data.replace("\n", "\\n"))
						print(data.split('\n'))
				
