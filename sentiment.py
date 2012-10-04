import sys
import urllib
import urllib2
import json
import tokens
#import lang_detector_em as lang_detector
import lang_detector
import pickle
from sklearn.feature_extraction.text import CountVectorizer

params = {"q": sys.argv[1],
		  "lang": "en",
		  "rpp": 100,
		  "result_type": "recent"}

api_base_url = "http://search.twitter.com/search.json"

raw_data = json.load(urllib2.urlopen(api_base_url + "?" + urllib.urlencode(params)))

# Load Tweets
tweets = []
for i in raw_data["results"]:
	tweets.append(tokens.tokenize(i["text"]))

# Filter out Non-English Tweets
tweets = lang_detector.filter_tweets(tweets)

# Load Classifier
f = open(sys.argv[2], 'rb')
classifier = pickle.load(f)
f.close()

vectorizer = CountVectorizer()
X = vectorizer.fit_transform([" ".join(t) for t in tweets])
y = classifier.predict_proba(X)

print "Positive, Negative :", 100 * sum(y) / sum(sum(y))

