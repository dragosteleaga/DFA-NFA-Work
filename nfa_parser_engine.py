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
#Verificam elem din tranzitie
for i in range(0, len(transitions), 3):
    if (transitions[i] or transitions[i+2]) not in state or transitions[i+1] not in sigma:
        verificare = 0
startPoint=[]
finishPoints=[]
#Verificam elementele din state
k=0
k1=0
for i in range(len(state)):
    if state[i] == "F":
        finishPoints.append(state[i-1])
    elif state[i] == "S" and state[i-1]=="F":
        startPoint = state[i-2]
    elif state[i] == "S":
        startPoint = state[i-1]
for i in state:
    if i=="S": #sa fie doar o stare de start
        k+=1
    elif i=="F":
        k1+=1
    if i!="S" and i!="F" and i not in transitions: #sa nu fie elem redundante in sigma
        verificare=0
if k!=1: #nu e doar un start
    verificare=0
if k1==0: # nu e nici un finish
    verificare=0
#Verificam sigma
for i in sigma:
    if i not in transitions:
        verificare=0


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
if verificare == 0:
    print("Invalid")
else:
    print("Valid")