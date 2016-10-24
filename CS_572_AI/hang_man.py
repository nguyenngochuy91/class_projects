#!/usr/bin/env python
''' Author  : Huy Nguyen
    Program : hang_man class game
    Start   : 09/28/2016
    End     : /2016
'''
import dictionary
import AI
from colorama import Fore,Style
class HangMan(object):
    def __init__(self,chances = 7,word_length = 8, data = None ,multiplayer = 'y'):
        self.chances         = chances
        self.game_state      = [] # initiate game state as None
        self.guessed_letters = set() # initiate guessed letter as empty
        self.word            = None # initiate the word as empty, 
                                    # if its normal hangman, then it is a string
                                    # if evil, then it is a bag of possible word
        
        self.index_list      = [] # this index_list helps the solver to quicker 
                                  # reduce the potential words (less comparison)
        
        self.word_length     = word_length
        self.data            = data # pass dictionary object
        self.success         = False # initiate the game as False
        self.multiplayer     = multiplayer # indicate that we play human vs human
        self.solver          = AI.AI_solver() # initiate a solver
    # play the game function (main function)
    def play(self):
        # pull the data
        length_count, length_to_word = self.data.utility_function()

        # Initialize the game
        self.initialize(length_count,length_to_word)
        #  initiate a solver
        while not self.is_end_game():
            self.play_a_turn() # play a turn
    ''' 
        function : from dictionary of length word to word, ask user for which word
                to choose, then initialize the game with the word and the state
                of the game (or the string of letter to solve)
        input    : dic (length_count), dic(length_to_word) from function play
        output   : string (word choice)
    '''           
    def initialize(self,length_count,length_to_word):
        self.guessed_letters = set()
        # initialize game state 
        for letter in range(self.word_length):
            self.game_state.append('_')
            
        if self.multiplayer.lower() == 'y':
            # list of the word of such length to choose (print about 50 of them)
            print ("Here are possible words of such length: ")
            if length_count[self.word_length] >=50:
                print (length_to_word[self.word_length][:50])
            else:
                print (length_to_word[self.word_length])
            word = str(input("Please choose a word of length "+str(self.word_length)+": "))
            while len(word) != self.word_length or word not in length_to_word[self.word_length]:
                word = str(input("Invalid choice. Please choose a word of length "+str(self.word_length)+":" ))
        else:
            ## create an AI to get a word of length based on level.
            level = str(input("Please choose a level (easy,medium,hard): "))
            # create an instant of AI_computer based on level
            computer = AI.AI_Computer(level,dictionary.Dictionary(length_to_word[self.word_length]) )
            # choose a word using the level
            word = computer.choose_word().lower()
            # print ("word:",word)
        self.word = word # initial our word
        self.solver.dic = dictionary.Dictionary(length_to_word[self.word_length]) #  object initial our solver data as a dictionary
        
        
    ''' 
        function : given the word and chances, ask the user for letter input 
                  and derive new states, and new chances. Also, it will update wrong guess
                  for the AI solver
              
        input    : str(word)
        output   : str(game_state),int(chances)
    '''  
    def play_a_turn(self):
        print (Fore.RED +"The letters you have guessed: "+str(self.guessed_letters)+Style.RESET_ALL)
        print ("alphabet_letter: ",self.data.alphabet_letter)
        # get the letter input from user
        letter = str(input("Please chose an alphabet letter: "))
        while letter not in self.data.alphabet_letter or letter in self.guessed_letters:
            letter = str(input("Please provide a proper alphabet letter: "))
        # add the letter to guessed_letters
        self.guessed_letters.add(letter)
        self.find_all(letter)  # find all the index of letter in word
        
        if len(self.index_list) ==0: # cant find any
            self.chances -= 1 # update chance if guess wrong
            print ("You have guessed wrongly")
            self.print_state()
        else:
            
            self.update(letter) # else, using the index in our current index list to update the game state
            print ("You have guessed rightly")
            self.print_state()
            
        # using the updated index_list, and the letter, our AI class method solve
        # will reason whether if the letter is a wrong guess or not and provide
        # next suggestions
        suggestions = self.solver.solve(self.index_list,letter)
        # print those suggestions
        print ("Here are the top 5 most probable letters: ")
        self.solver.print_top_5(suggestions) 
        
    ############################################################################
    # helper functions
    
    # given a right move, update the game state
    def update(self,letter):
        for index in self.index_list:
            self.game_state[index] = letter
            
    # given a letter, find all the index 
    def find_all(self,letter):
        self.index_list =[]
        for index in range(len(self.word)):
            if self.word[index] == letter:
                self.index_list.append(index)
            
        
    # print state game and chances left
    def print_state(self):
        print ("You have "+str(self.chances) +" chances left")
        print ("The string so far is : ")
        string =""
        for item in self.game_state:
            string+=item+"  "
        print (Fore.GREEN + string+ Style.RESET_ALL)
    
    # check if end state of game, it prints the the state of the game
    def is_end_game(self):
        if '_' not in self.game_state: # check if the word is solve
            print ("You have successfully solved it, congratz")
            self.print_state() # print state
            return True
        else:
            # if not solved, but chances are 0, then the player lost
            if self.chances ==0:
                print ("Oops, you have lost")
                self.print_state() # print state
                print ("Here is the word: " + self.word)
                return True
            else:
                return False
            
                
 
                    
def main():
    dictionary_word = str(input("which dictionary you want to use ('words.txt','words2.txt','words3.txt'): "))
    chances = int(input("Please indicate how many chances player can have: "))
    word_length = int(input("Please indicate what length to choose: "))
    mutiplayer = str(input("Do you want to play with a human(y,n): "))
    # create a Hangman object
    diction = dictionary.Dictionary(dictionary.parse_text(dictionary_word))
    game = HangMan(chances,word_length, diction,mutiplayer)
    game.play()
    string = str(input("Do you want to play again? (y:yes, n : no) "))
    while string.lower() == 'y':
        chances = int(input("Please indicate how many chances player can have: "))
        word_length = int(input("Please indicate what length to choose: "))
        game = HangMan(chances,word_length,diction,mutiplayer)
        game.play()    
        string = str(input("Do you want to play again? (y:yes, n : no) "))
    
main()
