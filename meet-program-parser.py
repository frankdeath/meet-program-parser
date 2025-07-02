#!/usr/bin/env python3

import fitz
import re

doc = fitz.open("meet-program.pdf")

eventNum = None
eventName = None
heat = None
lane = None

# This doesn't work for events that don't have age groups: "#1 Girls 200 Yard Freestyle"
#!eventPattern = r"#(?P<eventNum>[0-9]+) (?P<gender>\w+) (?P<ageGroup>.+) (?P<distance>[0-9]+ \w+) (?P<stroke>.*)"
eventPattern = r"#(?P<eventNum>[0-9]+) (?P<eventName>.+)"
headerPattern = r"^ *(?P<header>Team|Relay|Lane|Seed Time|Age|Name)"

for page in doc:
	
	text = page.get_text()
	#print(text)
	
	for line in text.split("\n"):
		matches = re.findall(eventPattern, line)
		if matches != []:
			# Event line
			#!print(matches)
			#!print(line)
			matches = re.findall(eventPattern, line)
			#!print(matches)
			eventNum, eventName = matches[0]
			print(eventNum, eventName)
			
		matches = re.findall(headerPattern, line)
		if matches != []:
			# Header line
			#!print(matches)
			# Do nothing with this right now. Eventually collect the headers for an event to know what to display
			pass
		#!else:
		#!	print("!", line)
