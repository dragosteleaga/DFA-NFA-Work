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
        elif len(s) == 5 and "#" not in s and ",#" not in s:
            state.append(s[0])
            state.append(s[2])
            state.append(s[4])
        else:
            state.append(s[0])
    if ok == "Transitions" and s[0] != "Transitions" and s[0] != ":" and s[0] != "#" and s[0] != "End" and s[0][0] != "#" :
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
    elif state[i] == "S" and state[i-1]=="F":
        startPoint = state[i-2]
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

val=[startPoint]
for i in range(0, len(transitions), 3):
    if transitions[i] in val and transitions[i+2] not in val:
        val.append(transitions[i+2])
ok2=0
for i in finishPoints:
    if i in val:
        ok2=1
if ok1 == 1 and ok == 0 and ok2==1:
    ok_ex2 = 1
else:
    print("Not valid!")
# enunt2
if ok_ex2 == 1:
    finalPoints=[]
    matrix = [[-1 for x in range(points)] for j in range(points)]
    for i in range(len(m)): 
        matrix[statesOnly.index(m[i][0])][statesOnly.index(m[i][2])] = m[i][1]
    k=0
    for i in range(len(state)) :
        if state[i]!="S" and state[i]!="F":
            state[i]=k
            k+=1
        if state[i]=="F":
            finalPoints.append(state[i-1])
    
    word=input("word to test ")
    ok_verif = 1
    if word[0] in matrix[0]:
        poz_anterioara = matrix[0].index(word[0])
    else:
        ok_verif = 0
    nr_litera = 0

    for i in range(len(word)-1):
        if word[i+1] in matrix[poz_anterioara]:
            poz_anterioara = matrix[poz_anterioara].index(word[i+1])            
        else:
            ok_verif = 0
            break

    if poz_anterioara not in finalPoints:
        ok_verif = 0

    if ok_verif == 0:
        print("Invalid input !")
    else:
        print("Valid input !")
    
