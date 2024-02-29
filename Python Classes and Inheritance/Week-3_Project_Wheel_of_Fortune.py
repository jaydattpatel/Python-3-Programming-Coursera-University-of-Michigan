'''
author : Jaydatt Patel

Python Classes and Inheritance on Coursera (University of Michigan)

Week - 3 Project: Wheel of Fortune

https://runestone.academy/ns/books/published/fopp/Inheritance/chapterProject.html

This project will take you through the process of implementing a simplified version of the game Wheel of Fortune. Here are the rules of our game:

There are num_human human players and num_computer computer players.
Every player has some amount of money ($0 at the start of the game)

Every player has a set of prizes (none at the start of the game)

The goal is to guess a phrase within a category. For example:
Category: Artist & Song

Phrase: Whitney Houston’s I Will Always Love You

Players see the category and an obscured version of the phrase where every alphanumeric character in the phrase starts out as hidden (using underscores: _):
Category: Artist & Song

Phrase: _______ _______'_ _ ____ ______ ____ ___

Note that case (capitalization) does not matter

During their turn, every player spins the wheel to determine a prize amount and:
If the wheel lands on a cash square, players may do one of three actions:
Guess any letter that hasn’t been guessed by typing a letter (a-z)
Vowels (a, e, i, o, u) cost $250 to guess and can’t be guessed if the player doesn’t have enough money. All other letters are “free” to guess

The player can guess any letter that hasn’t been guessed and gets that cash amount for every time that letter appears in the phrase

If there is a prize, the user also gets that prize (in addition to any prizes they already had)

If the letter does appear in the phrase, the user keeps their turn. Otherwise, it’s the next player’s turn

Example: The user lands on $500 and guesses ‘W’
There are three W’s in the phrase, so the player wins $1500

Guess the complete phrase by typing a phrase (anything over one character that isn’t ‘pass’)
If they are correct, they win the game

If they are incorrect, it is the next player’s turn

Pass their turn by entering 'pass'

If the wheel lands on “lose a turn”, the player loses their turn and the game moves on to the next player

If the wheel lands on “bankrupt”, the player loses their turn and loses their money but they keep all of the prizes they have won so far.

The game continues until the entire phrase is revealed (or one player guesses the complete phrase)


'''

import sys
sys.setExecutionLimit(600000) # let this take up to 10 minutes

import json
import random
import time

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
VOWELS  = 'AEIOU'
VOWEL_COST  = 250


class WOFPlayer :
    def __init__(self,name):
        self.name = name
        self.prizeMoney = 0
        self.prizes = []

    def addMoney(self,amt):
        self.prizeMoney += amt

    def goBankrupt(self):
        self.prizeMoney = 0

    def addPrize(self,prize):
        self.prizes += [prize]

    def __str__(self):
        return "{} (${})".format(self.name,self.prizeMoney)
    

class WOFHumanPlayer(WOFPlayer):
    def __init__(self,name):
        WOFPlayer.__init__(self,name)

    def getMove(self,category, obscuredPhrase, guessed):
        self.category = category 
        self.obscuredPhrase =obscuredPhrase
        self.guessed =guessed
        s = input('''{name} has ${prizeMoney}\n\nCategory: {category}\nPhrase:  {obscuredPhrase}\nGuessed: {guessed}\n\n
              Guess a letter, phrase, or type 'exit' or 'pass':'''.format(name = self.name, prizeMoney = self.prizeMoney,
              category = self.category, obscuredPhrase = self.obscuredPhrase, guessed = self.guessed))
        return (s)
    
