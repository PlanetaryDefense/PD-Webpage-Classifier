import csv 
import re

"""
Creates dataset of text documents containing only words inside of pasred URL and title for each
crawl result.

"MAYBE" no longer needed and can be deleted.

"YES" AND "NO" folders need to be created manually

NOTE: User of program must edit paths accordingly 
"""

# put csv file into list
with open(r'/Users/yjiang/Documents/pythonWorkspace/PD-Webpage-Classifier/balancedTrainingSet.csv', encoding="utf8") as csv_file:
    reader = csv.reader(csv_file, delimiter = ",")
    data = list(reader)
    
for row in range(0, len(data)):
    
    parsedURL = re.findall(r"['\w']+", data[row][0])
    parsedTitle = re.findall(r"['\w']+", data[row][1])
    
    if data[row][6] == 'Yes':
        with open('/Users/yjiang/Documents/nutch_data/classification/YES/' + 'YES' + str(row) + '.txt', 'w', encoding="utf8") as title:
            urlString = ''
            for i in range(0, len(parsedURL)):
                if parsedURL[i] != 'http' and parsedURL[i] != 'https' and parsedURL[i] != 'www':
                    urlString = urlString + ' ' + parsedURL[i]
            title.write(urlString)
          
            titleString = ''
            for i in range(0, len(parsedTitle)):
                titleString = titleString + ' ' + parsedTitle[i]
            title.write(titleString)
    if data[row][6] == 'No':
        with open('/Users/yjiang/Documents/nutch_data/classification/NO/' + 'NO' + str(row) + '.txt', 'w', encoding="utf8") as title:
            urlString = ''
            for i in range(0, len(parsedURL)):
                if parsedURL[i] != 'http' and parsedURL[i] != 'https' and parsedURL[i] != 'www':
                    urlString = urlString + ' ' + parsedURL[i]
            title.write(urlString)
          
            titleString = ''
            for i in range(0, len(parsedTitle)):
                titleString = titleString + ' ' + parsedTitle[i]
            title.write(titleString)