import os
from pandas import DataFrame
import numpy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.cross_validation import KFold
from sklearn.metrics import confusion_matrix, f1_score

"""
Trains a classifier using features extracted from webpage URLs anmd titles 
in order to predict whether a future webpage is relevant or irrelevant.

Uses multinomial naive Bayes and produces a confusion matrix and F1 score to 
display the results of tweaking the parameters of the classifier. 

NOTE: User of program must edit paths accordingly 
"""

NEWLINE = '\n'
SKIP_FILES = {'cmds'}

"""
Takes a file path, iterates recursively through all files in path,
and yields textual content from crawler contained in the path.  Allows for moving 
of data into directories

Args:
    path: path containing parsed keywords from crawl results
"""
def read_files(path):
    for root, dir_names, file_names in os.walk(path):
        for path in dir_names:
            read_files(os.path.join(root, path))
            
        for file_name in file_names:
            if file_name not in SKIP_FILES:
                file_path = os.path.join(root, file_name)
                if os.path.isfile(file_path):
                    lines = []
                    f = open(file_path, encoding="latin-1")
                    
                    for line in f:
                        lines.append(line)
                            
                    f.close()
                    content = NEWLINE.join(lines)
                    #print(content)
                    yield file_path, content

"""
Uses Panda library to turn data into ideal array format 
for classifier

Args:
    path: path containing parsed keywords from crawl results
    classification: marker indicating relevant or not relevant
Returns: 
    data_frame: DataFrame from all files in path
"""              
def build_data_frame(path, classification):
    rows = []
    index = []
    for file_name, text in read_files(path):
        rows.append({'text': text, 'class': classification})
        index.append(file_name)

    data_frame = DataFrame(rows, index=index)
    return data_frame

# classifications of data
R = 'relevant'
NR = 'not relevant'

# training set of relevant and not relevant webpages
# arranged by (PATH, CLASSIFICATION)
SOURCES = [
    ('/Users/yjiang/Documents/nutch_data/classification/YES',       R),
    ('/Users/yjiang/Documents/nutch_data/classification/NO',      NR),
]

# add training set to data frame
data = DataFrame({'text': [], 'class': []})
for path, classification in SOURCES:
    data = data.append(build_data_frame(path, classification))

data = data.reindex(numpy.random.permutation(data.index)) # shuffle the dataset

# Pipeline consists of a count vectorizer and a classifier to
# learn vocabulary and extract word count features
pipeline = Pipeline([
    ('count_vectorizer',   CountVectorizer(ngram_range=(1,  2))), # looking for n-gram frequency
    ('classifier',         MultinomialNB())])

pipeline.fit(data['text'].values, data['class'].values)
# examples = ['neo jpl', 'venus NASA', 'black hole']
# pipeline.predict(examples)

# save the trained model to use in AccuracyCalc.py
from sklearn.externals import joblib
joblib.dump(pipeline, 'multinomial_classifier.pkl') 

k_fold = KFold(n=len(data), n_folds=6)
scores = []
confusion = numpy.array([[0, 0], [0, 0]])
for train_indices, test_indices in k_fold:
    train_text = data.iloc[train_indices]['text'].values
    train_y = data.iloc[train_indices]['class'].values

    test_text = data.iloc[test_indices]['text'].values
    test_y = data.iloc[test_indices]['class'].values

    pipeline.fit(train_text, train_y)
    predictions = pipeline.predict(test_text)

    confusion += confusion_matrix(test_y, predictions)
    score = f1_score(test_y, predictions, pos_label=R)
    scores.append(score)

print('Total pages classified:', len(data))
print('Score:', sum(scores)/len(scores))
print('Confusion matrix:')
print(confusion)