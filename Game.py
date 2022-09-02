##### Hnefltafl
##### Michal Doneberk


### Import and variables ###

import random #for AI priority

##Gameover variables
KingCaptured=False 
KingEscaped=False

##Gameboard variables
#setting gameboard
Board = []
BoardSize = 0
BoardLetters = ""

##Player/AI sides
# 0 = neutral,1 = defender,-1 = attacker
# for checking oposite sides
PlayerSide = 0
AISide = 0
Turn = 0

##Possible movement paths
#storing movement options
Path = []
AIPath = []

###Setting-up functions
##Board
def SetBoard():
    #Board variables
    global Board
    global BoardSize
    global BoardLetters

    #LoadingBoard
    SelectedBoard=False
    while SelectedBoard==False:
        print("Board size 7x7,9x9,11x11")
        n = input("- ")
        if n=="7x7":
            BoardSize = 9
            BoardFile = open("Board (7x7).txt",'r').readlines()
            SelectedBoard=True
        if n=="9x9":
            BoardSize = 11
            BoardFile = open("Board (9x9).txt",'r').readlines()
            SelectedBoard=True
        if n=="11x11":
            BoardSize = 13
            BoardFile = open("Board (11x11).txt",'r').readlines()
            SelectedBoard=True
            
    #Setting up coordinates text for PrintBoard()
    for i in range(0,BoardSize-2):
        BoardLetters = BoardLetters +chr(97+i)+" "
        
    #Generating board from file     
    for y in range(0,BoardSize):
        Board.append([])
        for x in range(0,BoardSize):
            if BoardFile[y][x]=="0": #Generating empty spaces
                Board[y].append(Tile())
                Board[y][x].Type="Empty"
                Board[y][x].Look=" "
            if BoardFile[y][x]=="1": #Generating attackers
                Board[y].append(Tile())
                Board[y][x].Type="Unit"
                Board[y][x].Owner=-1
                Board[y][x].Look="a"
            if BoardFile[y][x]=="2": #Generating defenders
                Board[y].append(Tile())
                Board[y][x].Type="Unit"
                Board[y][x].Owner=1
                Board[y][x].Look="b"
            if BoardFile[y][x]=="3":
                Board[y].append(Tile())
                Board[y][x].Type="King" #Generating king
                Board[y][x].Owner=1
                Board[y][x].Look="B"
            if BoardFile[y][x]=="4":
                Board[y].append(Tile())
                Board[y][x].Type="Corner" #Generating corners
                Board[y][x].Look="C"
            if BoardFile[y][x]=="5":
                Board[y].append(Tile())
                Board[y][x].Type="End" #Generating borders
            Board[y][x].Location=[y,x]
    #Generating tile relations
    for y in range(0,BoardSize):
        for x in range(0,BoardSize):
            if Board[y][x].Type!="End":
                Board[y][x].Left=Board[y][x-1]
                Board[y][x].Right=Board[y][x+1]
                Board[y][x].Up=Board[y-1][x]
                Board[y][x].Down=Board[y+1][x]
                
##Starting settings
def StartGame():
    global PlayerSide
    global AISide
    global Turn
    
    #Choosing side
    SelectedSide=False
    while SelectedSide==False:
        print("Which side are you playing as? (Attacker(A)/Defender(B))")
        n = input("- ")
        if n=="A":
            PlayerSide = -1
            AISide = 1
            SelectedSide=True
        if n=="B":
            PlayerSide = 1
            AISide = -1
            SelectedSide=True
    
    #Choosing who plays first
    SelectedFirst=False
    while SelectedFirst==False:
        print("Which side plays first? (Attacker(A)/Defender(B))")
        n = input("- ")
        if n=="A":
            Turn = -1
            SelectedFirst=True
        if n=="B":
            Turn = 1
            SelectedFirst=True
###Tiles and their interaction
##Tile
class Tile:
    def __init__(self):
        self.Owner=0 # 0 = Neutral, 1  =Defender, -1 = Attacker
        self.Type="Empty" #Empty,Attacker,Defender,King,Corner,End
        self.Look=" " #displaying tile (" ","a","b","B","C")
        self.Location=[0,0] #coordinates on board [a,b]=Board[a][b]
        #Neighbors
        self.Left=None 
        self.Right=None
        self.Up=None
        self.Down=None
    #Change self to "Empty"
    def Removed(self):
        if self.Type=="Unit":
            self.Type="Empty"
            self.Look=" "
            self.Owner=0
        # King defeat
        if self.Type=="King":
            global KingCaptured
            KingCaptured=True
