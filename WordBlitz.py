'''
Written by:Elifnaz Gulsen
This program simulates a Word Blitz game where two players are given a
clue and try to guess a secret word, whoever has the most money at the end
of the game when the secretWord is revealed wins the game
'''
import sys
import random

'''
This function loads the set of puzzles into the program.
'''
def loadPuzzles(filename='wordblitzclues.txt'):
    fileClues = open(filename,'r')
    lisClues = []
    for line in fileClues:
        lisClues.append(line.rstrip()) #rstrip strips all chars from the end of the string.
    fileClues.close()
    return lisClues

'''
This function loads a random puzzle from the list of puzzles.
Removes any extra tabs that may be in the imported clue or word.
'''
def getRandomPuzzle(puzzleLis):
    randomIndex = random.randint(0,len(puzzleLis)-1)
    puzzle = puzzleLis[randomIndex].split('\t')
    for extraTab in puzzle:
        if extraTab == '':
            puzzle.remove('')
    puzzleClue = puzzle[0]
    secretWord = puzzle[1]
    return puzzleClue,secretWord


'''
asks and returns player's names
'''
def askNames():
    global player1
    global player2
    player1 = input("Player 1 name: ")
    player2 = input("Player 2 name: ")

    return player1,player2

'''
Identifies the winner by comparing total scores at the end of the game
or when user decides to quit the game without the secretWord being revealed
'''
def identifyWinner(player1total,player2total):
    if player1total > player2total:
        print("Player 1 wins with a total of:",player1total,"!")
        print("Player 2 is in second with:",player2total)
    elif player2total > player1total:
        print("Player 2 wins with a total of:",player2total,"!")
        print("Player 1 is in second with:",player1total)
    else:
        print("player 1 and player 2 are tied with:",player1total,"points")

'''
Menu choice 1: Spin the wheel
'''
def spinWheel(player,playerTurn):
    global player1Turn
    global player1Total
    global player2Turn
    global player2Total
    spin = random.randint(0,21)
    if spin == 0: #bankrupcy element
        print("Sorry, you get a bankruptcy element.")
        turnMoney = 0
        if player == 1:
            player1Turn = 0
            player1Total += player1Turn
            playerTurn = updateTurns(1)
            return playerTurn
        else:
            player2Turn = 0
            player2Total += player2Turn
            playerTurn = updateTurns(2)
            return playerTurn
            
    elif spin == 21:#lose-a-turn element
        print("You spun:",spin)
        print("Sorry, you lose a turn")
        if player == 1:
            player1Total += player1Turn
            player1Turn = 0
            playerTurn = updateTurns(1)
            return playerTurn
        else:
            player2Total += player2Turn
            player2Turn = 0
            playerTurn = updateTurns(2)
            return playerTurn

    else: #spin between 1 and 20 inclusive
        print("You spun:",spin)
        condition = True
        while (condition):
            chooseConsonant = input("Enter a consonant: ")
            if len(chooseConsonant) == 1 and chooseConsonant in["b","c","d","f","g","h","j","k","l","m","n","p",
                         "q","r","s","t","v","w","x","y","z","B","C","D",
                         "F","G","H","J","K","L","M","N","P","Q","R","S",
                         "T","V","W","X","Y","Z"]:
                condition = False
            #if user enters more than one consonant
            elif len(chooseConsonant) > 1:
                print("Please only enter 1 consonant")
                condition = True

            else:
                print("Please enter a consonant")
                condition = True

        #checks if consonant is in secretWord
        if chooseConsonant.upper() in secretWord.upper():
            #gives the indice(s) the consonant(s) is/are  in
            correctIdx = checkWord(chooseConsonant.upper(),secretWord.upper())
            for idx in correctIdx:
                #append correct indices to our list to display later
                visibleIndexes.append(idx)
            guessedLetters.append(chooseConsonant)
            turnMoney = 0
            turnMoney += (spin * len(correctIdx))
            print("You found",len(correctIdx),chooseConsonant,"'s")
            print("")
            if player == 1:
                player1Turn += turnMoney
                playerTurn = updateTurns(2)
                return playerTurn
            else:
                player2Turn += turnMoney
                playerTurn = updateTurns(1)
                return playerTurn
            
   
        else:
            print("Sorry, the consonant is not in the word, you lose",spin,"dollars")
            guessedLetters.append(chooseConsonant)
            turnMoney2 = 0
            turnMoney2 -= spin
            if player == 1:
                player1Turn += turnMoney2
                player1Total += player1Turn
                #set turn money equal to zero again
                player1Turn = 0
                playerTurn = updateTurns(1)
                return playerTurn
            else:
                player2Turn += turnMoney2
                player2Total += player2Turn
                #set turn money equal to zero again
                player2Turn = 0
                playerTurn = updateTurns(2)
                return playerTurn