class WOFComputerPlayer(WOFPlayer):
    SORTED_FREQUENCIES = 'ZQXJKVBPYGFWMUCLDRHSNIOATE'

    def __init__(self,name,difficulty):
        WOFPlayer.__init__(self,name)
        self.difficulty = difficulty
    
    def smartCoinFlip(self):
        ran = random.randint(1, 10)
        if ran > self.difficulty:
            return True
        else: 
            return False
        
    def getPossibleLetters(self,guessed):
        possible_letters = [c for c in LETTERS if c not in guessed]

        possible_letters_without_VOWELS = [c for c in possible_letters if c not in VOWELS]

        if self.prizeMoney < VOWEL_COST:     
            return possible_letters_without_VOWELS
        if self.prizeMoney >= VOWEL_COST:
            return possible_letters

    def getMove(self,category, obscuredPhrase, guessed):
        self.category = category 
        self.obscuredPhrase = obscuredPhrase
        possible_letters = self.getPossibleLetters(guessed)
        if (len(possible_letters) == 0):
            return 'pass'
        else:
            if (self.smartCoinFlip() == True):
                l = ''
                size = len(self.SORTED_FREQUENCIES)-1
                i = size
                while (i>=0):
                    if self.SORTED_FREQUENCIES[i] in possible_letters:
                        l = self.SORTED_FREQUENCIES[i]
                        break
                    i -= 1 
                return l
            else:
                return random.choice(possible_letters)
        


# Repeatedly asks the user for a number between min & max (inclusive)
def getNumberBetween(prompt, min, max):
    userinp = input(prompt) # ask the first time

    while True:
        try:
            n = int(userinp) # try casting to an integer
            if n < min:
                errmessage = 'Must be at least {}'.format(min)
            elif n > max:
                errmessage = 'Must be at most {}'.format(max)
            else:
                return n
        except ValueError: # The user didn't enter a number
            errmessage = '{} is not a number.'.format(userinp)

        # If we haven't gotten a number yet, add the error message
        # and ask again
        userinp = input('{}\n{}'.format(errmessage, prompt))

# Spins the wheel of fortune wheel to give a random prize
# Examples:
#    { "type": "cash", "text": "$950", "value": 950, "prize": "A trip to Ann Arbor!" },
#    { "type": "bankrupt", "text": "Bankrupt", "prize": false },
#    { "type": "loseturn", "text": "Lose a turn", "prize": false }
def spinWheel():
    with open("wheel.json", 'r') as f:
        wheel = json.loads(f.read())
        return random.choice(wheel)

# Returns a category & phrase (as a tuple) to guess
# Example:
#     ("Artist & Song", "Whitney Houston's I Will Always Love You")
def getRandomCategoryAndPhrase():
    with open("phrases.json", 'r') as f:
        phrases = json.loads(f.read())

        category = random.choice(list(phrases.keys()))
        phrase   = random.choice(phrases[category])
        return (category, phrase.upper())

# Given a phrase and a list of guessed letters, returns an obscured version
# Example:
#     guessed: ['L', 'B', 'E', 'R', 'N', 'P', 'K', 'X', 'Z']
#     phrase:  "GLACIER NATIONAL PARK"
#     returns> "_L___ER N____N_L P_RK"
def obscurePhrase(phrase, guessed):
    rv = ''
    for s in phrase:
        if (s in LETTERS) and (s not in guessed):
            rv = rv+'_'
        else:
            rv = rv+s
    return rv

# Returns a string representing the current state of the game
def showBoard(category, obscuredPhrase, guessed):
    return """
Category: {}
Phrase:   {}
Guessed:  {}""".format(category, obscuredPhrase, ', '.join(sorted(guessed)))

# GAME LOGIC CODE
print('='*15)
print('WHEEL OF PYTHON')
print('='*15)
print('')

num_human = getNumberBetween('How many human players?', 0, 10)

# Create the human player instances
human_players = [WOFHumanPlayer(input('Enter the name for human player #{}'.format(i+1))) for i in range(num_human)]

num_computer = getNumberBetween('How many computer players?', 0, 10)

# If there are computer players, ask how difficult they should be
if num_computer >= 1:
    difficulty = getNumberBetween('What difficulty for the computers? (1-10)', 1, 10)

# Create the computer player instances
computer_players = [WOFComputerPlayer('Computer {}'.format(i+1), difficulty) for i in range(num_computer)]

players = human_players + computer_players

# No players, no game :(
if len(players) == 0:
    print('We need players to play!')
    raise Exception('Not enough players')

# category and phrase are strings.
category, phrase = getRandomCategoryAndPhrase()
# guessed is a list of the letters that have been guessed
guessed = []

# playerIndex keeps track of the index (0 to len(players)-1) of the player whose turn it is
playerIndex = 0

