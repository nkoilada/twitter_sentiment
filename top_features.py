import time
import sys
from math import log

words_cnts = { }
n_pos_tweets = 0
n_neg_tweets = 0

for l in open(sys.argv[1],"rb").readlines():
	n_pos_tweets = n_pos_tweets + 1
	wl = l.strip().split()
	for w in wl:
		if words_cnts.get(w) is None:
			words_cnts[w] = {}
			words_cnts[w]["pos"] = 1
			words_cnts[w]["neg"] = 0
		else:
			words_cnts[w]["pos"] = words_cnts[w]["pos"] + 1

for l in open(sys.argv[2],"rb").readlines():
	n_neg_tweets = n_neg_tweets + 1
	wl = l.strip().split()
	for w in wl:
		if words_cnts.get(w) is None:
			words_cnts[w] = {}
			words_cnts[w]["neg"] = 1
			words_cnts[w]["pos"] = 0
		else:
			words_cnts[w]["neg"] = words_cnts[w]["neg"] + 1

all_words = words_cnts.keys()
n_tweets = float(n_pos_tweets + n_neg_tweets)
p_pos = float(n_pos_tweets)/float(n_tweets)
p_neg = 1.0 - p_pos


# Calculate Mutual Information for each feature (word)
f = open("top_features.txt", "w")
for w in all_words:
	mi = 0.0
	n_pos_w = words_cnts[w]["pos"] if words_cnts[w]["pos"] is not 0 else 1 
	n_neg_w = words_cnts[w]["neg"] if words_cnts[w]["neg"] is not 0 else 1
	n_w = n_pos_w + n_neg_w
	mi = mi + (n_pos_w/n_tweets) * log(n_pos_w/(p_pos * n_w))
	mi = mi + (n_neg_w/n_tweets) * log(n_neg_w/(p_neg * n_w))
	mi = mi + ((n_pos_tweets - n_pos_w)/n_tweets) * log((n_pos_tweets - n_pos_w)/(p_pos * (n_tweets - n_w)))
	mi = mi + ((n_neg_tweets - n_neg_w)/n_tweets) * log((n_neg_tweets - n_neg_w)/(p_neg * (n_tweets - n_w)))
	f.write(str(mi) + "\t" + w + "\n")
f.close()	

