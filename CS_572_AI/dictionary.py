#!/usr/bin/env python
''' Author  : Huy Nguyen
    Program : Store dictionary word to a data structure
    Start   : 09/28/2016
    End     : /2016
'''

'''
    function : given a text file of ward, provide a word list
    input    : text file
    output   : list
'''
def parse_text(myfile):
    out_list =[]
    infile = open(myfile,'r')
    for line in infile.readlines():
        out_list.append(line.strip())
    return out_list
    
class Dictionary(object):
    frequent_letter = ['a', 'e', 'i', 'o','u' ]
    alphabet_letter = set('qwertyuiopasdfghjklzxcvbnm')
    def __init__(self,infile):
        self.out_list = parse_text(infile)
    # variable that store 
    '''
        function : utility function that reduce time to go thorugh outfile
                  the idea is that to return a letter_freq dictionary (key: letter, value: freq), 
                  a length_freq dic (key: length of a word, value: freq of the length),
                  a length_word dic (key: length of a word, value: words of that length)
        input    : none
        output   : dic (wordFreq_from_letterFreq),dic (length_count), dic(length_to_word)
    '''   
    def utility_function(self):
        length_count ={} # ex: {5:12,7:108}
        length_to_word ={} # {5:['table','spong'],1:['a','b']}
        
        wordFreq_from_letterFreq = {} #{'able': .3451, 'table':1.234}
        letter_count = {}
        count = 0  # serve as the number of element in out_list
        total_letter = 0 # keep track of how many letter total
        # first pass through out_list, update count, and total letter,
        
        for word in self.out_list:
            count +=1 # update the count of number
            length = len(word)
            total_letter += length # update the total_letter
            # put in the length count dic
            if length in length_count:
                length_count[length] +=1
            else:
                length_count[length] = 1
            # put in the length to word dic
            if length in length_to_word:
                length_to_word[length].append(word)
            else:
                length_to_word[length] =[word]
            
            # update the letter_count
            for letter in word:
                if letter in letter_count:
                    letter_count[letter] +=1
                else:
                    letter_count[letter] =1
        # another pass through letter count to update wordFreq_from_letterFreq using total_letter
        for word in self.out_list:
            freq = 0
            for letter in word:
                freq += letter_count[letter]/total_letter
            wordFreq_from_letterFreq[word] = freq
        return wordFreq_from_letterFreq, length_count, length_to_word
                    
            

my_dic = Dictionary('words.txt') # create an onject Dictionary
wordFreq_from_letterFreq, length_count, length_to_word = my_dic.utility_function()

