# , parallel_backend, register_parallel_backend
from joblib import Parallel, delayed
import numpy as np
import pandas as pd

import contractions
import textstat
import emoji as Emoji
import nltk
nltk.download('stopwords')
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
from textblob import TextBlob
# nltk.download('wordnet')
# nltk.download('omw-1.4')
# nltk.download('stopwords')
# nltk.download('vader_lexicon')
stop = stopwords.words('english')
# Parallel processing


class SubPreprocessor:
    def __init__(self, stemmer=PorterStemmer()):
        self.stemmer = stemmer
        #self.tokenize = tokenize
        self.stop_words = stop

    def fit(self, X, y=None, **fit_params):
        return self

    def transform(self, X, **transform_params):
        res = Parallel(n_jobs=-1)(
            delayed(self.processRow)(row[0]) for row in X.loc[:, 'raw_text']
        )
        res = pd.DataFrame(res, index=X.index)
        res = pd.concat([X, res], axis=1)
        return res

    def fit_transform(self, X, y=None, **fit_params):
        return self.fit(X, y).transform(X)

    def processRow(self, text):
        text, urls = self.extractLink(text, '')
        text, emojis = self.extractEmoji(text, '')
        text, emoticons = self.extractEmoticons(text, '')
        text = self.removePunctuation(text)
        text = self.removeRtLink(text)
        text = self.removeStopWords(text)

        return {
            #             'url_cnt': len(urls),
            #             'emoticons': emoticons,
            #             'emojis': emojis ,
            #             'emo_cnt': len(emoticons) + sum(emojis.values()),
            'clean_text': text,
        }

    def removePunctuation(self, text, replace='', remove_num=False, remove_emoji=False):
        r_emoji = '\u00a9|\u00ae|[\u2000-\u3300]|\ud83c[\ud000-\udfff]|\ud83d[\ud000-\udfff]|\ud83e[\ud000-\udfff]'
        r = f'[!#"$%&\'()*+,-./:;<=>?@[\]^_`{{|}}~—]'
        if remove_emoji:
            r += f'|[{r_emoji}]'
        if remove_num:
            r += f'|[0-9]'
        text = re.sub(r, replace, text)
        return text

    def extractLink(self, text, replace_text=''):
        #r = '(http\S+?|www.\S+?)(?=\'|\")'
        #r = '(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b'
        #r = '''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))'''
        #r ='^https?:\/\/.*[\r\n]*'
        r = 'http://\S+|https://\S+'
        # .apply(lambda url: url[1:-1]) # trim quotes
        urls = re.findall(r, text)
        text = re.sub(r, replace_text, text)
        return text, urls

    def extractEmoticons(self, text, replace_text=''):
        r = '(?::|;|=|X)(?:-)?(?:\)|\(|D|P)'
        emoticons = re.findall(r, text)
        text = re.sub(r, replace_text, text)
        # replace('-','') removes nose of emoticons
        emoticons = [emoticon.replace('-', '') for emoticon in emoticons]
        return text, emoticons

    def extractEmoji(self, text, replace_text=''):
        distinct_ls = Emoji.distinct_emoji_list(text)
        emoji_cnt = dict(zip(distinct_ls, [0 for i in distinct_ls]))
        for emoji in emoji_cnt.keys():
            emoji_cnt[emoji] = text.count(emoji)
            text = text.replace(emoji, replace_text)

        return text, emoji_cnt

    def wordCount(self, text):
        return textstat.lexicon_count(text, removepunct=True)

    def splitWords(self, text):
        w_list = re.split('\s+', text.strip())
        return w_list

    def removeRtLink(self, text):
        # Removes RT
        #text = re.sub('RT @\w+: ','', text)
        #text = text.lower()

        # Removes @username from the tweet
        #text = re.sub(r'(@[A-Za-z0-9_]+)', '', text)

        # Removes link
        text = re.sub('http://\S+|https://\S+', '', text)

        # Only considers string or digits or whitespace
        text = re.sub(r'[^\w\s]', '', text)

        # Removes digits
        text = re.sub(r'\d+', '', text)
        return text

    def removeStopWords(self, text):
        #text_tokens = self.tokenize(text)
        text_tokens = word_tokenize(text)
        text = [word for word in text_tokens if not word in self.stop_words]
        return ' '.join(text)

    def __call__(self, text):
        return self.processRow(text)
