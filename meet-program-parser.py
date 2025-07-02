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

for page in doc:
	
	text = page.get_text()
	#print(text)
	
	for line in text.split("\n"):
		if len(line) > 0 and line[0] == "#":
			# Event line
			#!print(line)
			matches = re.findall(eventPattern, line)
			#!print(matches)
			eventNum, eventName = matches[0]
			print(eventNum, eventName)
			
