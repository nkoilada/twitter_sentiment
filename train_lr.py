import pickle
import time
import sys
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

def train():
	tweets = []
	labels = []

	# load training data
	print "Loading Training Data..."
	for tweet in open(sys.argv[1], 'rb').readlines():
		tweets.append(tweet)
		labels.append(1.0)

	for tweet in open(sys.argv[2], 'rb').readlines():
		tweets.append(tweet)
		labels.append(0.0)
	vectorizer = CountVectorizer()
	X = vectorizer.fit_transform(tweets)
	
	print "Started Training Logistic Regression Classifier"
	classifier = LogisticRegression(tol=0.01)
	classifier.fit(X, labels)
	print "Score: ", classifier.score(X, labels)

	print "Saving Model to File"
	f = open("models/model_lr_" + str(int(time.time())) + ".pkl",'wb')
	pickle.dump(classifier, f, -1)
	f.close()

if __name__ == '__main__':
	train()
