#!/usr/bin/env python3

import fitz
import re

doc = fitz.open("meet-program.pdf")

event = None
heat = None
lane = None

for page in doc:
	
	text = page.get_text()
	#print(text)
	
	for line in text.split("\n"):
		if len(line) > 0 and line[0] == "#":
			# event line
			print(line)