# will be set to the player instance when/if someone wins
winner = False

def requestPlayerMove(player, category, guessed):
    while True: # we're going to keep asking the player for a move until they give a valid one
        time.sleep(0.1) # added so that any feedback is printed out before the next prompt

        move = player.getMove(category, obscurePhrase(phrase, guessed), guessed)
        move = move.upper() # convert whatever the player entered to UPPERCASE
        if move == 'EXIT' or move == 'PASS':
            return move
        elif len(move) == 1: # they guessed a character
            if move not in LETTERS: # the user entered an invalid letter (such as @, #, or $)
                print('Guesses should be letters. Try again.')
                continue
            elif move in guessed: # this letter has already been guessed
                print('{} has already been guessed. Try again.'.format(move))
                continue
            elif move in VOWELS and player.prizeMoney < VOWEL_COST: # if it's a vowel, we need to be sure the player has enough
                    print('Need ${} to guess a vowel. Try again.'.format(VOWEL_COST))
                    continue
            else:
                return move
        else: # they guessed the phrase
            return move


while True:
    player = players[playerIndex]
    wheelPrize = spinWheel()

    print('')
    print('-'*15)
    print(showBoard(category, obscurePhrase(phrase, guessed), guessed))
    print('')
    print('{} spins...'.format(player.name))
    time.sleep(2) # pause for dramatic effect!
    print('{}!'.format(wheelPrize['text']))
    time.sleep(1) # pause again for more dramatic effect!

    if wheelPrize['type'] == 'bankrupt':
        player.goBankrupt()
    elif wheelPrize['type'] == 'loseturn':
        pass # do nothing; just move on to the next player
    elif wheelPrize['type'] == 'cash':
        move = requestPlayerMove(player, category, guessed)
        if move == 'EXIT': # leave the game
            print('Until next time!')
            break
        elif move == 'PASS': # will just move on to next player
            print('{} passes'.format(player.name))
        elif len(move) == 1: # they guessed a letter
            guessed.append(move)

            print('{} guesses "{}"'.format(player.name, move))

            if move in VOWELS:
                player.prizeMoney -= VOWEL_COST

            count = phrase.count(move) # returns an integer with how many times this letter appears
            if count > 0:
                if count == 1:
                    print("There is one {}".format(move))
                else:
                    print("There are {} {}'s".format(count, move))

                # Give them the money and the prizes
                player.addMoney(count * wheelPrize['value'])
                if wheelPrize['prize']:
                    player.addPrize(wheelPrize['prize'])

                # all of the letters have been guessed
                if obscurePhrase(phrase, guessed) == phrase:
                    winner = player
                    break

                continue # this player gets to go again

            elif count == 0:
                print("There is no {}".format(move))
        else: # they guessed the whole phrase
            if move == phrase: # they guessed the full phrase correctly
                winner = player

                # Give them the money and the prizes
                player.addMoney(wheelPrize['value'])
                if wheelPrize['prize']:
                    player.addPrize(wheelPrize['prize'])

                break
            else:
                print('{} was not the phrase'.format(move))

    # Move on to the next player (or go back to player[0] if we reached the end)
    playerIndex = (playerIndex + 1) % len(players)

if winner:
    # In your head, you should hear this as being announced by a game show host
    print('{} wins! The phrase was {}'.format(winner.name, phrase))
    print('{} won ${}'.format(winner.name, winner.prizeMoney))
    if len(winner.prizes) > 0:
        print('{} also won:'.format(winner.name))
        for prize in winner.prizes:
            print('    - {}'.format(prize))
else:
    print('Nobody won. The phrase was {}'.format(phrase))




