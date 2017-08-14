# Mohammad Zariff Ahsham Ali

import re, sys, json
from tweet_sentiment import *
import matplotlib.pyplot as plt
import operator
import numpy as np

# Fill the rest
# Details explained in class.
# Input: The downloaded tweets file
# Output: The freq dictionary {key: tweet terms, value: frequency as probability}
def frequency(tweets_file):
    freq = {}
    tweets_file = open(tweets_file)
    n = 1 #set to 1 to avoid divide by zero error.

    for tweet in tweets_file:
        try:
            tweet_json = json.loads(tweet, strict=False)
        except: continue
        tweet_terms = getENTweet(tweet_json)
        n += len(tweet_terms)

        for term in tweet_terms:
            term = term.lower()

            if freq.has_key(term):
                freq[term] += 1
            else:
                freq[term] = 1

    for key in freq:
        freq[key] /= float(n)

    return freq

def printFrequency(freqDict):
    for key in freqDict.keys():
        print("%s %.6f" % ( key, freqDict[key] ) )

def topTenFrequency(freqDict):
    freqList = sorted(freqDict, key=freqDict.get, reverse=True)
    print '\nTop Ten:\nTerm\tFrequency\n'
    for i in range(10):
        print freqList[i], '\t', freqDict[freqList[i]]

def plotFrequencyBar(freqDict):
    #Turns the dictionary into a list of tuples.
    # The [0:10] makes the list return its first 10 key-value pairs, and the reverse=True sorts the list from highest to lowest.
    lists = sorted(freqDict.items(), key=operator.itemgetter(1), reverse=True)[0:10]
    # Divides the tuples in the list into separate lists of keys (terms) and values (counts)
    terms, counts = zip(*lists)
    # This is the range of the plotting of the graph.
    r = range(len(terms))
    # This is necessary to print strings on the x axis.
    plt.xticks(r, terms)
    # This shows bars for the Y value instead of points, and aligns each bar to the center of each X value.
    plt.bar(r, counts, align='center', color='crimson')
    plt.xlabel('Terms')
    plt.ylabel('Frequency (Probability)')
    plt.title('Frequency/Probability Distribution of top ten terms')
    # Shows the bar chart.
    plt.show()


if __name__ == '__main__':
    printFrequency(frequency(sys.argv[1]))
    topTenFrequency(frequency(sys.argv[1]))
    plotFrequencyBar(frequency(sys.argv[1]))

