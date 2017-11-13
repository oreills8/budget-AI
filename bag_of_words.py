
import pandas as pd
import re
from sklearn.feature_extraction.text import CountVectorizer

class Bag_of_words:

    def __init__(self, string_series):
        self.string_series = string_series
        self.x = self.tokenize()

    def tokenize(self):
        DF = pd.DataFrame()
        count = 0
        for index,sentence in self.string_series.iteritems():
            description = sentence.split(' ')
            for word in description:
                if (word.isalnum()) and not (self.hasNumbers(word)) : #if word doesnt contain special characters or numbers
                    per_use = (float(description.count(word))/len(description))
                    DF.set_value(count, word, per_use)
            count = count + 1
        DF = DF.fillna(0.0)
        return DF

    def hasNumbers(self,inputString):
        return any(char.isdigit() for char in inputString)