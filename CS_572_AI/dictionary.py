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
    data =[]
    infile = open(myfile,'r')
    for line in infile.readlines():
        data.append(line.strip())
    return data
    
class Dictionary(object):
    def __init__(self,data):
        self.data = data
        self.alphabet_letter = set('qwertyuiopasdfghjklzxcvbnm')
    # variable that store 
    '''
        function : utility function that reduce time to go thorugh outfile
                  the idea is that to return 
                  a length_freq dic (key: length of a word, value: freq of the length),
                  a length_word dic (key: length of a word, value: words of that length)
        input    : none
        output   : dic (length_count), dic(length_to_word)
    '''   
    def utility_function(self):
        length_count ={} # ex: {5:12,7:108}
        length_to_word ={} # {5:['table','spong'],1:['a','b']}
        
        count = 0  # serve as the number of element in data
        total_letter = 0 # keep track of how many letter total
        # first pass through data, update count, and total letter,
        
        for word in self.data:
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
            
        return length_count, length_to_word
        
    '''
        function : given the word list, for each alphabet letter, provide the possibility
                   of the letter appear in our list
        input    : list (data)
        output   : dic (key: letter, value : probability)
    ''' 
    def alphabet_letter_freq(self):
        letter_probability = {}
        size = len(self.data)
        letter_count = {}
        for letter in self.alphabet_letter:
            letter_count[letter] = 0 # initiate count as 0
        for word in self.data: # go through each word in the word list
            for letter in letter_count: # for each letter appear, increment count by 1
                if letter in word:                
                    letter_count[letter] += 1 
        for letter in letter_count:
            letter_probability[letter] = letter_count[letter]/size
        return letter_probability
              
    '''
        function : given the the length of word  and dictionary length_to_word,
                    return the dictionary that keep track of frequency of each word
                    * this version uses naive frequency letter to calculate frequency of the word
        input    : self (basically get the list of word in the data as input)
        output   : dic (word_to_frequency,key: word, value : probability)
    ''' 
    def word_to_frequency(self):
        count = 0
        total_letter_count = 0
        letter_count = {}
        word_to_frequency ={}
        for word in self.data:
            count +=1 
            for letter in word:
                total_letter_count +=1
                if letter in letter_count:
                    letter_count[letter] +=1
                else:
                    letter_count[letter] =1
        for word in self.data:
            freq = 0
            for letter in word:
                freq += letter_count[letter]/total_letter_count
            word_to_frequency[word] = freq
        return word_to_frequency,count
        
    ############################################################################
    # helper functions 
        
    # functions that given word_to_frequency, return list of word with low frequency
    # take the 25% lowest
    def lowest_freq_words(self,word_to_frequency,count):
        min_freq = []
        limit = 0
        for word in sorted(word_to_frequency,key =word_to_frequency.get,reverse=True):
            if limit >= count/4:
                break
            count +=1
            min_freq.append(word)
        return min_freq
