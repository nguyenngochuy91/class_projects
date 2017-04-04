#!/usr/bin/env python
''' Author  : Huy Nguyen
    Program : Naive method with learning abilities
    Start   : 03/1/2017
    End     : 03/15/2017
'''

import argparse
import string 

translator = str.maketrans('', '', string.punctuation)
sentence_trans   = str.maketrans('', '', '!"#$%&\'()*+,-/:;<=>?@[\\]^_`{|}~')
# get the arguments from command line
def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--Input","-i",help="This is the book i want to summarize")
    parser.add_argument("--Output","-o", help="Summarize to this file")
    parser.add_argument("--StopWord","-w", help="Stop words file")
    parser.add_argument("--Sentences","-s", help="Number of sentence for summarize")
    args = parser.parse_args()
    return args

'''@function: given the a book, creae a dictionary that store info for each word
            frequency, remove the stop words
   @input   : text, stop_words
   @output  : dic (key: word, value: frequency)
'''  
def parse_text(myfile,stop_words):
    stop_words_list = open(stop_words,"r")
    book            = open(myfile,"r")
    stop_word_dic   = {}
    for line in stop_words_list.readlines():
        stop_word_dic[line.strip()] = None
    result = {}
    for paragraph in book.readlines():
        paragraph = paragraph.translate(translator).lower().split()
        for word in paragraph:
            if word in stop_word_dic:
                continue
            if word in result:
                result[word]+=1
            else:
                result[word]=1
    return result


'''@function: given the a result dic from above, and the number of sentence to 
            summarize into , return a string summarize to write out
   @input   : result, num sentence
   @output  : string
'''  
def summarize(myfile,result,num):
    result_list ={}
    book        = open(myfile,"r")
    for paragraph in book.readlines():
        new_paragraph = paragraph.translate(sentence_trans).lower().split(".")
        paragraph     = paragraph.split(".")
        for i in  range(len(new_paragraph)):
            count = 0
            for word in new_paragraph[i].split():
                if word in result:
                    count += result[word]
            result_list[paragraph[i]] = count
    count = 0
    my_list =[]
    for key in sorted(result_list, key = result_list.get,reverse= True):
        if key[0]== " ":           
            my_list.append(key[1].upper()+key[2:])
        else:
            my_list.append(key[0].upper()+key[1:])
        count +=1
        if count == num:
            break
    print (my_list)
    return ". ".join(my_list)
if __name__ == "__main__":
    args         = get_arguments()
    stop_words   = args.StopWord
    input_file   = args.Input
    output_file  = args.Output
    num_sentence = int(args.Sentences)
    frequency_dic = parse_text(input_file,stop_words)
    summary       = summarize(input_file,frequency_dic,num_sentence)
    file_out      = open(output_file,"w")
    file_out.write(summary)
    file_out.close()
    