'''
menu option 2, buying a vowel
checks if user enters a vowel, checks if vowel is in the secret word
updates secret word with vowel in it
'''
def buyVowel(player,playerTurn):
    global player1Total
    global player1Turn
    global player2Total
    global player2Turn
    
    deduction = -25
    if player == 1:
        player1Turn += deduction
        player1Total += player1Turn
        player1Turn = 0
        print("You have bought a vowel. 25 dollars has been subtracted from your total")
    else:
        player2Turn += deduction
        player2Total += player2Turn
        player2Turn = 0

    #checking whether user enters a vowel
    condit = False
    while (condit) == False:
        vowelGuess = input("Enter a vowel: ")
        if len(vowelGuess) == 1 and vowelGuess in ["a","e","i","o","u",
                                                 "A","E","I","O","U"]:
            condit = True

        elif len(vowelGuess) > 1:
            print("Please only enter 1 vowel")
            condit = False
        else:
            print("Please enter a vowel")
            condit = False

    if vowelGuess.upper() in secretWord.upper():
            #gives the indice(s) the consonant(s) is/are  in
            correctIdx = checkWord(vowelGuess.upper(),secretWord.upper())
            for idx in correctIdx:
                visibleIndexes.append(idx)
            guessedLetters.append(vowelGuess)
            if player == 1:
                player1Total += player1Turn
                player1Turn = 0
                playerTurn = updateTurns(2)
                return playerTurn
            else:
                player1Total += player1Turn
                player1Turn = 0
                playerTurn = updateTurns(1)
                return playerTurn

    else:
            print("Sorry, the vowel is not in the word")
            guessedLetters.append(vowelGuess)
            if player == 1:
                playerTurn = updateTurns(1)
                return playerTurn
            else:
                playerTurn = updateTurns(2)
                return playerTurn
 
'''
menu option 3: user guesses the word
if the word is correct, user gets 5 dollars for each word that was not
revealed in the secretWord, then the totals are calculated, and the winner
is revealed. 
'''
def wordGuess(player,playerTurn):
    global player1Total
    global player2Total
    global player1Turn
    global player2Turn
    userGuess = input("Enter a guess: ")
    if userGuess.upper() == secretWord.upper():
        print("You got it, the secret word was:",secretWord.upper())
        disp = displayWord(secretWord,visibleIndexes)
        dispList = list(disp)
        countIds = dispList.count('_')
        if player == 1:
            player1Total += countIds * 5
            winner2 = identifyWinner(player1Total,player2Total)
            print("Thanks for playing")
            sys.exit()
        else:
            player2Total += countIds * 5
            winner3 = identifyWinner(player1Total,player2Total)
            print("Thanks for playing")
            sys.exit()
    else:
        print("Sorry, Incorrect guess.")
        if player == 1:
           playerTurn = updateTurns(1)
           return playerTurn
        else:
           playerTurn = updateTurns(2)
           return playerTurn

'''
checks user guess when they buy vowel or spin wheel and get a consonant
returns the indice(s) that the letter is in.
'''
def checkWord(word,secret_word):
    indicesIn = [i for i, letter in enumerate(secret_word) if (word) == letter]
    return indicesIn

# found + modified the above code for checkWord from:
#____________________________________________________
#Title: Hangman
#Author: Neil Chowdhury
#Date: 2016
#URL: https://repl.it/@primesandfract/Hangman
#____________________________________________________



