#IMPORT
import random
import requests as rq
from urllib.request import urlopen
import re
from time import sleep as wait
from unidecode import unidecode
from termcolor import colored

#FUNCTIONS
def choose_word():
    '''Picks random word for website drawing words. Then sets lists for both words and user answer'''
    url = "http://debonogenerator.cba.pl/"
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")

    pattern = "<p.*?>.*?</p.*?>"
    match_results = re.search(pattern, html, re.IGNORECASE)
    word = match_results.group()
    word = re.sub("<.*?>", "", word) # Remove HTML tags
    spaces=len(word)
    if spaces<=5:
        chances=10
    else:
        chances=spaces*2
    answer=[]
    for i in word:
        answer.append("_")
    print(f"Na podstawie zaawansowanych kalkulacji, stwierdzam, że przy tej długości słowa powinieneś odgadnąć moje słowo w {chances} próbach")
    print(colored("_ ","yellow")*spaces)
    return word, answer, chances


def look_for_letter(word,answer,letter,chances):
    '''Iterate throught word to see if user guessed correctly. If so, user answer is updated with new letter'''
    letter=letter.upper()
    place= ([pos for pos, char in enumerate(word) if char == letter])
    for i in place:
        answer[i]=letter
    if letter not in word:
        chances-=1
    return answer,chances

def draw_board(answer):
    '''Draws gameboard in the terminal. "_" for unknow letters and normal letters for ones that user guessed'''
    string=""
    for i in answer:
        string+=i+" "
    print (colored(string,"yellow"))
    print(" ")

#CODE
print (colored("Witaj w grze w wisielca. Gotów na nowe literkowe wyzwania?", "magenta"))
while True:
    decision=input("Zaczynamy? (y/n):")
    print(" ")
    if decision == "y":
        word, answer, chances=(choose_word())
        letters=""
        while True:
            letter=input("Twoja litera: ")
            letters+=letter+" "
            print (f"Wykorzystane litery: {letters}\nPozostałę próby: {chances}")
            answer,chances=look_for_letter(word,answer,letter,chances)
            draw_board(answer)
            if "_" not in answer:
                print (colored("Gratulacje, odgadłeś moje słowo!\n\n", "green"))
                break
            if chances==0:
                print (colored("Przegrałeś, moja potęga Cię zwyciężyła!\n\n", "red"))
                print (word)
                break
    elif decision == "n":
        print("Trudno, widzimy się następnym razem!")
        wait(2)
        #break
    else:
        print ("A co to? Wprowadź poprawne dane")
