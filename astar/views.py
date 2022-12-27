from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.

import copy
import random
def shuffle():
  """
  If possible, generate initial condition
  """
  pass
def findIndx(puzzle,num):
    """ Find index of 0 i x j """
    index = puzzle.find(num)
    i = index // 3
    j = index - i * 3
    #print("i = " , i , " j = " ,j)
    return i,j
def possible_dir(puzzle): # DONE!!!
    """
    input = "024163587"
    0 2 4
    1 6 3
    5 8 7
    So, possible move according to user
    = RIGHT, DOWN 
    output = ["RIGHT","DOWN"]
    """
    i,j = findIndx(puzzle,"0") 

    # Find possible direction 0 can move
    map = [(-1,0),(1,0),(0,-1),(0,1)] # UP DOWN LEFT RIGHT respectively [direction according to the 8 puzzle on the website]
    result = []
    dir = {
      (-1,0) : "UP",
      (1,0)  : "DOWN",
      (0,-1) : "LEFT",
      (0,1)  : "RIGHT"
    }

    for k in map:
        if not ((i+k[0] < 0) or (i+k[0] > 2) or (j+k[1] < 0) or (j+k[1] > 2)):
            result.append(dir[k])

    return result 
def gen_state(puzzle, possible_dir):
    """
    input = "024163587", ["RIGHT", "DOWN"]
    0 2 4
    1 6 3
    5 8 7
    output = [["204163587","RIGHT"],["124063587","DOWN"]]
    """
    dir = {
      "UP"    : (-1,0),
      "DOWN"  : (1,0),
      "LEFT"  : (0,-1),
      "RIGHT" : (0,1)
    }

    # get 0 coordinate
    i,j = findIndx(puzzle,"0")

    # get possible dir coordinate
    move_to = []
    for d in possible_dir:
        move_to.append((i+dir[d][0],j+dir[d][1]))
    #print(move_to)

    # generate output
    new_puzzle = []
    for p in move_to:

    # turn string puzzle into list form
        puzzle_list = []
        for a in puzzle:
            puzzle_list.append(a)

    # turn coordinates into index
        blank_indx = i * 3 + j
        dest_indx = p[0] * 3 + p[1]

        # swap position of blank space and possible direction
        puzzle_list[blank_indx],puzzle_list[dest_indx] = puzzle_list[dest_indx],puzzle_list[blank_indx]

        # turn new puzzle into string form
        new_puzzle.append("".join(puzzle_list))

        result = []
        for item in range(len(new_puzzle)):
            result.append([new_puzzle[item],possible_dir[item]])

    # check
    """
    print(new_puzzle)
    for b in range(len(possible_dir)):
    print("\n" + possible_dir[b])
    show_puzzle(new_puzzle[b])
    """
    return result
def h_score(puzzle, goal):

    h_point = 0
    for num in range(len(puzzle)):
        i,j = findIndx(puzzle,str(num))
        x,y = findIndx(goal,str(num))

        h = abs(i-x) + abs(j-y)
        h_point += h

    h2_point = 0
    for n in range(len(puzzle)):
        if puzzle[n] != goal[n]:
            h2_point += 1

    f_point = h_point #+ h2_point 
    return f_point
def show_puzzle(route): # DONE!!!
    """ Print puzzle in more understandable way lol """
    for i in range(len(route)):
        puzzle = route[i][0]
        text = route[i][1]
        g = i
        h = route[i][2]
        f = g + h
        print("Step {}: {}| g = {} h = {} f = {}".format(i,text,g,h,f))
        print(puzzle)
        for k in range(0,9,3):
            print(puzzle[k] + " " + puzzle[k+1] + " " + puzzle[k+2])

        print("")
    
def solve(puzzle,goal):
    """ Main progress """

    path = []
    result = []
    check = {puzzle:1}
    gen = 0
    dept = 0

    path.append([[puzzle]])
    #print(path)

    while path:

        # show generation
        if gen % 1000 == 0:
            print("Gen: ", gen)
        gen += 1

        # choose route and declare puzzle to work on
        current_route = path.pop(0)
        current_puzzle = current_route[-1][0]

        # check if win
        if current_puzzle == goal:
            route = current_route
            return route

        # declare g score
        g = len(current_route)

        # if the current_puzzle already visited once with different step then abandon this route
        # it will remove the route with that visite the same puzzle but take more move
        if check[current_puzzle] != g:
            continue 

        # generate possible move of blank space or "0" in this case
        next_state = gen_state(current_puzzle,possible_dir(current_puzzle))

        # consider if the next state should be add to the route or not
        for state in next_state:
          # declare puzzle and g score of the state
            state_puzzle = state[0]
            state_g = g + 1

          # check if this puzzle have been visited before
            if state_puzzle in check:

            # if visited before but g score is less than the recent then
            # change the visted puzzle to the lesser one
                if  state_g < check[state_puzzle]:
                    check[state_puzzle] = state_g
                    to_add_state = copy.deepcopy(current_route)
                    print(state)
                    state.append(h_score(state_puzzle,goal))
                    to_add_state.append(state)
                    path.append(to_add_state)

            # if visited before but g score is higher then do nothing

          # if never visited before then add the data to dictionary "check" and add to path
            else:
                check[state_puzzle] = state_g
                to_add_state = copy.deepcopy(current_route)
                state.append(h_score(state_puzzle,goal))
                to_add_state.append(state)
                path.append(to_add_state)

        # sort route according to the step (lengt of the route list) and h score respectively
        path = sorted(path, key= lambda x: (len(x), x[-1][-1]))



@csrf_exempt
def say_hello(request):
    if(request.method =="OPTIONS"):
        return JsonResponse({"true":'123'})
    k=json.loads(request.body.decode('utf-8'))
    print(k['end'])
    solution = solve(k['start'],k['end'])
    sol = []
    for i in solution:
        sol.append([i for i in i[0]])
        print(i)
    return JsonResponse({"solution":sol})