Sentiment Analysis using Twitter
================================

Overview
--------

People share their experiences with their friends on social networks. These posts often have a clear sentiment of the person. It would be useful to analyze this huge amount of data present on social networks to derive some useful sentiment statistics about consumer products, movies, celebrities etc. This project uses machine learning techniques to analyzes the data from Twitter social network and derive the sentiment statictics.

Training Data
-------------
A labelled dataset for training the machine learning model is created by using Twitter Search API. The tweets from Twitter search results for the query ":)" are marked as positive and for the search query ":(" are marked negative. This approach of creating the training dataset might result in lot of noisy data. To counter that we can have really large dataset and a choose a good machine learning algorithm which is robust against noisy features.


Cleaning The Data
-----------------
Twitter has special markup like usernames (start with @), topics (start with #), retweet (indicated by RT) etc.
These special markup tokens are identified and removed. Only words made up of alphabets, "-" and "_" are included.

		python tokens.py raw_tweets.txt

Language Detection
------------------
The tweets returned by Twitter Search API could also contains tweets in some other languages like Spanish, Portuguese, Dutch etc. This can happen even when lang = en filter is used. There are two different methods implemented in this project to separate the non-english tweets from english tweets:

1. Clustering Based Language Detection
In this method we assume Mixture of Gaussians model for the tweets and use the Expection-Maximization algorithm to estimate the parameters of the model. We hope that the two groups formed will be of english and non-english tweets. Once the model parameters are estimated, we can use them to classify new tweets.

		python lang_detection_em.py --build clean_tweets.txt
		python lang_detection_em.py clean_tweets.txt #creates a new file clean_tweets.filtered.txt

2. Dictionary Based Language Detection
This is a simple model which uses a dictionary of english words for reference. A tweet is classified as english or not, based on the number of tokens of the tweets present in the dictionary. This approach can also result in false negatives as Twitter language is often not perfect english.

For this method the performance of the model mainly depends on the size of dictionary. We can have a very large dictionary with small memory footprint using BloomFilter.

		python lang_detection.py clean_tweets.txt #creates a new file clean_tweets.filtered.txt


Sentiment Detection
-------------------
A Logistic Regression (lr) model is used to classify a tweet's sentiment as positive or negative. The script sentiment.py gets the last 100 tweets for the search query and uses the lr model to produce sentiment statistics.

		$python sentiment.py <search query> <path to model file>
				
		nkoilada@nkoilada-lap:~/Projects/twitter_sentiment$ python sentiment.py facebook models/model_lr_1349310935.pkl 
		Positive, Negative : [ 59.57148106  40.42851894]
		nkoilada@nkoilada-lap:~/Projects/twitter_sentiment$ python sentiment.py google models/model_lr_1349310935.pkl 
		Positive, Negative : [ 55.73795085  44.26204915]
		nkoilada@nkoilada-lap:~/Projects/twitter_sentiment$ python sentiment.py microsoft models/model_lr_1349310935.pkl 
		Positive, Negative : [ 58.35616305  41.64383695]
		nkoilada@nkoilada-lap:~/Projects/twitter_sentiment$ python sentiment.py twitter models/model_lr_1349310935.pkl 
		Positive, Negative : [ 61.25092372  38.74907628]

License
-------
This software comes with GNU LGPL v2.1. For complete terms see "LICENSE.txt"

Author
------
Name: Nagendra Koilada

Email: nkoilada@uci.edu


 
