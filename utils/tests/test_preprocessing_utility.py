import unittest
from utils.preprocessing_utility import tweet_treatment

class test_preprocessing_utility(unittest.TestCase):
    
    def test_tweet_treatment_without_operation_and_term(self):
        self.assertEqual(tweet_treatment('@WhoKnowsBot '), '@WhoKnowsBot ')

    def test_tweet_treatment_without_operation_with_term(self):
        self.assertEqual(tweet_treatment('@WhoKnowsBot banana abaxi limao'), '@WhoKnowsBot ')

    def test_tweet_treatment_with_operation_without_term(self):
        self.assertEqual(tweet_treatment('@WhoKnowsBot QuAntOsSaBEM'), '@WhoKnowsBot QUANTOSSABEM #twitter')

    def test_tweet_treatment_with_spaced_operation(self):
        self.assertEqual(tweet_treatment('@WhoKnowsBot              Quem                Sabe   #python'), '@WhoKnowsBot QUEMSABE #python')
        self.assertEqual(tweet_treatment('@WhoKnowsBot           QuAntOs    SaBE M    #python'), '@WhoKnowsBot QUANTOSSABEM #python')
        self.assertEqual(tweet_treatment('@WhoKnowsBot   sobre O que            sabem   #python'), '@WhoKnowsBot SOBREOQUESABEM #python')

    def test_tweet_treatment_with_spaced_term(self):
        self.assertEqual(tweet_treatment('@WhoKnowsBot QuAntOsSaBEM lucas rotsen pereira'), '@WhoKnowsBot QUANTOSSABEM #lucasrotsenpereira')

    def test_tweet_treatment_without_space_between_operation_and_term(self):
        self.assertEqual(tweet_treatment('@WhoKnowsBot QuAntOsSaBEMlucasrotsenpereira'), '@WhoKnowsBot QUANTOSSABEM #lucasrotsenpereira')