##Function to trigger neighbors to change to "Empty"
#checks if neighbour is opposite player and if is threatened from opposits side
def Remove (Node):
    if Node.Left.Owner*Node.Owner==-1:
        if Node.Left.Left.Owner==Node.Owner:
            Node.Left.Removed()
    if Node.Right.Owner*Node.Owner==-1:
        if Node.Right.Right.Owner==Node.Owner:
            Node.Right.Removed()
    if Node.Up.Owner*Node.Owner==-1:
        if Node.Up.Up.Owner==Node.Owner:
            Node.Up.Removed()
    if Node.Down.Owner*Node.Owner==-1:
        if Node.Down.Down.Owner==Node.Owner:
            Node.Down.Removed()
##Function to move by overwriting target           
def Move (Moving,Place):
    Place.Look=Moving.Look
    Place.Owner=Moving.Owner
    Place.Type=Moving.Type
    Moving.Look=" "
    Moving.Owner=0
    Moving.Type="Empty"
    Remove(Place) #Trigger to remove enemy by moving

###Finding valid moves
##Starting function to find near empty spaces
#Path - for finding valid Tiles for player to move
#AIPath - for finding valid moves for AI [priority,target,moving tile]
def FindPath(Node):
    global Path
    global AIPath
    #Divides to directions
    if Node.Left.Type=="Empty":
        FindPathLeft(Node.Left,Node)
    if Node.Right.Type=="Empty":
        FindPathRight(Node.Right,Node)
    if Node.Up.Type=="Empty":
        FindPathUp(Node.Up,Node)
    if Node.Down.Type=="Empty":
        FindPathDown(Node.Down,Node)
    #King exeption for corner move and high priority AI move
    if Node.Left.Type=="Corner" and Node.Type=="King":
        AIPath.append([100,Node.Left,Node])
        Path.append(Node.Left)
    if Node.Right.Type=="Corner" and Node.Type=="King":
        AIPath.append([100,Node.Right,Node])
        Path.append(Node.Right)
    if Node.Up.Type=="Corner" and Node.Type=="King":
        AIPath.append([100,Node.Up,Node])
        Path.append(Node.Up)
    if Node.Up.Type=="Corner" and Node.Type=="King":
        AIPath.append([100,Node.Up,Node])
        Path.append(Node.Up)
        
#Finding left path    
def FindPathLeft(Node,Original):
    global Path
    global AIPath
    Path.append(Node)
    AIPath.append([AIPathValue(Node,Original.Owner),Node,Original])
    if Node.Left.Type=="Empty":
        FindPathLeft(Node.Left,Original)
    if Node.Left.Type=="Corner" and Original.Type=="King":
        AIPath.append([1000,Node.Left,Original])
        Path.append(Node.Left)
        
#Finding right path         
def FindPathRight(Node,Original):
    global Path
    global AIPath
    Path.append(Node)
    AIPath.append([AIPathValue(Node,Original.Owner),Node,Original])
    if Node.Right.Type=="Empty":
        FindPathRight(Node.Right,Original)
    if Node.Right.Type=="Corner" and Original.Type=="King":
        AIPath.append([1000,Node.Right,Original])
        Path.append(Node.Right)
        
#Finding up path       
def FindPathUp(Node,Original):
    global Path
    global AIPath
    Path.append(Node)
    AIPath.append([AIPathValue(Node,Original.Owner),Node,Original])
    if Node.Up.Type=="Empty":
        FindPathUp(Node.Up,Original)
    if Node.Up.Type=="Corner" and Original.Type=="King":
        AIPath.append([1000,Node.Up,Original])
        Path.append(Node.Up)
        
#Finding down path         
def FindPathDown(Node,Original):
    global Path
    global AIPath
    Path.append(Node)
    AIPath.append([AIPathValue(Node,Original.Owner),Node,Original])
    if Node.Down.Type=="Empty":
        FindPathDown(Node.Down,Original)
    if Node.Down.Type=="Corner" and Original.Type=="King":
        AIPath.append([1000,Node.Down,Original])
        Path.append(Node.Down)

