import sys

# Build dictionary
words = dict()
for i in open('data/words.txt', 'rb').readlines():
	w = i.strip().lower()
	if not words.has_key(w):
		words[w] = True

def filter_tweets(tweets):
	# Filter out non-english tweets
	en_tweets = []
	for tweet in tweets:
		n = 1.0
		p = 1.0
		for t in tweet:
			if words.has_key(t):
				p = p + 1.0
			else:
				n = n + 1.0
			p_en = 	p / (n + p)
		if p_en > 0.5:
			en_tweets.append(tweet)
	return en_tweets

if __name__ == "__main__":

	tweets = []
	# Read Tweets
	for l in open(sys.argv[1],"rb"):
		tweets.append(l.strip().split())

	filtered_tweets = filter_tweets(tweets)
	# Write Filtered tweets to file
	f = open(sys.argv[1][0:-4] + ".filtered.txt", "w")
	for l in filtered_tweets:
		f.write(" ".join(l) + "\n")
	f.close() 
	

