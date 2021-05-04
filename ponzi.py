"""
PONZI. A pyramid scheme you can trust

YOU HAVE UNLIMTED TRIES
THE 4 DIGITS IN THE NUMBER DONT REPEAT
THERE IS NO LEADING ZERO
YOUR GUESS CANNOT HAVE REPEATING NUMBERS
THE FASTER YOU ARE DONE THE BEST
THE RETURNS ARE ALLOCATED ACCORDING TO YOU ABILITY TO SCAPE THE PYRAMID FROM THE TOP

KILLED MEANS THE NUMBER IS PRESENT AND IT IS LOCATED IN THE RIGHT POSITION
INJURED MEANS THE NUMBER IS PRESENT BUT NOT IN THE RIGHT POSITION
"""
import time
from random import sample, shuffle
import json

data = {}
digits = 3
guesses = 10
player="name"




#check if input repeats digits function to warn player
def has_doubles(n):
    return len(set(str(n))) < len(str(n))
#counting killed-injured function
def countX(lst, x):
    count = 0
    for ele in lst:
        if (ele == x):
            count = count + 1
    return count

# Create a random number with no leading 0 no repeated digit.

letters = sample('0123456789', digits)

if letters[0] == '0':
    letters.reverse()

number = ''.join(letters)

counter = 1


while True:
    
    print('Guess #', counter)
    guess = input()
    
    if counter == 2:
        start_time = time.time()

    if len(guess) != digits:
        print('Wrong number of digits. Try again!')
        continue
    if has_doubles(guess) is True:
        print('You cannot repeat digits. Try again!')
        continue

    # Create the clues.
    
    clues = []

    for index in range(digits):
        if guess[index] == number[index]:
            clues.append('Killed')
        elif guess[index] in number:
            clues.append('Wounded')


    if len(clues) == 0:
        print('Nothing')
    else:
        print('There are {} {}'.format(countX(clues, "Killed"), "Killed"))
        print('There are {} {}'.format(countX(clues, "Wounded"), "Wounded"))


    counter += 1
    

    if guess == number:
        print('You got it!')
        end_time = time.time()
        data['start_time']= start_time
        data['end_time']= end_time
        data['total_time']= end_time - start_time
        data['status']= "solved"
        json_data = json.dumps(data)
        print("You took: ", end_time - start_time)
        break

    if counter > guesses:
        print('You ran out of guesses. The answer was', number)
        end_time = time.time()
        print("You took: ", int(end_time - start_time), "seconds")
        break