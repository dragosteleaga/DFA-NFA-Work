from asyncio.windows_events import NULL
from http.client import CONTINUE
import re
from sys import dllhandle


transitions = []
sigma = []
state = []
f = open("dfa_config_file")
s = f.readline().split()
while(len(s)):
    if "#" in s[0]:
        s = f.readline().split()
    if s[0] == "Sigma":
        ok = "Sigma"
    if s[0] == "Transitions":
        ok = "Transitions"
    if s[0] == "State":
        ok = "State"
    if ok == "Sigma" and s[0] != "Sigma" and s[0] != ":" and s[0] != "#" and s[0] != "End":
        sigma.append(s[0])
    if ok == "State" and s[0] != "State" and s[0] != ":" and s[0] != "#" and s[0] != "End" and s[0][0] != "#":
        if len(s) == 3 and "#" not in s and ",#" not in s:
            state.append(s[0])
            state.append(s[2])
        else:
            state.append(s[0])
    if ok == "Transitions" and s[0] != "Transitions" and s[0] != ":" and s[0] != "#" and s[0] != "End" and s[0][0] != "#":
        transitions.append(s[0])
        transitions.append(s[2])
        transitions.append(s[4])
    s = f.readline().split()


def validareMinima(finish_points, start_points, ok, points):
    finish_points = 0
    start_points = 0
    points = 0
    ok = 0
    for i in state:
        if i == "F":
            finish_points += 1
        elif i == "S":
            start_points += 1
        else:
            points += 1
    if(start_points > 1):
        ok = 1
    for i in transitions:
        if i not in sigma and i not in state:
            ok = 1
    return finish_points, start_points, ok, points


finish_points = 0
start_points = 0
ok = 0
points = 0
finish_points, start_points, ok, points = validareMinima(
    finish_points, start_points, ok, points)
# liste cu start point si finish points
finishPoints = []
statesOnly = []
for i in range(len(state)):
    if state[i] == "F":
        finishPoints.append(state[i-1])
    elif state[i] == "S":
        startPoint = state[i-1]
    else:
        statesOnly.append(state[i])
# matrice ajutatoare pentru parcurgere
m = []
for i in range(0, len(transitions), 3):
    m.append([transitions[i], transitions[i+1], transitions[i+2]])
# lista cu elemente pentru verificarea finala
goodPoints = [startPoint]
for i in m:
    if i[0] == startPoint or i[0] in goodPoints:
        goodPoints.append(i[2])
ok1 = 0
for i in finishPoints:
    if i in goodPoints:
        ok1 = 1
ok_ex2 = 0
if ok1 == 1 and ok == 0:
    ok_ex2 = 1
# else:
 #   print("Not valid !")
# if    ok_ex2 == 1:
  #  print("Valid !")
statesOnlyIndex = []
# jumate de matrice
for i in range(len(statesOnly)):
    statesOnlyIndex.append(i)
matrix = [[0 for i in range(j)]for j in range(1, len(statesOnly))]
for i in range(len(m)):
    m[i][0] = statesOnly.index(m[i][0])
    m[i][2] = statesOnly.index(m[i][2])

# primul pas in hasurarea matricei
for i in range(len(matrix)):
    for j in range(len(matrix[i])):
        if (statesOnly[i+1] in finishPoints and statesOnly[j] not in finishPoints) or (statesOnly[i+1] not in finishPoints and statesOnly[j] in finishPoints):
            matrix[i][j] = 1

ok = 1
# completez matricea pana nu se mai poate
while ok == 1:
    ok = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 0:
                for litera in sigma:
                    for k in m:
                        if(k[1] == litera and k[0] == i+1):
                            newState1 = k[2]
                        if(k[1] == litera and k[0] == j):
                            newState2 = k[2]
                    if(newState1 < newState2):
                        newState1, newState2 = newState2, newState1
                    if(newState1 == newState2):
                        continue
                    if(matrix[newState1-1][newState2]):
                        matrix[i][j] = 1
                        ok = 1
# afisare
asd = []
k = 0
for i in range(len(matrix)):
    for j in range(len(matrix[i])):
        if matrix[i][j] == 0:
            if not len(asd):
                asd.append([statesOnly[j], statesOnly[i+1]])
            else:
                if(statesOnly[j] in asd[k]):
                    if statesOnly[i+1] in asd[k]:
                        continue
                    asd[k] = asd[k]+[statesOnly[i+1]]
                else:
                    asd.append([statesOnly[j], statesOnly[i+1]])
                    k += 1
d = {}
for i in asd:
    d[i[0]] = i
ls = []
stateShow = []
for i in d.values():
    for j in i:
        ls.append(j)
for i in state:
    if i in d:
        stateShow.append(d[i])
    elif i in ls:
        continue
    else:
        stateShow.append(i)
transitionsShow=[]
print(ls)
for i in range(0,len(transitions),3):
    for j in d:
        if transitions[i] in d[j] and transitions[i+2] in d[j]:
            continue
        elif transitions[i] in d[j] and transitions[i+2] not in d[j]:
            transitionsShow.append(transitions[i])
            transitionsShow.append(transitions[i+1])
            transitionsShow.append(transitions[i+2])
    if transitions[i] not in ls and transitions[i+2] not in ls:
        transitionsShow.append(transitions[i])
        transitionsShow.append(transitions[i+1])
        transitionsShow.append(transitions[i+2])
print(transitionsShow)
tra1Show=[]
for i in transitionsShow:
    if i in d:
        tra1Show.append(d[i])
    elif i not in ls:
        tra1Show.append(i)
    else:
        for t in range(ls.index(i),-1,-1):
            if ls[t] in d:
                tra1Show.append(d[ls[t]])
                break
print(tra1Show)
print("Sigma : ")
for i in sigma:
    print(i)
print("End")
print("State : ")
for i in range(len(stateShow)):
    if i != len(stateShow)-1 and stateShow[i+1] == "S":
        print(*stateShow[i], " , S")
    elif  stateShow[i] == "F":
        continue
    elif stateShow[i] == "S":
        continue
    elif i != len(stateShow)-1 and stateShow[i+1] == "F":
        if(len(stateShow[i]) > 1):
            print(*stateShow[i], " , F")
    else:
        print(stateShow[i])
print("End")
print("Transitions : ")
for i in range(0, len(tra1Show), 3):
    print(tra1Show[i]," , ", tra1Show[i+1]," , ", tra1Show[i+2])  
print("End")