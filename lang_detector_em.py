import sys
import random
import re
import pickle
from  math import log
	
def build_model(train):
	n_tweets = len(train)
	params = [{},{}]
	cnt = [0.0, 0.0]
	labels = [] 
	
	# Initialization
	for i in range(n_tweets):
		l = random.uniform(0,1)
		labels.append(l)
		cnt[0] = cnt[0] + l
		cnt[1] = cnt[1] + 1.0 - l
		for f in train[i]:
			params[0][f] = params[0].get(f,0.0) + l
			params[1][f] = params[1].get(f,0.0) + 1.0 - l
	
	# EM Algorithm
	for j in range(50):
		# E - Step 
		for i in range(n_tweets):
			p_0 = 1.0
			p_1 = 1.0
			for f in train[i]:
				p_0 = p_0 * params[0].get(f) 	
				p_1 = p_1 * params[1].get(f)
			p_0 = p_0 * (cnt[0]/(cnt[0] + cnt[1])) 	
			p_1 = p_1 * (cnt[1]/(cnt[0] + cnt[1]))
			labels[i] = p_0/(p_0 + p_1)
		# M - Step
		params = [{},{}]
		for i in range(n_tweets):
			l = labels[i]	
			cnt[0] = cnt[0] + l
			cnt[1] = cnt[1] + 1.0 - l
			for f in train[i]:
				params[0][f] = params[0].get(f,0.0) + l
				params[1][f] = params[1].get(f,0.0) + 1.0 - l
		# Compute Log-Likelihood
		ll = 0.0
		for i in range(n_tweets):
			l = labels[i]
			p_0 = 1.0
			p_1 = 1.0
			for f in train[i]:
				p_0 = p_0 * params[0].get(f) 	
				p_1 = p_1 * params[1].get(f)
			p_0 = p_0 * (cnt[0]/(cnt[0] + cnt[1])) 	
			p_1 = p_1 * (cnt[1]/(cnt[0] + cnt[1]))
			ll = ll + log(p_0 + p_1)
		print "Log-Likelihood", ll
			
	params.append(cnt[0])
	params.append(cnt[1])
	f = open("models/lang_detection_model.pkl","wb")
	pickle.dump(params, f, 1)
	f.close()

def filter_tweets(tweets):
	f = open("models/lang_detection_model.pkl","rb")
	params = pickle.load(f)
	f.close()
	cnt = params[2:4]

	en_label = 0.0 
	if cnt[0] < cnt[1]:
		en_label = 1.0
	en_tweets = []
	for tweet in tweets:
		p_0 = 1.0
		p_1 = 1.0
		for f in tweet:
			p_0 = p_0 * max(params[0].get(f,0.0),0.1)
			p_1 = p_1 * max(params[1].get(f,0.0),0.1)
			p_0 = p_0 * (1.0/(1.0 + (cnt[1]/cnt[0])))
			p_1 = p_1 * (1.0/((cnt[0]/cnt[1]) + 1.0))
			p_0 = p_0/(p_0 + p_1)
	if (en_label == 0.0 and p_0 > 0.5) or (en_label == 1.0 and p_0 < 0.5):
		en_tweets.append(tweet)
	return en_tweets

if __name__ == "__main__":
	if sys.argv[1] == "--build":
		train = [l.strip().split() for l in open(sys.argv[2],"rb").readlines()]
		build_model(train)
	else:
		tweets = [l.strip().split() for l in open(sys.argv[1],"rb").readlines()]
		filtered_tweets = filter_tweets(tweets)
		# Write Filtered tweets to file
		f = open(sys.argv[1][0:-4] + ".filtered.txt", "w")
		for l in filtered_tweets:
			f.write(" ".join(l) + "\n")
		f.close()	
