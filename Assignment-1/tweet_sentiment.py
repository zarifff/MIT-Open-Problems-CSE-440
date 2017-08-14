# Mohammad Zariff Ahsham Ali


# Required imports or library dependencies
import re, sys, json, math
import matplotlib.pyplot as plt

unknownTermDict = {}


# Is the tweet in English?
# Use try and except clause
# If try works for english language tweet return true, else false
# Read Twitter Developer Documentation carefully
def isLang(tweet_json, lang = 'en'):
    try: 
        return tweet_json['lang'] == lang
    
    except: return False


# Create a sentiment dictionary
def genSentDict(sent_file):
    sent_file = open(sent_file)
    scores = {}
    
    for line in sent_file:
        term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        scores[term] = int(score)        # Convert the score to an integer.        
    
    return scores


# Get a English tweet 
# Check for English Tweets 
# input: tweet as json
# output: tweet terms as list

# Make sure to use unicode encode
# Use re.findall to get the tweet terms/words as list.
# Fill the rest.
# Details explained in class.
def getENTweet(tweet_json):
    if ( isLang(tweet_json) ):
	unicode_tweet_text = tweet_json['text']
	encoded_tweet_text = unicode_tweet_text.encode('utf-8')
	tweet_terms = re.findall(r"(?i)\b[a-z']+\b", encoded_tweet_text)
        return tweet_terms
    else: return []


# Get score from the tweet
# input: tweet as json, sentiment dictionary (hashmap and/or map, python dictionary)
# output: tweet score
# Fill the rest, details explained in class.
def getSentScoreOfTweet(tweet_json, sentDict, choice):

    tweet_score = 0
    tweet_terms = getENTweet(tweet_json)

    for term in tweet_terms:

	term = term.lower()
	try:
            tweet_score += sentDict[term]
            
        except:
            if choice == 'y':
                tweet_score += unknownTermDict[term]
            else:
                tweet_score += 0
                 
    return tweet_score
                   

def genUnknownTermDict(tweet_json, sentDict):
    tweet_terms = getENTweet(tweet_json)
    tweet_score = 0
    termnum = 0

    for term in tweet_terms:
        term = term.lower()

        if sentDict.has_key(term):
            tweet_score += sentDict[term]
            termnum += 1
            continue
        else:
            if unknownTermDict.has_key(term):
                continue
            else:
                unknownTermDict[term] = list()

    try:
        tweet_score /= float(termnum)
        #tweet_score = int(round(tweet_score))
    except:
        tweet_score = 0
            
    for term in tweet_terms:
        term = term.lower()     
        try:
            unknownTermDict[term].append(tweet_score)
        except: continue
        

def genUnknownTermScore():
    for key, val in unknownTermDict.iteritems():
        totalScore = 0
        terms = len(val)

        while not len(val) == 0:
            totalScore += unknownTermDict[key].pop()
            
        finalScore = totalScore/float(terms)
        #finalScore = int(round(finalScore))

        unknownTermDict[key] = finalScore


# Score the tweets in the tweets file
# Incorporates an option to generate tweet scores from dynamically generated new term dictionary
def getTweetScores(sentDict, tweets_file1):
    tweets_file = open(tweets_file1)
    sentDict = genSentDict(sentDict)
    posScore = 0
    negScore = 0
    minScore = 0
    maxScore = 0
    mostPositiveTweet = 'Not enough data!'
    mostNegativeTweet = 'Not enough data!'
    scoresList = []

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
            score = getSentScoreOfTweet(tweet_json, sentDict, choice)
            score = int(round(score))
            scoresList.append(score)
            if score > 0:
                posScore += 1
            elif score < 0:
                negScore += 1
            if score > maxScore and not score == 0:
                try:
                    mostPositiveTweet = tweet_json['text']
                    maxScore = score
                except: continue
            if score < minScore and not score == 0:
                try:
                    mostNegativeTweet = tweet_json['text']
                    minScore = score
                except: continue
            print score

        except: pass

    scoreCount = [posScore, negScore]
    scoreLabel = ['Positive', 'Negative']

    genPosNegBar(scoreCount, scoreLabel)
    print '\nMost Positive Tweet: \'', mostPositiveTweet, '\'\nScore: ', maxScore
    print '\nMost Negative Tweet: \'', mostNegativeTweet, '\'\nScore: ', minScore

#Function to generate graph
def genPosNegBar(scoreCount, scoreLabel):
    r = range(len(scoreLabel))
    plt.xticks(r, scoreLabel)       
    plt.bar(r, scoreCount, align='center', color='aqua')
    plt.xlabel('Positive/Negative Tweet')
    plt.ylabel('Number of Tweets')
    plt.title('Number of Positive tweets and negative tweets.\n(Neutral tweets not shown)')
    plt.show()


if __name__ == '__main__':
    getTweetScores(sys.argv[1], sys.argv[2])
