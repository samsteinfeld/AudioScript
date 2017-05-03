from PyDictionary import PyDictionary 
import string
import re
import glob
from textblob.classifiers import NaiveBayesClassifier
from textblob import TextBlob
import sys

#training set for finding sentiment
training_set = [
    ("I would not", "neg"),
    ("I wouldn't", "neg"),
    ("no", "neg"),
    ("not okay", "neg"),
    ("not alright", "neg"),
    ("not all right", "neg"),
    ("do not", "neg"),
    ("don't", "neg"),
    ("wrong", "neg"),


    ("I would", "pos"),
    ("okay", "pos"),
    ("alright", "pos"),
    ("all right", "pos"),
    ("yes", "pos"),
    ("yeah", "pos"),
    ("right", "pos")
    ]

cl = NaiveBayesClassifier(training_set)

#store synonums of specified word
dictionary=PyDictionary() 

#find all files in current directory that end in .txt
transcripts = glob.glob('*.txt')

row = input("Enter row number: ")

#make sure user is entering proper data type
while row.isdigit() == False:
    row = input("Number not recognized, please try again. Enter row number: ")
column = input("Enter column number: ")
while column.isdigit() == False:
    column = input("Number not recognized, please try again. Enter column number: ")
bool3 = True
bool1 = True
bool2 = True
bool4 = True

#iterate through all .txt files in directory
for filename in transcripts:
    topics = []
    
    #reopen file to start from beginning
    file = open(filename, "r+", encoding='utf-8', errors='ignore')
    output = open("./excel_output.xls", "a", encoding='utf-8', errors='ignore')
    output.write("\n")
    
    p = 1
    counter = 1
    string3 = ""
    for line in file:
        string3 = line.strip('\n')
        match0 = re.search('^R ',string3)
        if match0:
            counter+=1
    file.close()
    
    string2 = ""
    
    file = open(filename, "r+", encoding='utf-8', errors='ignore')
    i = 0
    q = 1
    r = 2
    if bool4:
        while r < int(row):
            output.write("%c" % ("\n"))
            r+=1
        bool4 = False
    while q < int(column):
        output.write("%c" % ("\t"))
        q+=1
    
    if bool1:
        count = input("Enter number of topics: ")
        while count.isdigit() == False:
            count = input("Number not recognized. Enter number of topics: ")
        bool1 = False
    while (i < int(count)) and bool3 == True:
        file = open(filename, "r+", encoding='utf-8', errors='ignore')
        words = []
        topic = input("Enter a topic: ")
        topics.append(topic)
        topicsFound = []
        wordCount = input("Enter number of words in topic: ")
        while count.isdigit() == False:
            wordCount = input("Number not recognized. Enter number of words in topic: ")
        j = 0
        while j < int(wordCount):
            w = input("Enter word: ")    
            words.append(w)
            words.append(topic)
            if w == "good":
                words.append("okay")
            
            for m in dictionary.synonym(w):
                words.append(m)
            count2 = 0
            k = 0
    
            responses = []
            for line in file:
                string2 = line.strip('\n')
                match = re.search('^R ',string2)
                if match:
                    responses.append(string2)
    
            for entry in responses:
                bool = False
                counter+=1
                
                for word in words:
                    for text in entry.split(" "):
                        if word == text.translate(string.punctuation).lower():
                            topicsFound.append(topic)
                            count2 += 1
                            bool = True
                            
                if (bool): 
                    classified_response = cl.classify(entry)  
                    final = topic + " - " + classified_response       
                    output.write("%s" % (final))
                else:
                    output.write("%s" % ("N/A"))        
                output.write("%c" % ("\t"))
    
            j += 1
            
        file.close()
        i += 1
    bool3 = False
    output.close()