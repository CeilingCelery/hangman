import time
import random


def setup():
    global gameactive
    global keyword
    global guesses
    global guessedletterst
    global guessedlettersf
    global letterindex
    global keywordset
    global revealer
    #Generate our word the player needs to guess
    wordfile = list(open("words_alpha.txt","r"))
    keyword = ""
    i=0
    while keyword == "":
        while len(keyword)<5 or len(keyword)>10:
            try:            
                keyword = random.choice(wordfile).strip()
                time.sleep(1)
            except IndexError:
                if i < 1:
                    time.sleep(1)
                    keyword = random.choice(wordfile).strip()
                else:
                    keyword = "joystick"
    print(keyword)
    #Set the number of wrong guesses allowed, increase to make the game easier
    guesses = 6
    gameactive = True
    guessedletterst = set()
    guessedlettersf = set()
    letterindex = []
    keywordset = set(keyword)
    revealer = wordstate()

def playagain():
    global gameactive
    global keyword
    global guesses
    global guessedletterst
    global guessedlettersf
    global letterindex
    global keywordset

    print('The word was:',keyword)
    time.sleep(2)
    playagain = str(input('Would you like to play again? (y/n)\n')).lower()
    if playagain[0]=='y':
        setup()
        print('Have fun!\n')
        time.sleep(2)
    else:
        gameactive=False
        print('Goodbye')
        time.sleep(2)

def checkguess():
    global validguess
    if playerguess.isalpha()==True and len(playerguess)==1:
        validguess=True
    else:
        print('Please only enter one letter of the alphabet for your guess\n')
        time.sleep(3)
        validguess=False

def wordstate():
    #Returns the currently guessed correct letters formatted in a readable way for the player
    revealer = ""
    for l in range(len(keyword)):
        if keyword[l] in guessedletterst:
            revealer += keyword[l]
        else:
            revealer += "-"
    return revealer

setup()

print('Welcome to Hangman!\nHave fun playing!\n')
time.sleep(2)
print('The word you are guessing is',len(keyword),'letters long')

while gameactive == True:
    print('--------------------------------------------------------')
    playerguess=str(input('What letter would you like to guess?\n')).lower()
    checkguess()
    while validguess==False:
        playerguess=str(input('What letter would you like to guess?\n')).lower()
        checkguess()
    time.sleep(1)

    if (playerguess in keyword)==True:
        print('\nYou have guessed a correct letter!\n')
        time.sleep(2)
        print('The letter',playerguess.upper(),'occurs',keyword.count(playerguess),'times in the word')

        i=0
        while i<len(keyword):
            if keyword.find(playerguess,i,len(keyword))>=0: #Figuring if the guessed letter appears in the remainder of the word on this loop
                letterindex.append(keyword.find(playerguess,i,len(keyword))+1) #Add where in the word the letter appears totell the player
                i=letterindex[letterindex.index(max(letterindex))] #Update i so we can continue from this part of the word in the next find loop
            else:
                i=len(keyword)
        charindex = ''
        for l in range(len(letterindex)):
            if l == 0:
                charindex += str(letterindex[l])
            else:
                charindex += (' and '+str(letterindex[l]))
        print('The letter',playerguess.upper(),'is the',charindex,'character(s) in the word')
        letterindex = []

        print('You still have',guesses,'incorrect guesses remaining\n')
        guessedletterst.add(playerguess)
        print('You have guessed the following correct letters:',guessedletterst)
        print('You have guessed the following incorrect letters:',guessedlettersf,'\n')

        revealer = wordstate()

        print('The word board currently looks like:', revealer,'\n\n')

        if guessedletterst==keywordset:
            print('YOU WIN')
            playagain()



    else:
        guesses-=1
        print('\nYour guessed letter is not contained in the word')
        time.sleep(2)
        print('You have',guesses,'incorrect guesses remaining\n')
        guessedlettersf.add(playerguess)
        print('You have guessed the following correct letters:',guessedletterst)
        print('You have guessed the following incorrect letters:',guessedlettersf,'\n')

        revealer = wordstate()

        print('The word board currently looks like:', revealer,'\n\n')

        if guesses<1:
            print('You have run out of guesses\nGAME OVER\n')
            playagain()