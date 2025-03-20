import sys
import time
import re
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import pandas as pd

df = pd.read_csv("./raw/cancer_doc_classification.csv",sep=',',skiprows=1,usecols=[1,2],names=['label','text'], encoding='ISO-8859-1')

abstract = df['text']


#run if the dataset is modified
def lemmetize_raw_data():
    lemm = WordNetLemmatizer()

    corpus = []

    for i in range(0, len(abstract)):
        sys.stdout.write('Lemmetized Sentence[' + str(i) + ']')
        time.sleep(0.0005)
        if(i < len(abstract)-1):
            sys.stdout.write('\r')
        extract = re.sub('[^a-zA-Z0-9]',' ', abstract[i])
        extract = extract.lower()
        extract = extract.split()

        extract = [lemm.lemmatize(word) for word in extract if not word in stopwords.words('english')]
        extract = ' '.join(extract)
        corpus.append(extract)

    corpus_df = pd.DataFrame(corpus,columns=['text'])
    sys.stdout.write('Successfully Lemmetized Corpus.')
    corpus_df.to_csv('./processed/corpus.csv',index=False)  # save lemmetized dataset