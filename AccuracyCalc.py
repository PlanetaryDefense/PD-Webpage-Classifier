from sklearn.externals import joblib
import csv 
import re

"""
Uses the trained classifier to predict whether or not a webpage from a full set of webcrawler results is relevant or not.  The accuracy of each round is then printed to a text document.

NOTE: User of program must edit paths accordingly 
"""

def calcRelevant(listInput, roundMark):
    """
    For each webpage in the full crawl dataset, parses the URL and title which is 
    passed to the imported classifier which predicts if the webpage is relevant 
    or not.  This result is then appended to a structure of rounds and their 
    corresponding accuracy percentages based on the classifier.
    
    Args:
        listInput: a list containing webpages sharing the same crawl round
        roundMark: the marker of the round associated with the webpage list
    """
    if roundMark > 1:
        successCount = 0
        for row in range(0, len(listInput)):
            
            # use regular expressions to get key words from URL and title
            parsedURL = re.findall(r"['\w']+", listInput[row][0])
            parsedTitle = re.findall(r"['\w']+", data[row][1])
            
            urlString = ''
            for i in range(0, len(parsedURL)):
                if parsedURL[i] != 'http' and parsedURL[i] != 'https' and parsedURL[i] != 'www':
                    urlString = urlString + ' ' + parsedURL[i]       
            titleString = ''
            for i in range(0, len(parsedTitle)):
                titleString = titleString + ' ' + parsedTitle[i]
                
            result = [urlString + titleString]
            prediction = pipeline.predict(result) # predict if page is relevant or not based on URL and title
            if(prediction[0] == 'relevant'):
                successCount+=1
                
        # append the round number along with the percentage of successful pages for that round based on the prediction model
        roundAccuracy.append([roundMark, successCount/len(listInput)])
                
def writeEvaluation(evalArr):
    """
    Writes the results of the crawler evaluation to CSV file in this order:
    (Round Number, Success Percentage)
    
    Args:
        evalArr: array containing results of crawler evaluation per round
    """
    with open(r'C:\JGSTCWork\crawleva\CSVresults\output_classification.csv', "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerows(evalArr)

# load in the trained model from file in same directory
pipeline = joblib.load('multinomial_classifier.pkl') 

# put csv file into list
with open(r'C:\JGSTCWork\crawleva\eva_0729_test_so.csv', encoding="utf8") as csv_file:
    reader = csv.reader(csv_file, delimiter = ",")
    data = list(reader)
    
# rows arranged by round of crawl from least to greatest,
# assuming the column containing the round is the 6th (key = 5)
data = sorted(data, key = lambda x: x[5])

roundAccuracy = []

rowMarker = 0
roundMarker = 1

# calculate the percentage of relevant webapages for each round of the crawl
while True:    
    roundList = []
    while (data[rowMarker][5] == data[rowMarker + 1][5]):
        roundList.append(data[rowMarker][0:1])
        rowMarker+=1
        if(rowMarker == len(data)-1):
            break
    roundList.append(data[rowMarker][:]) # takes care of appending final round value
    
    calcRelevant(roundList, roundMarker)
    
    if rowMarker == len(data) - 1:
        break
    roundMarker += 1
    rowMarker+=1
    
writeEvaluation(roundAccuracy)