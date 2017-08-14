# Mohammad Zariff Ahsham Ali

# Required imports or library dependencies
import re, sys, json
from tweet_sentiment import *

# Fill me.
# Details explained in class.
# Added another list variable. This list holds the top-10
# hashtag frequency. A tuple containing both the sorted keys along with
# their values is returned. The algorithm is simple. Everything is provided
# in the Twitter API. isLang() from tweet_sentiment.py is used to check for English
# A simple check is done to see if key exists; if it does, add 1 to its value
# else make a new key in dictionary with value of 1.

def gettopTenHashTags(tweets_file, n = 10):
    hashTagFreq = {}
    hashTagFreqVal = []
    tweets_file = open(tweets_file)
        
    for tweet in tweets_file:
        try:
            tweet_json = json.loads(tweet, strict=False)
        except: continue
        if ( isLang(tweet_json) ):
            try:
                key = tweet_json['entities']['hashtags']
                for hashTagsDict in key:
                    if hashTagFreq.has_key(hashTagsDict['text']):
                        hashTagFreq[hashTagsDict['text']] += 1

                    else:
                        hashTagFreq[hashTagsDict['text']] = 1

            except: continue       

    sortedTags = sorted(hashTagFreq,
                        key=hashTagFreq.get,
                        reverse=True)
    
    for i in range(len(hashTagFreq)):
        hashTagFreqVal.append(hashTagFreq[sortedTags[i]])

    genGraph(sortedTags, hashTagFreqVal)
    
    return (sortedTags[:n], hashTagFreqVal[:n])

def genGraph(sortedTags, hashTagFreqVal, n=10):
    slices = hashTagFreqVal[:n]
    hashtags = sortedTags[:n]
    colorsList = ['r','aqua','lightgreen','lightgoldenrodyellow','m','lightcyan','darkred','aquamarine','darkgray','honeydew']
    '''otherScore = 0
    if len(sortedTags) > n:
        for i in range(n, len(sortedTags)):
            otherScore += hashTagFreqVal[i] #Other hashtags forms a very large percent
    slices.append(otherScore)
    hashtags.append('Others')'''
    plt.pie(slices, labels=hashtags, startangle=90, colors=colorsList, shadow=True, autopct='%1.1f%%')
    plt.title('Top 10 Hashtags')
    
    plt.show()

#Iterate through tuple printing key + value pairs, with formatting
if __name__ == '__main__':    
    toptenTags = gettopTenHashTags(sys.argv[1])
    print '\nHashtag'.ljust(21), 'Frequency\n'
    for i in range(10):
	try:
            print toptenTags[0][i].encode('utf-8').ljust(23), toptenTags[1][i]
	except:
	    pass  
    
    
    