'''
displays the secretWord
'''
def displayWord(wordIn,blanks):
    global dispWord
    dispWord = ""
    for i in range(len(wordIn)):
        if i in blanks:
            dispWord += wordIn[i] + " "
        else:
            dispWord += "_ "
    return dispWord

# found + modified the above code for display word from:
#________________________________________________
#Title: Hangman
#Author: Neil Chowdhury
#Date: 2016
#URL: https://repl.it/@primesandfract/Hangman
#________________________________________________



'''
tracks turns of the players
'''
def updateTurns(turn):
    if turn == 1:
        nextTurn = 2 
        return nextTurn
    else: #turn == 2:
        nextTurn = 1 
        return nextTurn
    
    
'''
displays current turn and overall game balances
'''
def moneyBalance():
    print(player1,"'s turn balance:",player1Turn)
    print(player1,"'s total balance:",player1Total)
    print("")
    print(player2,"'s turn balance:",player2Turn)
    print(player2,"'s total balance:",player2Total)
    
    
'''
main function that begins program execution
'''
def main():
    global secretWord
    puzzle = loadPuzzles()
    puzzleClue,secretWord = getRandomPuzzle(puzzle)
    print("Welcome to WordBlitz!")
    print("")
    askName = askNames()
    print("")
    
    global player1Total
    global player1Turn
    global player2Total
    global player2Turn
    
    player1Total = 0
    player1Turn = 0
    player2Total = 0
    player2Turn = 0
    global guessedLetters
    guessedLetters = []
    global visibleIndexes
    visibleIndexes = []

    #begin with player 1 
    turn = 1
    nextTurn = 2 
    init = True
    while init:
        if turn == 1:
            print("It's",player1,"'s turn")
            print("")
            print("Clue is:",str(puzzleClue))
            
            moneyDisp = moneyBalance()
            disp = displayWord(secretWord,visibleIndexes)
            
            print("Secret word:",disp)
            print("Guessed Letters:",guessedLetters)
            
            userIn = int(input("""would you like to:
                      1) Spin the Wheel?
                      2) Buy a vowel?
                      3) Guess the word?
                      4) Quit the game?

                      Choice: """))
            
            if userIn == 1 :
                userSpin = spinWheel(1,player1Turn)
                nextTurn = userSpin
                if nextTurn == 2:
                    turn = 2
                else:
                    turn = 1 
            elif userIn == 2:
                vowel = buyVowel(1,player1Turn)
                nextTurn = vowel
                if nextTurn == 2:
                    turn = 2
                else:
                    turn = 1
            elif userIn == 3:
                guess1 = wordGuess(1,player1Turn)
                nextTurn = guess1
                if nextTurn == 2:
                    turn = 2
                else:
                    turn = 1
            else:
                winner1 = identifyWinner(player1Total,player2Total)
                print("Thank you for playing")
                sys.exit()
        if turn == 2:
            #player 2's turn
            print("It's",player2,"'s turn")
            print("Clue is:",str(puzzleClue))
            
            moneyDisp = moneyBalance()
            disp = displayWord(secretWord,visibleIndexes)
            
            print("Secret word:",disp)
            print("Guessed Letters:",guessedLetters)
            
            userIn = int(input("""would you like to:
                      1) Spin the Wheel?
                      2) Buy a vowel?
                      3) Guess the word?
                      4) Quit the game?

                      Choice: """))
            
            if userIn == 1:
                userSpin2 = spinWheel(2,player2Turn)
                nextTurn = userSpin2
                if nextTurn == 1 :
                    turn = 1
                else:
                    turn = 2
            elif userIn == 2:
                vowel2 = buyVowel(2,player2Turn)
                nextTurn = vowel2
                if nextTurn == 1:
                    turn = 1
                else:
                    turn = 2 
            elif userIn == 3:
                guess = wordGuess(2,player2Turn)
                nextTurn = guess
                if nextTurn == 1:
                    turn = 1
                else:
                    turn = 2
            else:
                winner2 = identifyWinner(player1Total,player2Total)
                print("Thank you for playing")
                sys.exit()



main()
