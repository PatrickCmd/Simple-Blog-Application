import re


some_string = "Finding atleast 4 digit numbers in the string 2346, 1234, 903930303, 1673, 1234748, and 4568 even also 23, 123, 890"

regex_pattern = re.compile(r"\D(\d{4})\D") 

match_patterns = re.findall(regex_pattern, some_string)

print(match_patterns)

for match in match_patterns:
	print match, 
	# print(match )
print(" ")
print(" ")


""" Extracting Captilised words """

txt = "Can you find A Match with some words: Car, House, Shirt, Apple, Google, liverpool, manchester, Facebook, Arsenal, manu."
regex_patterns = re.compile(r"([A-Z]{1}[a-z]+)\s?")
matches = re.findall(regex_patterns, txt)

print matches
for match in matches:
	print match,
print " "
print " "



""" Captilised and Punctuated """
txt = "this is poor syntax"
txt2 = "This is good punctuated capitakized sysntax."

regex_pattern = re.compile(r"^[A-Z](.*)[\.\?\!]$")   
matches = re.findall(regex_pattern, txt2)
print(matches)
