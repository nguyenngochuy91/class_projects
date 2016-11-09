#!/usr/bin/env python
''' Author  : Huy Nguyen
    Program : AI class strategy to give word , and an AI solver for the game
                and an AI that find the best string of letter to guess given the level
                is hard.
    Start   : 09/28/2016
    End     : /2016
'''
import random
from itertools import compress # this helps to modify list in O(n), with limited memory requirement.
import itertools
import dictionary
import copy
###############################################################################
## AI computer to choose word (level)
###############################################################################
class AI_Computer(object):
    def __init__(self,level = 'easy',dic=None):
        self.level = level # get the level
        self.dic = dic # pass the dic list of the dictionary of such length count
        self.index_list =[]
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
        elif self.level == 'hard' or self.level == "insane" or self.level =="intermediate":
            word = self.dic.data
        return word # could be a word, or list of word
    
    '''
        function : given a guessed letter, this will filter the word list (only 
                   get invoked if the level is hard).
                   In this method, naively try to remove as much letter the user
                   guess as possible (greedy)
                   If it returns a single word, then switch is yes
        input    : guessed letter, and utilize the current self.dic.data
        output   : list (updated self.dic.data), list( of index), switch (boolean)
    '''
    def naive_filter(self,letter):
        selectors = (letter not in word for word in self.dic.data) # our selectors won't have letter     
        count = 0
        for i,word in enumerate(compress(self.dic.data,selectors)): # enumerate elemenets does not have letter:
            count +=1
            self.dic.data[i] = word # move found element to the beginning of the list, without resizing
        # print (self.dic.data)
        if count == 0: # this means that either all of them has such letter 
            word = random.choice(self.dic.data)
            self.index_list = self.find_all(word,letter)
            return word,self.index_list, True
        elif count == 1:
            self.index_list = self.find_all(self.dic.data[0],letter)
            return self.dic.data[0],self.index_list, True # return the only word with no letter occurence, and index is as 0 
        else:
            del self.dic.data[i+1:] # remove those that have the letter
            return self.dic.data, self.index_list, False
            
    '''
        function : given a guessed letter, this will categorize the list of words into classes.
                   Then, it will use the class with most number of words. and list of index
                   such letter appear
        input    : guessed letter, and utilize the current self.dic.data
        output   : list (updated self.dic.data), list( of index), switch (boolean)
    '''
    def class_size_filter(self,letter):
        # partition
        max_words, index_list,self.dic.data = self.partition(letter) 
        # convert the index string into normal index 
        self.index_list = []
        for index in index_list:
            self.index_list.append(int(index))
        if max_words == 1: # there is only 1 word left
            return self.dic.data, self.index_list, True
        else:
            return self.dic.data, self.index_list, False 
                    
    ###########################################################################
    # helper functions
    # given a letter and word, find all the index 
    def find_all(self,word,letter):
        index_list =[]
        for index in range(len(word)):
            if word[index] == letter:
                index_list.append(index)
        return index_list
        
    # given a letter and word, find all the index , return as a string
    def find_all_as_string(self,word,letter):
        index_list =""
        for index in range(len(word)):
            if word[index] == letter:
                index_list+= str(index)
        return index_list
    
    # given a guessed letter, partition our data into different categories
    # return a max_words, index list, and the word list
    def partition(self,letter):
        dic = {} # key is the index list that the letter appear in word, value is the list of word
        max_words = 0 # keep track which one has maximum number of words
        most_words_at_index = None
        index_list = None
        for word in self.dic.data:
            # get all the index of letter appear in word
            temp_index = self.find_all_as_string(word,letter)
            if temp_index in dic: # if such index list is in dic already
                # adding the word using category add word function
                dic[temp_index].add_word(word)
            # if not in dic, then initiate the category object
            else:
                dic[temp_index] = category([word],1)
        
        # get the one with max
        for index in dic:
            if max_words < dic[index].count:
                max_words = dic[index].count
                index_list = index # assign the index_list
                most_words_at_index = dic[index].word_list
        return max_words,index_list,most_words_at_index
        
###############################################################################        
## AI solver given the data find the most probable letter  
###############################################################################
        
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
        # print (self.dic.data)
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
        
###############################################################################
## AI class that given the hard level strategy, find the most probable
## series of letter to guess
###############################################################################
        
class AI_hard_solver(object):
    def __init__(self,dic = None,wrong_guess= ''):
        self.dic = dic # pass the dic list of the dictionary of such length count
                        # this list will get truncated after each of our guess
        self.wrong_guess = wrong_guess # set of letter that is not in the word
        self.number_of_try = 0 # use this to study how many time our solve fails a guess
        self.alphabet = set('qwertyuiopasdfghjklzxcvbnm')
        self.index_list = None
        self.guess_string = ''
    '''
        function : Given then data bag of word, utilize the hard level strategy,
                    find the shortest sequence of letter to guess
        input    : None
        output   : string (letters)
    '''
    def solve(self):
        AI   = AI_Computer('hard',self.dic)
        finish = False
        solver = AI_solver()
        solver.dic = self.dic
        letter_probability = self.dic.alphabet_letter_freq()
        ## getting a guidline number using the AI normal solver 
        while not finish:
            for item in sorted(letter_probability,key = letter_probability.get,reverse=True):
                letter = item
                break
            self.alphabet.remove(letter)
            self.number_of_try += 1 # increment the total number of trial
            self.dic.data, self.index_list, finish  = AI.class_size_filter(letter)
            if len(self.index_list) == 0: # wrong guess
                self.wrong_guess +=letter
            self.guess_string += letter
            letter_probability = solver.solve(self.index_list,letter)
        min_wrong_guess = self.wrong_guess
        min_guess_string = self.guess_string
        length_wrong_guess = len(self.wrong_guess)
        
    '''
        function : Given then data bag of word, utilize the hard level strategy,
                    find the shortest sequence of letter to guess
        input    : None
        output   : string (letters)
    '''
    def test(self):
        finish = False
        ## getting a guidline number using the AI normal solver 
        result ={}
        for i in range(1,4):
            current = list(itertools.permutations(self.alphabet,i))
            local_max= 0
            local_data = None
            sequence = None
            for permutation in current:
                AI   = AI_Computer('hard',copy.deepcopy(self.dic))
                for letter in permutation:
                    data, index_list, finish = AI.class_size_filter(letter)
                # print (permutation,data)
                if local_max < 1/len(data):
                    local_data = data
                    sequence = permutation
            result[sequence] = len(local_data)
        return result
###############################################################################
## helper classes
class category(object):
    def __init__(self,word_list,count):
        self.word_list = word_list
        self.count     = count 
        
    def add_word(self,word):
        self.word_list.append(word)
        self.count +=1
        
    def get_count(self):
        return self.count
        
    def get_word_list(self):
        return self.word_list

class guessed_letter(object):
    def __init__(self,alphabet,count):
        self.alphabet = alphabet
        self.count     = count 
        
###############################################################################
# testing AI_hard_solver
diction = dictionary.Dictionary(dictionary.parse_text('words.txt'))
length_count, length_to_word = diction.utility_function()
## using 1st strategy
#solver = AI_hard_solver()
#solver.dic = dictionary.Dictionary(length_to_word[5])
#solver.solve()
#shortest = solver.wrong_guess
#gues_string = solver.guess_string
#word =  solver.dic.data
## using2nd strategy
solver = AI_hard_solver()
solver.dic = dictionary.Dictionary(length_to_word[5])
result = solver.test()
