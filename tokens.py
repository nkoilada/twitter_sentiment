import time
import sys
import re

ignore_regex = (
	
	#Twitter Usernames
	r"""(@[\w]+)"""
	,
	#Twitter Hashtags
	r"""(#[\w]+)"""
	,
	#URLs
	r"""(http[s]?://[\w_./]+)"""
	,
	#HTML Entities
	r"""(&[a-z]+;)"""
	#,
	#Non-Alphabet Word
	#r"""([^a-z^A-Z]+)"""
)

stop_list = [w.strip() for w in open("data/stop_words.txt","rb").readlines()]

def tokenize(text):
	for i in ignore_regex:
		text = re.sub(i, ' ', text)
	# Split by all alpha number characters except "`,-,_"
	tokens = re.split("[\s,.?!:)({}\"=*\[\]|;^<>~]+", text)
	filtered_tokens = set()
	for t in tokens:
			# Select only alphabetical words which can have "',-,_" in them. Length of word must be > 2.
			if re.match("(^[a-z][a-z'\-_]*[a-z]$)",t) is not None and t not in stop_list:
				filtered_tokens.add(t.lower())
	return filtered_tokens

if __name__ == "__main__":
	for l in open(sys.argv[1],"rb").readlines():
		wl = tokenize(l)
		print " ".join(wl)
