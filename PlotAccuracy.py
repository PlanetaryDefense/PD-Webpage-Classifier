import matplotlib.pyplot as plt
import csv

# put csv file into list
with open(r'C:\JG_STC_Work\crawleva\CSVresults\output_classification.csv', encoding="utf8") as csv_file:
    reader = csv.reader(csv_file, delimiter = ",")
    data = list(reader)

rounds = []
percentage = []
for round in range(0, len(data)):
    rounds.append(data[round][:][0])
    percentage.append(data[round][1][:])

plt.plot(rounds, percentage)
plt.ylabel('Accuracy Percentage')
plt.xlabel('Round Number')
plt.show()