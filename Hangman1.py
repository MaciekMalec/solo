import datetime
import time
import random
from os import system, name
from operator import itemgetter


def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')



def get_word_list(file_name):
    worda=[]
    with open(file_name,"r") as words:
        for line in words:
            worda.append(words.readline().upper().strip().split(" | "))
    del worda[-1]
    return worda

def get_score_table(file_name):
    with open(file_name, 'r') as high_scores:
        sort_scores=[]
        full_table=[]
        for el in high_scores:
            elt=el.split(" | ")
            full_table.append(elt)
            # print(elt)
            points=int(''.join(filter(str.isdigit, elt[2])))
            # print(int(points))
            highscore = {
                "name": elt[0],
                "score": int(1000*len(elt[3])*(.95**int(points)))
            }
            sort_scores.append(highscore)
        sort_scores.sort(key=itemgetter("score"),reverse=True)
        return sort_scores, full_table

def high_score_table(sort_scores):
    long_name=max([len(el['name'])] for el in sort_scores)
    for i in range(1, min([len(sort_scores),10])):
        spaces=(long_name[0]-len(sort_scores[i]['name']))
        print(i, " - ", sort_scores[i]['name'], " "*spaces,  " reached the score: ", sort_scores[i]['score'])

def hangman(password, hint, chances):
    clear()
    passup=password.upper()
    passlist=("_ "*len(password)).split(" ")[:-1]
    answer = ' '
    for letter, el in enumerate(passup):
        if answer==el:
            passlist[letter]=answer
    print(' '.join(passlist), " - chances remaining: ", chances)
    bad_letters=[]
    while answer !='0' and passlist!=list(passup):
        answer=input("Guess a character or try password or [0] to quit: ")
        clear()
        if len(answer)==1 and answer !='0':
            answer=answer.upper()
            if answer in passup and answer not in passlist:
                for letter, el in enumerate(passup):
                    if answer==el:
                        passlist[letter]=answer
            elif chances>0:
                bad_letters.append(answer)
                chances-=1
        elif len(answer)>1:
            trial=answer.upper()
            if trial==passup:
                passlist=list(passup)
            else:
                print('Wrong answer. You lose 2 chances as a penalty!')
                chances-=2
        print(' '.join(passlist), " - chances remaining: ", chances)
        if chances==1:
            print('Hint: ',hint)
        if chances<1:
            answer='0'
        print('Wrong letters: ',bad_letters)
    print('Game over.')
    if passlist==list(passup):
        print('You have guessed correctly the password: ',password)
        return chances
    else:
        print('TOO BAD.\nThe password was very easy:\n ',password,'\nBetter Luck next time!')
        return False

def main():
    sort_scores=[]
    word_list="capitals.txt"
    score_list="scores.txt"
    chances=5
    print('This game was created by Maciek.\n List of things:')
    # print(worda) - debug to see if list of cities is imported correctly
    time.sleep(1)
    x=input('Try Hangman for yourself or press enter to continue: ')
    if x:
        start_time=time.time()
        y=hangman(x,'It\'s the word you have just typed',5)
        elapsed_time=time.time()-start_time
        if y:
            f = int(1000*len(x)*(.95**(elapsed_time)))
            high_scores = {
                "name": 'Maciek',
                "score": f
            }
            print(high_scores)
            print("It took you :", int(elapsed_time), " seconds.")
            time.sleep(2)
    ans=1
    while ans!='x':
        x=15
        print('\n'," "*(x+2),'---===<<<Hangman game>>>===---\n')
        print(" "*x,'The word list is from: ',word_list)
        print(" "*x,'The scores are saved in: ', score_list)
        print(" "*x,'The game is set to have: ', chances,' chances.')
        print('\n'," "*(x+5),'[e] to see the word list\n'," "*(x+5),'[h] to see the high scores')
        print(" "*(x+5),' [f] to modify file names \n'," "*(x+5),'any other answer to start a game')
        print(" "*(x+5),' [x] to quit.')
        ans=input('                      What do You want to do? ')
        if ans=='x':
            break
        elif ans=='e':
            worda=get_word_list(word_list)
            for el in worda:
                print(el[1], 'that is the capital of ', el[0])
        elif ans=='h':
            if not sort_scores:
                sort_scores=get_score_table(score_list)[1]
                for el in sort_scores:
                    print(' | '.join(el))
            print('Points depend on how long the word is, and how much time it took to guess it correctly.')
        elif ans=='f':
            clear()
            print('Current word list file is: \'',word_list,'\'')
            a=input('Type the name of the .txt file with words and hints :')
            if a:
                try: 
                    x=get_word_list(a)
                    print('New list loaded with ', len(x), ' words and hints')
                    word_list=a
                except:
                    print('wrong file name')
            print('Current score list file is:\'',score_list,'\'')
            a=input('Type the name of the .txt file with scores: ')                
            if a:
                try:
                    x=get_score_table(a)[1]
                    print('New score list loaded with ',len(x),' scores.')
                    score_list=a
                except:
                    print('wrong file name')
        else:
            wordb=random.choice(get_word_list("capitals.txt"))
            stime=time.time()
            hint=' '.join([' It is the capital of',wordb[0]])
            y=hangman(wordb[1],hint,chances)
            elapsed_time=time.time()-stime
            points=int(1000*len(wordb[1])*(.95**int(elapsed_time)))
            if y:
                print("It took you :", int(elapsed_time), " seconds. Your score is: ", points,", while losing only " ,5-y," chances")
                scores = {
                    "name": input("Type your name: "),
                    "date": datetime.datetime.now(),
                    "time": int(elapsed_time),
                    "word": wordb[1]
                } 
                if scores["name"]:
                    
                    with open("scores.txt", "a") as score_file:
                        score_file.write(f"{scores['name']} | {scores['date']} | {scores['time']} second(s) | {scores['word']}\n")
                sort_scores,full_score=get_score_table(score_list)
                high_score_table(sort_scores)
            else:
                a=input("Oh, is the game too hard for You? \nMaybe You need more chances? \nHow many would You like to have now? ")
                if a:
                    if int(a)>3 and int(a)<12:
                        chances=int(a)
                        print('Now You will have ',chances,' chances. \nHave Fun!')
                    else:
                        if chances>3:
                            chances-=1
                        else:
                            chances=6
                    print('No can do, baby!\nI decided to let You have ', chances,' chances.\nHave Fun!')

        time.sleep(2)       
    print('Hall of fame:')
    if sort_scores:
        high_score_table(sort_scores)
    time.sleep(3)
clear()
main()
