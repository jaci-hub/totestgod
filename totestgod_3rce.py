
'''
Name: Jacinto Jeje Matamba Quimua
Date: 7/26/2026

- To test God - 3 Red Cars Experiment (3RCE)
'''

import os
import subprocess
import time
import random

random.seed(37836) # for reproducibility


global total_three_cars_ob1, total_three_cars_ob2, three_red_cars, not_three_red_cars, BREAK
total_three_cars_ob1 = 0 # substring of three cars seen by observer 1
total_three_cars_ob2 = 0 # substring of three cars seen by observer 2
three_red_cars = 0 # total substrings of three red cars
not_three_red_cars = 0 # total substrings of not three red cars
BREAK = False

transit = [' R ', ' N ', ' G ', ' W ', ' Y '] # All cars on the road, represented by their colors: Red, Navy Blue, Grey, White and Yellow

def clear_screen():
    command = 'cls' if os.name == 'nt' else 'clear'
    subprocess.run(command, shell=True)


def display_grid(grid):
    # print grid
    for i in range(len(grid)):
        row=''
        for j in range(len(grid[i])):
            row+=grid[i][j]
        print(row)
    
    print()
    # observer 1
    percentage_ob1 = 0
    if total_three_cars_ob1 > 0:
        percentage_ob1 = (three_red_cars/total_three_cars_ob1)*100
    print(f'- Total three car groups seen by observer 1: {total_three_cars_ob1}')
    print(f'3 Red cars in a row: {three_red_cars} ({round(percentage_ob1, 2)}%)')
    # observer 2
    percentage_ob2 = 0
    if total_three_cars_ob2 > 0:
        percentage_ob2 = (not_three_red_cars/total_three_cars_ob2)*100
    print(f'- Total three car groups seen by observer 2: {total_three_cars_ob2}')
    print(f'Not 3 Red cars in a row: {not_three_red_cars} ({round(percentage_ob2, 2)}%)')


def update_grid(grid):
    # generate a new random car
    car = random.choice(transit)

    for i in range(8, 0, -1):
        # road observed by observer 2
        if i==6:
            # update car position
            for j in range(len(grid[i])-1): # -1 because the last position is a wall
                if j!=len(grid[i])-2:
                    grid[i][j]=grid[i][j+1]
                else:
                    grid[i][j]=grid[i-1][len(grid[i-1])-2]

        # turning point
        if 3<=i<=5:
            grid[i][len(grid[i])-2]=grid[i-1][len(grid[i-1])-2]

        # road observed by observer 1
        if i==2:
            # update car position
            for j in range(len(grid[i])-2, -1, -1):
                if j!=0:
                    grid[i][j]=grid[i][j-1]
                else:
                    grid[i][j]=car


def observer_counts(grid):
    # observer 1
    if grid[2][0].strip() and grid[2][1].strip() and grid[2][2].strip():
        #   total three car group count
        global total_three_cars_ob1
        total_three_cars_ob1 += 1
        #   total three Red car group count
        if grid[2][0].strip() + grid[2][1].strip() + grid[2][2].strip() == 'RRR':
            global three_red_cars
            three_red_cars += 1

    # observer 2
    if grid[6][3].strip() and grid[6][4].strip() and grid[6][5].strip():
        #   total three car group count
        global total_three_cars_ob2
        total_three_cars_ob2 += 1
        # end the experiment/simulation after the observer 2 has seen a million cars 
        #   - observer 1 would have seen 1 million and 9 cars
        #   Note: we add 2 to the total three car group seen to get the total number of cars seen, because since 
        #         the window the observer fixes on has three slots, and the transit is a queue, then whenever the a car is dequeued two 
        #         of the cars in the window have already been seen, so we only count the new one that was just enqueued. So, the total number 
        #         of three car groups seen, plus two, equals the total number of cars seen.
        if total_three_cars_ob2 + 2 == 1000000: # UPDATE from 1000000 to the number of cars you want the second observer to see!
            global BREAK
            BREAK=True
        #   total Not three Red car group count
        if grid[6][3].strip() + grid[6][4].strip() + grid[6][5].strip() != 'RRR':
            global not_three_red_cars
            not_three_red_cars += 1


def run_exp(grid):
    time.sleep(1) # UPDATE the time here for slower or faster transit!
    clear_screen()
    update_grid(grid)
    observer_counts(grid)
    display_grid(grid)


if __name__=="__main__":
    grid = [
        ['   ','ob1','   ','   ','   ','   '], # observer 1
        ['___','___','___','___','___','___','_'],
        ['   ','   ','   ','   ','   ','   ',' |'],
        ['___','___','___','___','___','   ',' |'],
        ['   ','   ','   ','   ','   ','|','   ','|'],
        ['___','___','___','___','___','|','   ','|'],
        ['   ','   ','   ','   ','   ','   ',' |'],
        ['___','___','___','___','___','___','_|'],
        ['   ','   ','   ','   ','ob2','   '], # observer 2
    ]

    while True:
        run_exp(grid)
        if BREAK:
            break