###AI
##Function to adjust priority for movement target
def AIPathValue(Node,Side):
    global AISide
    AIPriority = random.randint(0, 100)#Random priority to prevent same moves
    if Node.Left.Owner*Side==-1:
        if Node.Left.Left.Owner==Side:
            AIPriority += 100
    if Node.Right.Owner*Side==-1:
        if Node.Right.Right.Owner==Side:
            AIPriority += 100
    if Node.Up.Owner*Side==-1:
        if Node.Up.Up.Owner==Side:
            AIPriority += 100
    if Node.Down.Owner*Side==-1:
        if Node.Down.Down.Owner==Side:
            AIPriority += 100
    #Aditional priority aginst King
    if Side==1:
        if Node.Left.Type=="King":
            AIPriority += 100
        if Node.Right.Type=="King":
            AIPriority += 100
        if Node.Up.Type=="King":
            AIPriority += 100
        if Node.Down.Type=="King":
            AIPriority += 100
    return AIPriority
##AITurn
def AITurn():
    global AIPath
    global AISide
    global BoardSize
    global Board
    
    AIPath = []#Clearing possible moves

    #Finding AI-controlled tiles and generating all possible moves
    for y in range (1,BoardSize-1):
        for x in range (1,BoardSize-1):
            if Board[y][x].Owner==AISide:
                FindPath(Board[y][x])

    #Finding most priority move
    if len(AIPath)>0:
        AIMax=[AIPath[0][0],AIPath[0][1],AIPath[0][2]]
        for i in range (0,len(AIPath)):
            AINew=[AIPath[i][0],AIPath[i][1],AIPath[i][2]]
            
            #Adjusting priority for king (based on distance to corner)
            if AINew[2].Type=="King":
                AINew[0] += 50*(abs(AINew[1].Location[0]-(BoardSize//2))+abs(AINew[1].Location[1]-(BoardSize//2)))
                
            if AINew[0]>AIMax[0]:
                AIMax=AINew  
        Move(AIMax[2],AIMax[1])
###Player
##PlayerTurn
def MovePlayer():
    global Path
    global PlayerSide
    
    ValidStart = False
    ValidEnd = False
    
    Path=[]#Clearing possible moves

    #Input of valid player starting tile
    while ValidStart==False:
        try:
            StartingPoint = input("Starting point: ")
            StartingPoint=PlayerInputTranslator(StartingPoint)#Translated from chess-like coordinates
            FindPath(StartingPoint)#Generating moves from input
            if len(Path)>0 and StartingPoint.Owner==PlayerSide:#Check if can move
                ValidStart=True
        except:
            ValidStart=False
            
    #Input of valid player ending tile          
    while ValidEnd==False:
        try:
            EndingPoint = input("Ending point: ")
            EndingPoint=PlayerInputTranslator(EndingPoint)#Translated from chess-like coordinates
            if EndingPoint in Path:#Check if move exists
                ValidEnd=True
        except:
            ValidEnd=False
    #Making move
    Move(StartingPoint,EndingPoint)

##Function to translate from chess-like coordinates
def PlayerInputTranslator(n):
    global Board
    n=n.split()# Splitting input by space
    n[0]=ord(n[0])-96 #Converting fom lower-case letters
    n[1]=BoardSize-int(n[1])-1 #"flipping" from ascending to descending
    n[0],n[1]=n[1],n[0] #"flipping" coordinates"
    return Board[n[0]][n[1]]#returning Tile by position (if doesnt exist is caught in PlayerMove() )
###Gameplay
##Displaying board
def PrintBoard():
    global BoardSize
    global Turn
    #printing everything except "edges"
    for y in range (1,BoardSize-1):
        for x in range (1,BoardSize-1):
            if x<(BoardSize-2):
                print (Board[y][x].Look,end=' ')
            if x==(BoardSize-2):
                print (Board[y][x].Look,BoardSize-y-1,end='\n')#enumerating end
    print(BoardLetters)#printing letters for player input
 
##GameTurn           
def GameTurn():
    global Turn
    global PlayerSide
    global AISide
    global Board
    global BoardSize
    global KingEscaped
    #Displaying
    print("")
    if Turn==-1:
        print("- - - Attacker Turn - - -")
    if Turn==1:
        print("- - - Defender Turn - - -")
    PrintBoard()

    #Player/AI moves
    if Turn==PlayerSide:
        MovePlayer()
    if Turn==AISide:
        AITurn()
    Turn=Turn*(-1)#changes active player

    #Checking if king escaped
    if Board[BoardSize-2][BoardSize-2].Type=="King" or Board[1][BoardSize-2].Type=="King" or Board[BoardSize-2][1].Type=="King" or Board[1][1].Type=="King":
        KingEscaped=True
    

###Running the game
StartGame()
SetBoard()
#Playing game until conditions change
while KingCaptured==False and KingEscaped==False:
    GameTurn()
###End
print("")
if KingEscaped==True:
    print("King has escaped!")
if KingCaptured==True:
    print("King was captured!")





