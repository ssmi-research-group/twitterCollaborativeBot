import re
import string

"""
1 - @WhoKnowsBot QuEm SaBE,             banana?
2 - @WhoKnowsBot QuEm SaBE             banana
3 - @WhoKnowsBot QuEm SaBE banana
4 - ['@WhoKnowsBot', QuEm, SaBE, banana] <- ERRADO
5 - ['@WhoKnowsBot', QuEmSaBE, banana]

1 - @WhoKnowsBot QuEm SaBE,             banana? macaco tesouro beliche
2 - QuEm SaBE,             banana? macaco tesouro beliche
3 - QuEm SaBE             banana macaco tesouro beliche
4 - QuEm SaBE banana macaco tesouro beliche
    sobre o que sabem banana macaco tesouro beliche
    quantos sabem banana macaco tesouro beliche

    quemsabe banana macaco tesouro beliche
    sobreoquesabem banana macaco tesouro beliche
    quantossabem banana macaco tesouro beliche

5 - banana macaco tesouro beliche
6 - ['banana', 'macaco', 'tesouro', 'beliche']

1 - @WhoKnowsBot
2 - ''
3 - ''
4 - ''
5 - (None, None)

1 - @WhoKnowsBot banana
2 - banana
3 - banana
4 - banana
5 - (None, None)

1 - @WhoKnowsBot QUEMSABE
2 - QUEMSABE
3 - QUEMSABE
4 - QUEMSABE
5 - 

1 - @WhoKnowsBot QUEM SABEcorrida de                 carros
2 - QUEM SABEcorrida de                 carros
3 - QUEM SABEcorrida de carros
4 - (QUEM SABE, corrida)
5 -

"""

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
