#!/usr/bin/env python
''' Author  : Huy Nguyen
    Program : AI class strategy to give word , and an AI solver for the game
    Start   : 09/28/2016
    End     : /2016
'''
import random
from itertools import compress # this helps to modify list in O(n), with limited memory requirement.

class AI_Computer(object):
    def __init__(self,level = 'easy',dic=None):
        self.level = level # get the level
        self.dic = dic # pass the dic list of the dictionary of such length count
        self.set_levels = ["easy","medium","hard"]
        
    # given the level, choose a word in the dictionary based on the level.
    def choose_word(self):
        # for random, it will return 1 word
        if self.level == 'easy':
            word=  random.choice(self.dic.data)
            print ("level:",self.level)
        elif self.level == 'medium':
            # use the wordFreq_from_letterFreq and length_to_word to retrieve the lowest frequency
            word_to_frequency,count = self.dic.word_to_frequency()
            words                   = self.dic.lowest_freq_words(word_to_frequency,count)
            word=  random.choice(words)
            print ("level:",self.level)
        else: # means hard level
            word= None
        return word
class AI_solver(object):
    def __init__(self,dic = None,wrong_guess= set()):
        self.dic = dic # pass the dic list of the dictionary of such length count
                        # this list will get truncated after each of our guess
        self.wrong_guess = wrong_guess # set of letter that is not in the word
        self.number_of_try = 0 # use this to study how many time our solve fails a guess
    '''
        function : for each guess, provide letter and it's probability to be in our 
        word
        input    : list(index of letters correctly guessed from hangman),string (guessed letter)
        output   : dic (key: alphabet letter, value: probability)
    '''
    def solve(self,index_list,letter): # keep solving until win or lose
        letter_probability = {}
        # rationalize about the new letter
        if len(index_list) == 0: # this means it is a wrong guess
            self.wrong_guess.add(letter) 
            self.number_of_try+=1 # increment the time we fail
            # call the method to remove all word in our dic that has such letter
            self.remove_word_with_letter(letter)
        else: # means that the letter is a write guess, eliminate those words in dic that 
              # does not comply to have such letter at index in index_list
            self.remove_word_not_comply(index_list,letter)
            # also remove the letter from our alphabet, since it appears always so the count is 1
            self.dic.alphabet_letter.remove(letter)
            
        # from the dic, calling method in the dictionary class to calculate 
        letter_probability = self.dic.alphabet_letter_freq()
        return letter_probability
    ############################################################################
    # helper functions 
        
    # given letter_probability dic, print out the top 5 highest probable words
    def print_top_5(self,letter_probability):
        count = 0
        for item in sorted(letter_probability,key = letter_probability.get,reverse=True):
            if count == 5:
                break
            print (item+":"+str(letter_probability[item]))
            count +=1
        return None
        
    # remove word in dic that contains letter from input in O(n)
    def remove_word_with_letter(self,letter):
        selectors = (letter not in word for word in self.dic.data) # our selectors won't have letter
        
        for i,word in enumerate(compress(self.dic.data,selectors)): # enumerate elemenets does not have letter:
            self.dic.data[i] = word # move found element to the beginning of the list, without resizing
        del self.dic.data[i+1:] # trim the end of the list
        
    # remove word in dic that does not have letter at index in index_list 
    def remove_word_not_comply(self,index_list,letter):
        # helper function to return boolean for remove_word_not_comply selector    
        def check_word(index_list,word,letter):
            flag = True
            for index in index_list:
                if word[index] != letter:
                    flag = False
                    break
            return flag
        selectors = (check_word(index_list,word,letter) for word in self.dic.data)
        for i,word in enumerate(compress(self.dic.data,selectors=selectors)): # enumerate elemenets does not have letter:
            self.dic.data[i] = word # move found element to the beginning of the list, without resizing
        del self.dic.data[i+1:] # trim the end of the list
