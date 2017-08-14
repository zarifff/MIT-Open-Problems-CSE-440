# Mohammad Zariff Ahsham Ali

# Required imports or library dependencies
import re, sys, json
from tweet_sentiment import *
import matplotlib.pyplot as plt


MAX_VALUE = 5

'''# Generate predicted Sentiment Dictionary from tweet score and unknown tweet terms.
# May want to use try except block
# The predSentDict updates automatically that is why we do not return anything.
# Fill the rest, details explained in class.
def genPredSentDict(score, numTerms, uTerms, predSentDict):    
    for uTerm in uTerms:
        try:
            # Fill me.
        except: predSentDict[uTerm] = [score, numTerms]
        

# Analyse The tweet
# Input: Tweet terms as list, and the sentiment dictionary - hashmap/map
# Output: tweet score, unknown terms as a set data structure.
# Fill the rest. 
# Details explained in class.
def tweetAnalysis(tweet_terms, sentDict):    
    tweet_score = 0
    unknown_terms = set()    
    for term in tweet_terms:
	# Fill me.
    
    return tweet_score, unknown_terms


# Refine the new sentiment dicionary!
# Details explained in class.
# Update the new sentiment dictionary, therefore no explicit return
# Fill the rest.
def refinePredSentDict(newSentDict):
    for key in newSentDict.keys():
	# fill me.

'''
def printSentDict(sentDict):
    for key in sentDict.keys():
        value = sentDict[key]
        print("%s %.4f" % (key, value))

'''
def initPredSentDict(sentDict, tweets_file):
    newSentDict = {}    
    tweets_file = open(tweets_file)
    sentDict = genSentDict(sentDict)
    
    for tweet in tweets_file:
        tweet_json = json.loads(tweet)
        tweet_terms = getENTweet(tweet_json)

        nTerms = len(tweet_terms)
        score, uTerms = tweetAnalysis(tweet_terms, sentDict)
        genPredSentDict(score, nTerms, uTerms, newSentDict)        
        
    return newSentDict


def getPredSentDict(sentDict, tweets_file):
    predDict = initPredSentDict(sentDict, tweets_file)
    refinePredSentDict(predDict)
    return predDict'''

def genGraph(unknownTermDict):
    bins = [-5,-4,-3,-2,-1,0,1,2,3,4,5]
    scoresList = unknownTermDict.values()
    plt.hist(scoresList, bins, histtype='bar', rwidth=1.5)
    plt.xlabel('Term Score')
    plt.ylabel('Number of Terms')
    plt.title('Scores of Unknown Terms')
    plt.show()
    

def getPredSentDict(sentDict, tweets_file):
    tweets_file = open(tweets_file)
    sentDict = genSentDict(sentDict)

    for tweet in tweets_file:
        try:
            tweet_json = json.loads(tweet, strict=False)
        except: continue

        try:
            genUnknownTermDict(tweet_json, sentDict)
        except: continue
    
    genUnknownTermScore()

    return unknownTermDict

if __name__ == '__main__':
    predDict = getPredSentDict(sys.argv[1], sys.argv[2])
    printSentDict(predDict)
    genGraph(unknownTermDict)
