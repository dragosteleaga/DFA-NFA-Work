transitions = []
sigma = []
state = []
ok = 0
f = open("nfa_config_file")
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
    if ok == "Transitions" and s[0] != "Transitions" and s[0] != ":" and s[0] != "#" and s[0] != "End" and s[0][0] != "#":
        transitions.append(s[0])
        transitions.append(s[2])
        transitions.append(s[4])
    s = f.readline().split()
verificare = 1
sigma.append("*")
# Verificam elem din tranzitie
for i in range(0, len(transitions), 3):
    if (transitions[i] or transitions[i+2]) not in state or transitions[i+1] not in sigma:
        verificare = 0

# Verificam elementele din state
k = 0
k1 = 0
points = 0
statesOnly = []
startPoint = []
finishPoints = []
for i in range(len(state)):
    
    if state[i] == "S" and state[i-1]=="F":
        startPoint = state[i-2]
        k+=1
    elif state[i]=="S" : #sa fie doar o stare de start
        startPoint.append(state[i-1])
        k+=1
    elif state[i]=="F":
        k1+=1
        finishPoints.append(state[i-1])
    else :
        points+=1
        statesOnly.append(state[i])
    if state[i]!="S" and state[i]!="F" and state[i] not in transitions: #sa nu fie elem redundante in sigma
        verificare=0
if k != 1:  # nu e doar un start
    verificare = 0
if k1 == 0:  # nu e nici un finish
    verificare = 0
# Verificam sigma
for i in sigma:
    if i not in transitions and i !="*":
        verificare = 0
m = []
for i in range(0, len(transitions), 3):
    m.append([transitions[i], transitions[i+1], transitions[i+2]])
matrix = [[[-1] for x in range(points)] for j in range(points)]
val=[startPoint]
for i in range(0, len(transitions), 3):
    if transitions[i] in val and transitions[i+2] not in val:
        val.append(transitions[i+2])
ok2=0
for i in finishPoints:
    if i in val:
        ok2=1
if ok2==0:
    verificare=0
if verificare:
    for i in range(len(m)):
        matrix[statesOnly.index(m[i][0])][statesOnly.index(
            m[i][2])].append(m[i][1])
    word = input("word to test ")
    for i in matrix:
        print(i)
    ok_verif = 1
    poz_anterioara = []
    list = []
    for i in range(len(matrix)):
        if word[0] in matrix[0][i]:
            list.append(i)
        elif "*" in matrix[0][i]:
            for j in range(len(matrix[i])):
                if word[0] in matrix[i][j]:
                    list.append(j)
        else:
            ok_verif = 0
    poz_anterioara.append(list)

    for i in range(len(word)-1):
        list = []
        for j in range(len(poz_anterioara[i])):
            for k in range(len(matrix[poz_anterioara[i][j]])):
                if word[i+1] in matrix[poz_anterioara[i][j]][k]:
                    list.append(k)
                elif "*" in matrix[poz_anterioara[i][j]][k]:
                    for t in range(len(matrix[k])):
                        if word[i+1] in matrix[k][t]:
                            list.append(t)
        poz_anterioara.append(list)
    finalPointsIndex = []
    ok_veriff = 0
    for i in statesOnly:
        if i in finishPoints:
            finalPointsIndex.append(statesOnly.index(i))
    for i in finalPointsIndex:
        if i in poz_anterioara[-1]:
            ok_veriff = 1
    if(ok_veriff == 1 and ok_verif == 0):
        print("Valid !")
    else:
        print("Invalid !")
else:
    print("Invalid NFA !")
