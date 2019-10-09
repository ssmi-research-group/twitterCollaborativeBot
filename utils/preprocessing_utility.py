import re
import string

def tweet_treatment (tweet_text):

    VALID_OPERATIONS = ['QUEMSABE', 'QUANTOSSABEM', 'SOBREOQUESABEM']
    treated_tweet_text = ''
    operation = None
    term = '#twitter'

    # recupera e remove do tweet original a conta do robô
    bot_account =  re.findall(r'@\w+', tweet_text)[0]
    tweet_text_bot_acc_removed = tweet_text.replace(bot_account, '')

    # adiciona ao tweet tratado a conta do robô
    treated_tweet_text += bot_account + ' '

    # remove os espaços do tweet original
    tweet_text_spaces_removed = tweet_text_bot_acc_removed.replace(' ', '')

    # remove a pontuação do tweet original e converte os caracteres para maiúsculos
    tweet_text_punctuation_removed = tweet_text_spaces_removed.translate(str.maketrans('', '', string.punctuation)).upper()

    # verifica, para cada operação permitida, se esta está contida no tweet
    for opr in VALID_OPERATIONS:
        if opr in tweet_text_punctuation_removed:
            operation = opr
            tweet_term = tweet_text_punctuation_removed.replace(opr, '')
            term = '#' + tweet_term.lower() if len(tweet_term) > 0 else '#twitter'

            # adiciona ao tweet tratado a operação e o termo extraídos
            treated_tweet_text += operation + ' ' + term

    return treated_tweet_text