'''
===============
WHEEL OF PYTHON
===============


---------------

Category: Author & Title
Phrase:   ___ _____ ______ __ _. _____ __________
Guessed:  

h1m spins...
$650!
h1m guesses "X"
There is no X

---------------

Category: Author & Title
Phrase:   ___ _____ ______ __ _. _____ __________
Guessed:  X

h2m spins...
900!
h2m guesses "Z"
There is one Z

---------------

Category: Author & Title
Phrase:   ___ _____ ______ __ _. _____ ___Z______
Guessed:  X, Z

h2m spins...
$2500!
h2m guesses "G"
There are 3 G's

---------------

Category: Author & Title
Phrase:   ___ G____ G_____ __ _. _____ ___ZG_____
Guessed:  G, X, Z

h2m spins...
$700!
h2m guesses "H"
There is one H

---------------

Category: Author & Title
Phrase:   _H_ G____ G_____ __ _. _____ ___ZG_____
Guessed:  G, H, X, Z

h2m spins...
$650!
h2m passes

---------------

Category: Author & Title
Phrase:   _H_ G____ G_____ __ _. _____ ___ZG_____
Guessed:  G, H, X, Z

h3m spins...
One Million!
Need $250 to guess a vowel. Try again.
Z has already been guessed. Try again.
Need $250 to guess a vowel. Try again.
Need $250 to guess a vowel. Try again.
h3m guesses "J"
There is no J

---------------

Category: Author & Title
Phrase:   _H_ G____ G_____ __ _. _____ ___ZG_____
Guessed:  G, H, J, X, Z

Computer 1 spins...
$700!
Computer 1 guesses "T"
There are 6 T's

---------------

Category: Author & Title
Phrase:   TH_ G___T G_T___ __ _. ___TT __TZG_____
Guessed:  G, H, J, T, X, Z

Computer 1 spins...
$700!
Computer 1 guesses "O"
There is one O

---------------

Category: Author & Title
Phrase:   TH_ G___T G_T___ __ _. __OTT __TZG_____
Guessed:  G, H, J, O, T, X, Z

Computer 1 spins...
$2500!
Computer 1 guesses "E"
There are 3 E's

---------------

Category: Author & Title
Phrase:   THE G_E_T G_T___ __ _. __OTT __TZGE____
Guessed:  E, G, H, J, O, T, X, Z

Computer 1 spins...
$700!
Computer 1 guesses "Q"
There is no Q

---------------

Category: Author & Title
Phrase:   THE G_E_T G_T___ __ _. __OTT __TZGE____
Guessed:  E, G, H, J, O, Q, T, X, Z

Computer 2 spins...
Bankrupt!

---------------

Category: Author & Title
Phrase:   THE G_E_T G_T___ __ _. __OTT __TZGE____
Guessed:  E, G, H, J, O, Q, T, X, Z

h1m spins...
Bankrupt!

---------------

Category: Author & Title
Phrase:   THE G_E_T G_T___ __ _. __OTT __TZGE____
Guessed:  E, G, H, J, O, Q, T, X, Z

h2m spins...
$800!
h2m guesses "R"
There are 2 R's

---------------

Category: Author & Title
Phrase:   THE GRE_T G_T___ __ _. __OTT __TZGER___
Guessed:  E, G, H, J, O, Q, R, T, X, Z

h2m spins...
$700!
h2m passes

---------------

Category: Author & Title
Phrase:   THE GRE_T G_T___ __ _. __OTT __TZGER___
Guessed:  E, G, H, J, O, Q, R, T, X, Z

h3m spins...
$900!
Need $250 to guess a vowel. Try again.
h3m guesses "Y"
There are 2 Y's

---------------

Category: Author & Title
Phrase:   THE GRE_T G_T__Y _Y _. __OTT __TZGER___
Guessed:  E, G, H, J, O, Q, R, T, X, Y, Z

h3m spins...
$650!
h3m guesses "P"
There is no P

---------------

Category: Author & Title
Phrase:   THE GRE_T G_T__Y _Y _. __OTT __TZGER___
Guessed:  E, G, H, J, O, P, Q, R, T, X, Y, Z

Computer 1 spins...
Lose a turn!

---------------

Category: Author & Title
Phrase:   THE GRE_T G_T__Y _Y _. __OTT __TZGER___
Guessed:  E, G, H, J, O, P, Q, R, T, X, Y, Z

Computer 2 spins...
$800!
Computer 2 guesses "N"
There is no N

---------------

Category: Author & Title
Phrase:   THE GRE_T G_T__Y _Y _. __OTT __TZGER___
Guessed:  E, G, H, J, N, O, P, Q, R, T, X, Y, Z

h1m spins...
$2500!
h1m guesses "L"
There is one L

---------------

Category: Author & Title
Phrase:   THE GRE_T G_T__Y _Y _. __OTT __TZGER_L_
Guessed:  E, G, H, J, L, N, O, P, Q, R, T, X, Y, Z

h1m spins...
$650!
h1m guesses "W"
There is no W

---------------

Category: Author & Title
Phrase:   THE GRE_T G_T__Y _Y _. __OTT __TZGER_L_
Guessed:  E, G, H, J, L, N, O, P, Q, R, T, W, X, Y, Z

h2m spins...
$800!
h2m passes

---------------

Category: Author & Title
Phrase:   THE GRE_T G_T__Y _Y _. __OTT __TZGER_L_
Guessed:  E, G, H, J, L, N, O, P, Q, R, T, W, X, Y, Z

h3m spins...
One Million!
h3m guesses "D"
There is one D

---------------

Category: Author & Title
Phrase:   THE GRE_T G_T__Y _Y _. __OTT __TZGER_LD
Guessed:  D, E, G, H, J, L, N, O, P, Q, R, T, W, X, Y, Z

h3m spins...
$900!
h3m passes

---------------

Category: Author & Title
Phrase:   THE GRE_T G_T__Y _Y _. __OTT __TZGER_LD
Guessed:  D, E, G, H, J, L, N, O, P, Q, R, T, W, X, Y, Z

Computer 1 spins...
$700!
Computer 1 guesses "M"
There is no M

---------------

Category: Author & Title
Phrase:   THE GRE_T G_T__Y _Y _. __OTT __TZGER_LD
Guessed:  D, E, G, H, J, L, M, N, O, P, Q, R, T, W, X, Y, Z

Computer 2 spins...
$600!
Computer 2 guesses "S"
There are 2 S's

---------------

Category: Author & Title
Phrase:   THE GRE_T G_TS_Y _Y _. S_OTT __TZGER_LD
Guessed:  D, E, G, H, J, L, M, N, O, P, Q, R, S, T, W, X, Y, Z

Computer 2 spins...
$900!
Computer 2 guesses "I"
There is one I

---------------

Category: Author & Title
Phrase:   THE GRE_T G_TS_Y _Y _. S_OTT _ITZGER_LD
Guessed:  D, E, G, H, I, J, L, M, N, O, P, Q, R, S, T, W, X, Y, Z

Computer 2 spins...
$700!
Computer 2 guesses "B"
There are 2 B's

---------------

Category: Author & Title
Phrase:   THE GRE_T G_TSBY BY _. S_OTT _ITZGER_LD
Guessed:  B, D, E, G, H, I, J, L, M, N, O, P, Q, R, S, T, W, X, Y, Z

Computer 2 spins...
$650!
Computer 2 guesses "A"
There are 3 A's

---------------

Category: Author & Title
Phrase:   THE GREAT GATSBY BY _. S_OTT _ITZGERALD
Guessed:  A, B, D, E, G, H, I, J, L, M, N, O, P, Q, R, S, T, W, X, Y, Z

Computer 2 spins...
$600!
Computer 2 guesses "C"
There is one C

---------------

Category: Author & Title
Phrase:   THE GREAT GATSBY BY _. SCOTT _ITZGERALD
Guessed:  A, B, C, D, E, G, H, I, J, L, M, N, O, P, Q, R, S, T, W, X, Y, Z

Computer 2 spins...
$600!
Computer 2 guesses "U"
There is no U

---------------

Category: Author & Title
Phrase:   THE GREAT GATSBY BY _. SCOTT _ITZGERALD
Guessed:  A, B, C, D, E, G, H, I, J, L, M, N, O, P, Q, R, S, T, U, W, X, Y, Z

h1m spins...
Lose a turn!

---------------

Category: Author & Title
Phrase:   THE GREAT GATSBY BY _. SCOTT _ITZGERALD
Guessed:  A, B, C, D, E, G, H, I, J, L, M, N, O, P, Q, R, S, T, U, W, X, Y, Z

h2m spins...
$700!
h2m guesses "F"
There are 2 F's
h2m wins! The phrase was THE GREAT GATSBY BY F. SCOTT FITZGERALD
h2m won $12100
'''