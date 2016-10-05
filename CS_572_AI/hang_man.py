#!/usr/bin/env python
''' Author  : Huy Nguyen
    Program : hang_man class game
    Start   : 09/28/2016
    End     : /2016
'''
import dictionary
class HangMan(object):
    def __init__(self,chances = 7,word_length = 8, data ='words.txt'):
        self.chances = chances
        self.word_length = word_length
        self.data = dictionary.Dictionary('words.txt') # pass dictionary object
        self.success = False # initiate the game as False
        
    # play the game function (main function)
    def play(self):
        # pull the data
        wordFreq_from_letterFreq, length_count, length_to_word = self.data.utility_function()
        # Initialize the game
        word, game_state,guessed_letters = self.initialize(length_count,length_to_word)
        while not self.is_end_game(game_state,self.chances,word):
            game_state,self.chances,guessed_letters = self.play_a_turn(game_state,
                                                                       self.chances,word,
                                                                       guessed_letters) # play a turn
    ''' 
        function: from dictionary of length word to word, ask user for which word
                to choose, then initialize the game with the word and the state
                of the game (or the string of letter to solve)
        input  : dic (length_count), dic(length_to_word) from function play
        output : string (word choice), list(state of the game represent by numeral _), set (guessed_letters)
    '''           
    def initialize(self,length_count,length_to_word):
        guessed_letters = set()
        # initialize game state 
        game_state =[]
        for letter in range(self.word_length):
            game_state.append('_')
        # list of the word of such length to choose (print about 50 of them)
        print ("Here are possible words of such length:")
        if length_count[self.word_length] >=50:
            print (length_to_word[self.word_length][:50])
        else:
            print (length_to_word[self.word_length])
        word = str(input("Please choose a word of length "+str(self.word_length)+":"))
        while len(word) != self.word_length or word not in length_to_word[self.word_length]:
            word = str(input("Invalid choice. Please choose a word of length "+str(self.word_length)+":"))
        return word, game_state,guessed_letters
        
    ''' 
        function: given the word and chances, ask the user for letter input 
                  and derive new states, and new chances.
        input  : str(game_state),int(chances),str(word)
        output : str(game_state),int(chances)
    '''  
    def play_a_turn(self,game_state,chances,word,guessed_letters):
        print ("You have guessed:",guessed_letters)
        letter = str(input("Please chose an alphabet letter:"))
        while letter in guessed_letters or letter not in self.data.alphabet_letter:
            letter = str(input("Please provide a proper alphabet letter:"))
        # add the letter to guessed_letters
        guessed_letters.add(letter)
        index_list = self.find_all(word,letter)  # find all the index of letter in word
        if len(index_list ) ==0: # cant find any
            chances -= 1 # update chance if guess wrong
            print ("You have guessed wrongly")
            self.print_state(game_state,chances)
        else:
            game_state = self.update(index_list,game_state,letter)
            print ("You have guessed rightly")
            self.print_state(game_state,chances)
        return game_state,chances,guessed_letters
        
    ######################################
    # helper functions
    
    # given a right move, update the game state
    def update(self,index_list,game_state,letter):
        for index in index_list:
            game_state[index] = letter
        return game_state
    
    # given a letter, find all the index 
    def find_all(self,word,letter):
        index_list =[]
        for index in range(len(word)):
            if word[index] == letter:
                index_list.append(index)
        return index_list
            
        
    # print state game and chances left
    def print_state(self,game_state,chances):
        print ("You have "+str(chances) +" chances left")
        print ("The string so far is :")
        string =""
        for item in game_state:
            string+=item+"  "
        print (string)
    
    # check if end state of game, it prints the the state of the game
    def is_end_game(self,game_state,chances,word):
        if '_' not in game_state: # check if the word is solve
            print ("You have successfully solved it, congratz")
            self.print_state(game_state,chances) # print state
            return True
        else:
            # if not solved, but chances are 0, then the player lost
            if chances ==0:
                print ("Oops, you have lost")
                self.print_state(game_state,chances) # print state
                print ("Here is the word:" + word)
                return True
            else:
                return False
            
                
 
                    
def main():
    chances = int(input("Please indicate how many chances player can have:"))
    word_length = int(input("Please indicate what length to choose:"))
    # create a Hangman object
    game = HangMan(chances,word_length,'words.txt')
    game.play()
    string = str(input("Do you want to play again? (y:yes, n : no)"))
    while string.lower() == 'y':
        chances = int(input("Please indicate how many chances player can have:"))
        word_length = int(input("Please indicate what length to choose:"))
        game = HangMan(chances,word_length,'words.txt')
        game.play()    
    
main()