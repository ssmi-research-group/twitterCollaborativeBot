import re
import string

def tweetPreprocessing (tweet_text):

    prepTweet = removeRedundantSpaces(removePunctuation(removeBotAccount(tweet_text)))
    return extractOperationAndTerm(prepTweet)


def removeBotAccount (tweet_text):
    return re.sub(r'@\w+', '', tweet_text).strip()

def removePunctuation (tweet_text):
    if tweet_text != '':
        return tweet_text.translate(str.maketrans('', '', string.punctuation))

    return tweet_text

def removeRedundantSpaces (tweet_text):
    if tweet_text != '':
        return re.sub(' +', ' ', tweet_text)

    return tweet_text

def extractOperationAndTerm (tweet_text):

    operation = None
    term = '#twitter'

    if tweet_text != '':

        VALID_OPERATIONS = ['QUEMSABE', 'QUANTOSSABEM', 'SOBREOQUESABEM', 'QUEM SABE', 'QUANTOS SABEM', 'SOBRE O QUE SABEM']
        tweetText = tweet_text.upper()

        for opr in VALID_OPERATIONS:
            if opr in tweetText:
                operation = opr.replace(' ', '')
                tweet_terms = tweetText.replace(opr, '').split()
                term = '#' + tweet_terms[0].lower() if len(tweet_terms) > 0 else '#twitter'
                break
    
    return (operation, term)
