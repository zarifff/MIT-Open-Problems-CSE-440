# Mohammad Zariff Ahsham Ali

# Required imports or library dependencies
import re, sys, json
import matplotlib.pyplot as plt
import operator
from tweet_sentiment import *
from stateDict import getStatesDict
from statesDictFull import getStatesDictFullKey


# Is the tweet from a certain country?
def isCountry(tweet_json, country = 'United States'):
    try: return tweet_json['place']['country'] == country
    except: return False


# Get abbreviated state's form from encrypted place info
# Fill me.
def getStateFromPlace(placeinfo, statesListFullKey):
    splittext = placeinfo.split(',')
    splittext[-1] = re.findall(r"\w+", splittext[-1])
    if splittext[-1][0] == 'USA':
        try:
            stateABV = statesListFullKey[splittext[0]]
        except:
            if splittext[0] == 'Washington, DC':
                stateABV = 'WA'
            else:
                stateABV = 'undef'
    else:
        stateABV = splittext[-1][0]
    return stateABV

#Did not need to use these functions
'''
# Gets the state (cond. USA) info of the tweet.
def getUSAStateABV(tweet_json):
    try:
        placeInfo = tweet_json['place']['full_name']        
        stateABV = getStateFromPlace(placeInfo)
        return stateABV
    except: ''


# Is the state in the United States?
# Returns true flase.
# Fill me
def isStateInUSA(tweet_json, stateList):
    try: 
        
    except: return False

'''
# Is the tweet geo coded?
def isGeoEnabled(tweet_json):
    return tweet_json['user']['geo_enabled']
    

# Fill the rest.
# Details explained in class
def mostHappyUSState(sentDict, tweets_file1):
    stateSenti = {}
    totalStateTweetCount = {}
    unknownTermDict = {}
    statesListABVKey = getStatesDict()
    statesListFullKey = getStatesDictFullKey()
    tweets_file = open(tweets_file1)
    sentDict = genSentDict(sentDict)

    choice = raw_input("Would you like to generate scores for unknown terms and incorporate them? Will take much longer. (Y/N): ")
    choice = choice.lower()

    if choice == 'y':
        for tweet in tweets_file:
            try:
                tweet_json = json.loads(tweet, strict=False)
            except:
                continue
            try:
                genUnknownTermDict(tweet_json, sentDict)
            except: continue
        
        genUnknownTermScore()
        
        tweets_file.close()
        tweets_file = open(tweets_file1)
       
    for tweet in tweets_file:
        try:
            tweet_json = json.loads(tweet, strict=False)
        except:
            continue
        try: 
            if(isGeoEnabled(tweet_json) and isCountry(tweet_json)):
                placeinfo = tweet_json['place']['full_name']
                placeinfo = placeinfo.encode('utf-8')
                stateABV = getStateFromPlace(placeinfo, statesListFullKey)
                if (len(stateABV) == 2) and (stateABV.isupper()):
                    score = getSentScoreOfTweet(tweet_json, sentDict, choice)
                    score = int(round(score))
                    if stateSenti.has_key(stateABV):
                        stateSenti[stateABV] += score
                        totalStateTweetCount[stateABV] += 1.0
                    else:
                        stateSenti[stateABV] = score
                        totalStateTweetCount[stateABV] = 1.0
        except:
            continue
	    
    sortDict = sorted(stateSenti, key=stateSenti.get, reverse = True)

    mostHappyAvg  = 0.0
    state = 'undef'
    print '\tStates'.ljust(18), 'Aggregate Score'.ljust(21), 'Total Tweets'.ljust(17), 'Average Score\n' 

    for i in range(len(sortDict)):
        try:
            avgScore = stateSenti[sortDict[i]]/totalStateTweetCount[sortDict[i]]
            if avgScore > mostHappyAvg:
                mostHappyAvg = avgScore
                state = statesListABVKey[sortDict[i]]
        except:
            continue
        print '\t', statesListABVKey[sortDict[i]].ljust(24), str(stateSenti[sortDict[i]]).ljust(20), str(int(totalStateTweetCount[sortDict[i]])).ljust(15), ('%.4f')%avgScore
    try:
        print '\n\tHappiest State:'.ljust(47), statesListABVKey[sortDict[0]]
        print '\tHappiest State by Average score of tweet: '.ljust(46), state
    except:
        print 'Error! No items in list.'

    plotTopTenHappyStates(sortDict, statesListABVKey, stateSenti)

#function for graph    
def plotTopTenHappyStates(sortDict, statesListABVKey, stateSenti):
    terms = []
    scores = []
    try:
        for i in range(10):
            scores.append(stateSenti[sortDict[i]])
            terms.append(sortDict[i])


        r = range(10)
        plt.xticks(r, terms)
        plt.bar(r, scores, align='center', color='darkgreen')
        plt.xlabel('States')
        plt.ylabel('Aggregate Tweet Score ')
        plt.title('Top 10 Happiest States')
        plt.show()
    except: pass            
        
if __name__ == '__main__':
    mostHappyUSState(sys.argv[1], sys.argv[2])
