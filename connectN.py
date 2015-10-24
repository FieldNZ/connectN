minrows = 3
maxrows = 10
mincolumns = 3
maxcolumns = 10
minwinlength = 3

def isInteger(n):
    result = True
    try:
        int(n)
        result = True
    except ValueError:
        print("That was not an Integer!")
        result = False
    return result

def inputInLimitCheck(x,min, max):
    response = True
    if x < min:
        print("That is too low! Must be at least %d" % min)
        response = False
    elif x > max:
        print("That is too high! Cannot be higher than %d" % max)
        response = False
    return response

def askForSetting(question, min, max):
    input = raw_input(question)
    if (isInteger(input)!=False):
        input = int(input)
        if (inputInLimitCheck(input, min, max)==True):
            result = input
        else:
            result = askForSetting(question, min, max)
    else:
        result = askForSetting(question, min, max)
    return result

def createGrid(columns, rows) :
    grid = []
    for row in range(0,rows):
        newRow = []
        for column in range(0,columns):
            newRow.append(0)
        grid.append(newRow)
    return grid

def printGrid(aGrid) :
    topline = "|"
    for n in range(0,len(aGrid)):
        topline += "-" + str(n) + "-|"
    print topline
    for row in aGrid:
        line = "| "
        for x in row:
            if (x == 0) :
                x = " "
            elif (x == 1) :
                x = "X"
            elif (x == 2) :
                x = "O"
            line = line + str(x) + " | "
        print line

def dropCoin(noColumns, grid, player) :
    global selectedColumn
    selectedColumn =  askForSetting("What column do you want to drop your coin? ", 0, noColumns-1)
    if isValidCoinDrop(selectedColumn, grid)==False :
        newGrid = dropCoin(noColumns, grid, player)
    else :
        for x in range(1,len(grid)+1) :
            if (x==len(grid)):
                grid[x-1][selectedColumn] = player
                newGrid = grid
            elif (grid[x][selectedColumn]!=0):
                grid[x-1][selectedColumn] = player
                newGrid = grid
                break
    return newGrid

def isValidCoinDrop(columnNo, grid):
    result = True
    if (grid[0][columnNo]!=0) :
        print "Column is already full!"
        result = False
    return result

def horizontalWinCheck(x,y,grid, player):
    streak = 0
    xleft = x
    xright = x + 1
    while (xleft>=0):
        if grid[y][xleft] == player:
            streak += 1
            xleft -= 1
        else:
            break
    while (xright<len(grid[0])):
        if grid[y][xright] == player:
            streak += 1
            xright += 1
        else:
            break
    return streak

def verticalWinCheck(x,y,grid,player):
    streak = 0
    yup = y
    ydown = y + 1
    while (yup>=0):
        if grid[yup][x] == player:
            streak += 1
            yup -= 1
        else:
            break
    while (ydown<len(grid)):
        if grid[ydown][x] == player:
            streak += 1
            ydown += 1
        else:
            break
    return streak

def NWSEWinCheck(x,y,grid,player):
    streak = 0
    yup = y
    ydown = y + 1
    xleft = x
    xright = x + 1
    while (yup>=0) and (xleft>=0):
        if grid[yup][xleft] == player:
            streak += 1
            yup -= 1
            xleft -= 1
        else:
            break
    while (ydown<len(grid)) and (xright<len(grid[0])):
        if grid[ydown][xright] == player:
            streak += 1
            ydown += 1
            xright += 1
        else:
            break
    return streak

def NESWWinCheck(x,y,grid,player):
        streak = 1
        yup = y
        ydown = y + 1
        xleft = x - 1
        xright = x
        while (yup>=0) and (xright<len(grid[0])):
            if grid[yup][xleft] == player:
                streak += 1
                yup -= 1
                xright += 1
            else:
                break
        while (ydown<len(grid)) and (xleft>=0):
            if grid[ydown][xleft] == player:
                streak += 1
                ydown += 1
                xleft -= 1
            else:
                break
        return streak

def winCheck(player, selectedColumn, grid, winlength):
    x = selectedColumn
    y = findLastRow(selectedColumn, grid)
    win = False
    if (horizontalWinCheck(x,y, grid, player)>=winlength) :
        win = True
    elif (verticalWinCheck(x,y,grid,player)>=winlength) :
        win = True
    elif (NESWWinCheck(x,y,grid,player)>=winlength) :
        win = True
    elif (NWSEWinCheck(x,y,grid,player)>=winlength) :
        win = True
    if (win == True):
        print("Player %d Wins!" % player)
    return win

def drawCheck(grid):
    result = True
    for x in grid[0]:
        if x == 0:
            result = False
            break
    if result == True:
        print("The Game is a Draw!")
    return result

def findLastRow(selectedColumn, grid) :
    for n in range(0,len(grid)):
        if grid[n][selectedColumn] != 0:
            result = n
            break
    return result

def initGame():
    noRows = askForSetting("How many rows? ", minrows, maxrows)
    noColumns = askForSetting("How many columns? ", mincolumns, maxcolumns)
    winLength = askForSetting("What is the win length? ", minwinlength, min(noRows, noColumns))
    grid = createGrid(noColumns, noRows)
    reciept = [grid, winLength]
    return reciept

def playGame(reciept):
    grid = reciept[0]
    winlength = reciept[1]
    printGrid(grid)
    noColumns = len(grid[0])
    player = 0
    complete = False
    while(complete==False) :
        player = (player%2)+1
        print("It is Player %d Turn!" % player)
        grid = dropCoin(noColumns, grid, player)
        complete = winCheck(player, selectedColumn, grid, winlength)
        if (complete!=True):
            complete = drawCheck(grid)
        printGrid(grid)

def endGame() :
    input = raw_input("Do you want to play again?(y/n) :")
    result = False
    if (input == "y"):
        print("Starting a New Game")
        result = True
    elif (input == "n"):
        print("Thanks for Playing!")
        result = False
    else:
        print("Please enter y for yes or n for no!")
        result = endGame()
    return result

newGame = True
while (newGame==True):
    reciept = initGame()
    playGame(reciept)
    newGame = endGame()
