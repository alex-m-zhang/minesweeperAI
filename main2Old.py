import time
import random
import math
from PIL import ImageGrab
import win32ui
from directKeys import click, queryMousePosition, pos
from MouseMovement import mouse_bez

#1-2-1 scenario is always solvable
#not straight mouse movements

#FULLSCREEN minesweeper!

#0.09s = 46s (monthly high)
#0.03s = 40s (#3 all time)
SLEEPTIME = 0.00 #obsolete now since we have mouse movement
EPSILON = 0.0000 #obsolete now since we have mouse movement
MOUSESLEEP = 0.000#0.003 obsolete now since we have mouse movement
MOUSESPEED = 0.0008

def calcSleep():
    return random.randrange(1, 81) * EPSILON + SLEEPTIME

mouseBoxSize = 20
boxSize = 20
#expert
numBombs = 99
numBoxesX = 30
numBoxesY = 16
leftMouseX = 436
leftScreenX = 444
#medium
#numBombs = 40
#numBoxesX = 16
#numBoxesY = 16
#leftMouseX = 238
#leftScreenX = 475
#beginner
#numBoxesX = 9
#numBoxesY = 9
#numBombs = 10
#leftMouseX = 238
#leftScreenX = 475

mouse_game_coords = (leftMouseX, 172, leftMouseX+(mouseBoxSize*numBoxesX), 172+(mouseBoxSize*numBoxesY))
game_coords = (leftScreenX, 180, leftScreenX+(boxSize*numBoxesX), 180+(boxSize*numBoxesX))

#screen = ImageGrab.grab(bbox=game_coords)
#screen.show()

topLeft = [leftMouseX+int(mouseBoxSize/2), 172+int(mouseBoxSize/2)]
reset = [736, 143]

previous_clicks = []

start_time = time.time()

def dist(x1, y1, x2, y2):
    diffX = abs(x1-x2)
    diffY = abs(y1-y2)
    return math.sqrt(diffX ** 2 + diffY ** 2)

def randomClickVariation():
    return random.randint(-5, 6)

#convert mouse coordinates to screren coordinates
def convertMouseToScreen(x, y):
    toReturnX = 2 * (x - leftMouseX)
    toReturnY = 2 * (y - 173)

    return toReturnX, toReturnY

#if the color is close enough (+- 10) on all three values then return true
def closeEnough(rgb, comparison):
    if abs(rgb[0] - comparison[0]) <= 10:
        if abs(rgb[1] - comparison[1]) <= 10:
            if abs(rgb[2] - comparison[2]) <= 10:
                return True
    return False

def rgba(colorref):
    mask = 0xff
    return [(colorref & (mask << (i * 8))) >> (i * 8) for i in range(4)]

def getPixelColor(x, y):
    name = "Minesweeper Online - Play Free Online Minesweeper - Google Chrome" #just an example of a window I had open at the time
    w = win32ui.FindWindow( None, name )
    dc = w.GetWindowDC()
    toReturn = dc.GetPixel(x, y)
    dc.DeleteDC()
    return toReturn

#converts a point on the screen to a number.
#0-8 for 0-8, f for flag, c for covered
#x and y must be at center of screen
def convertPointToNum(x, y):
    color = rgba(getPixelColor(x, y+7)) #2 is offcenter
    if closeEnough(color, (20, 130, 20)):
        return "2"
    color = rgba(getPixelColor(x, y-10)) #7 is offcenter
    if closeEnough(color, (94, 94, 94)):
        return "7"
    color = rgba(getPixelColor(x, y))
    if closeEnough(color, (189, 189, 189)):
        topColor = rgba(getPixelColor(x-17, y-17))
        if closeEnough(topColor, (255, 255, 255)): #is now white, so it was covered
            return "c"
        else:
            return "0"
    if closeEnough(color, (53, 53, 236)):
        return "1"
    if closeEnough(color, (222, 94, 94)):
        return "3"
    if closeEnough(color, (228, 48, 48)) and closeEnough(rgba(getPixelColor(x, y+10)), (0, 0, 0)): #flag is red on top and black on bottom
        return "f"
    if closeEnough(color, (47, 47, 139)):
        return "4"
    if closeEnough(color, (156, 94, 94)):
        return "5"
    if closeEnough(color, (94, 156, 156)):
        return "6"
    if closeEnough(color, (156, 156, 156)):
        return "8"
    if closeEnough(color, (0, 0, 0)): #mine uncovered :(
        return "m"
    return "d"

xPoints = []
yPoints = []
avgLength = 0
timesCalled = 0

def move(x, y, xNew, yNew):
    global xPoints, yPoints, avgLength, timesCalled
    xDist = xNew - x
    yDist = yNew - y

    distance = int(dist(x, y, xNew, yNew))

    #if distance > 114:
    if distance > 0:
        if distance < 100:
            deriv = random.randint(int(distance/4), int(distance/3))
        else:
            deriv = random.randint(int(distance/10), int(distance/8))
        if deriv % 2 == 1:
            deriv += 1
        length = (math.sqrt(distance)*8 +10)/100
        avgLength += length
        timesCalled += 1
        points = mouse_bez((x, y), (xNew, yNew), deriv, length)
        
        for i in range(len(points)):
            if i != 0 and int(points[i][0]) != int(points[i-1][0] and int(points[i][1]) != int(points[i-1][1])):
                pos(int(points[i][0]), int(points[i][1]))
                xPoints.append(int(points[i][0]))
                yPoints.append(int(points[i][1]))
                time.sleep(distance/len(points)*1E-13)
    else:
        if distance == 0:
            return

        incrementX = xDist/distance
        incrementY = yDist/distance

        for i in range(distance):
            pos(int(x + i * incrementX), int(y + i * incrementY))
            xPoints.append(int(x+i*incrementX))
            yPoints.append(int(y+i*incrementY))
            time.sleep(MOUSESPEED)

def getAdjacentSquares(row, column):
    toReturn = []
    if row != 0:
        if column != 0:
            toReturn.append([row-1, column-1])
        toReturn.append([row-1, column])
        if column != numBoxesX - 1:
            toReturn.append([row-1, column+1])
    if column != 0:
        toReturn.append([row, column-1])
    if column != numBoxesX - 1:
        toReturn.append([row, column+1])
    if row != numBoxesY - 1:
        if column != 0:
            toReturn.append([row+1, column-1])
        toReturn.append([row+1, column])
        if column != numBoxesX - 1:
            toReturn.append([row+1, column+1])
    return toReturn

print("initialized")

# only start the program after the mouse is on the left screen
while True:
    mouse_pos = queryMousePosition()
    if mouse_pos.x <= 0:
        break

#calibrator:
#while True:
#    mouse_pos = queryMousePosition()
#    print(str(mouse_pos.x) + "   " + str(mouse_pos.y))
#    time.sleep(1)

print("alright we good to go")
lastClick = ((mouse_game_coords[0] + 10, mouse_game_coords[1] + 10))
#playOnce = False
attempts = 0
while True:
    print("HI")
    #time.sleep(1)
    mouse_pos = queryMousePosition()
    #print(str(mouse_pos.x) + "    " + str(mouse_pos.y))
    click(mouse_game_coords[0] + 10, mouse_game_coords[1] + 10)

    if mouse_game_coords[0] < mouse_pos.x < mouse_game_coords[2] and mouse_game_coords[1] < mouse_pos.y < mouse_game_coords[3]:
        clicks = 0
        start_time = time.time()
        #centerX = int(numBoxesX/2) * mouseBoxSize + 10
        #centerY = int(numBoxesY/2) * mouseBoxSize + 10
        move(lastClick[0], lastClick[1], mouse_game_coords[0] + 10, mouse_game_coords[1] + 10)
        click(mouse_game_coords[0] + 10, mouse_game_coords[1] + 10) #first click in the center
        clicks += 1
        lastClick = (mouse_game_coords[0] + 10, mouse_game_coords[1] + 10)
        attempts += 1
        time.sleep(calcSleep())

        gameOver = False

        allFlags = []
        xs = []

        screenShotTime = 0
        sleepyTime = 0
        calcTime = 0
        timesScreenshot = 0
        avgLength = 0
        timesCalled = 0
        loops = 0

        #every square that was covered before but is now uncovered, get pixel the 8 around it.
        while True:
            if loops == 0: #first time through, read everything
                time.sleep(4)
                startTime = time.time()
                gameStatus = []
                #read in info
                nowReading = [20, 20]
                originalColumn = 20
                for row in range(numBoxesY):
                    gameRow = []
                    for column in range(numBoxesX):
                        gameRow.append(convertPointToNum(nowReading[0], nowReading[1]))
                        nowReading[0] += 40
                    nowReading[1] += 40
                    nowReading[0] = originalColumn
                    gameStatus.append(gameRow)
                    gameRow = []
                
                for flag in allFlags:
                    gameStatus[flag[0]][flag[1]] = 'f'
                for x in xs:
                    gameStatus[x[0]][x[1]] = 'x'
                
                screenShotTime += time.time() - startTime
                screenTime = time.time() - startTime
                calcStartTime = time.time()
                timesScreenshot += 1
                flagCount = 0
                coveredCount = 0
            else:
                pass
                #just read every square that was covered before

            for row in range(len(gameStatus)):
                for column in range(len(gameStatus[row])):
                    if gameStatus[row][column] == 'c':
                        if gameStatus[row][column] == 'c':
                            coveredCount += 1
            
            change = False
            bombChange = False

            potentialClicks = []

            for row in range(len(gameStatus)):
                for column in range(len(gameStatus[row])):
                    if gameStatus[row][column] == 'x' or gameStatus[row][column] == 'f' or gameStatus[row][column] == 'c':
                        if gameStatus[row][column] == 'f':
                            flagCount += 1
                        continue
                    elif gameStatus[row][column] == 'm' or gameStatus[row][column] == 'd':
                        print("there's a mine or d")
                        gameOver = True
                        break
                    number = int(gameStatus[row][column])
                    bombs = []
                    covers = []
                    squares = getAdjacentSquares(row, column)
                    for i in range(len(squares)):
                        if gameStatus[squares[i][0]][squares[i][1]] == 'f':
                            bombs.append([squares[i][0] - row, squares[i][1] - column])
                        if gameStatus[squares[i][0]][squares[i][1]] == 'c':
                            covers.append([squares[i][0] - row, squares[i][1] - column])
                    #123
                    #4 5
                    #678
                    if len(bombs) + len(covers) == 0:
                        gameStatus[row][column] = 'x'
                        xs.append([row, column])
                    if len(bombs) + len(covers) == number: #all covered are bombs
                        for cover in covers:
                            #clickX = mouse_game_coords[0] + 10 + ((column + cover[1]) * 10)
                            #clickY = mouse_game_coords[1] + 10 + ((row + cover[0]) * 10)
                            #print("RIGHT CLICK " + str(clickX) + "   " + str(clickY))
                            #rightClick(clickX, clickY)
                            allFlags.append([row + cover[0], column + cover[1]])
                            gameStatus[row][column] = 'f'
                            bombChange = True
                    if len(bombs) == number: #all covered are ok
                        if len(covers) != 0:
                            newClicks = []
                            for cover in covers:
                                clickX = mouse_game_coords[0] + 10 + ((column + cover[1]) * mouseBoxSize) + randomClickVariation()
                                clickY = mouse_game_coords[1] + 10 + ((row + cover[0]) * mouseBoxSize) + randomClickVariation()
                                #click(clickX, clickY)
                                #lastClick = (clickX, clickY)
                                newClicks.append([clickX, clickY])
                                change = True
                                #time.sleep(calcSleep())
                            distance = dist(lastClick[0], lastClick[1], newClicks[0][0], newClicks[0][1])
                            newClicks.append(distance)
                            potentialClicks.append(newClicks)
                    gameStatus[row][column] = number - len(bombs)
                    """if row != 0 and row != 1:
                        if gameStatus[row-2][column] == 1 and gameStatus[row-1][column] == 2:
                            clickX = mouse_game_coords[0] + 10 + (column)*mouseBoxSize
                            clickY = mouse_game_coords[1] + 10 + (row)*mouseBoxSize
                            print("121!" + str(clickX) + "    " + str(clickY))
                            columnToClick = -5
                            if column != 0 and gameStatus[row-2][column-1] == 'c' and gameStatus[row-1][column-1] == 'c' and gameStatus[row][column-1] == 'c':
                                if column != numBoxesX and gameStatus[row-2][column+1] != 'c' and gameStatus[row-1][column+1] != 'c' and gameStatus[row][column+1] != 'c':
                                    columnToClick = column - 1
                            if column != numBoxesX and gameStatus[row-2][column+1] == 'c' and gameStatus[row-1][column+1] == 'c' and gameStatus[row][column+1] == 'c':
                                if column != 0 and gameStatus[row-2][column-1] != 'c' and gameStatus[row-1][column-1] != 'c' and gameStatus[row][column-1] != 'c':
                                    columnToClick = column + 1
                            if columnToClick != -5:
                                newClicks = []
                                clickX = mouse_game_coords[0] + 10 + randomClickVariation() + (columnToClick)*mouseBoxSize
                                clickY = mouse_game_coords[1] + 10 + randomClickVariation() + (row-2)*mouseBoxSize
                                newClicks.append([clickX, clickY])
                                change = True
                                clickX = mouse_game_coords[0] + 10 + randomClickVariation() + (columnToClick)*mouseBoxSize
                                clickY = mouse_game_coords[1] + 10 + randomClickVariation() + (row-1)*mouseBoxSize
                                newClicks.append([clickX, clickY])
                                distance = dist(lastClick[0], lastClick[1], newClicks[0][0], newClicks[0][1])
                                newClicks.append(distance)
                                potentialClicks.append(newClicks)
                    if row != numBoxesY - 1 and row != numBoxesY - 2:
                        if gameStatus[row+1][column] == 2 and gameStatus[row+2][column] == 1:
                            clickX = mouse_game_coords[0] + 10 + (column)*mouseBoxSize
                            clickY = mouse_game_coords[1] + 10 + (row)*mouseBoxSize
                            print("121!" + str(clickX) + "    " + str(clickY))
                            columnToClick = -5
                            if column != 0 and gameStatus[row+2][column-1] == 'c' and gameStatus[row+1][column-1] == 'c' and gameStatus[row][column-1] == 'c':
                                if column != numBoxesX and gameStatus[row+2][column+1] != 'c' and gameStatus[row+1][column+1] != 'c' and gameStatus[row][column+1] != 'c':
                                    columnToClick = column - 1
                            if column != numBoxesX and gameStatus[row+2][column+1] == 'c' and gameStatus[row+1][column+1] == 'c' and gameStatus[row][column+1] == 'c':
                                if column != 0 and gameStatus[row+2][column-1] != 'c' and gameStatus[row+1][column-1] != 'c' and gameStatus[row][column-1] != 'c':
                                    columnToClick = column + 1
                            if columnToClick != -5:
                                newClicks = []
                                clickX = mouse_game_coords[0] + 10 + randomClickVariation() + (columnToClick)*mouseBoxSize
                                clickY = mouse_game_coords[1] + 10 + randomClickVariation() + (row+2)*mouseBoxSize
                                newClicks.append([clickX, clickY])
                                change = True
                                clickX = mouse_game_coords[0] + 10 + randomClickVariation() + (columnToClick)*mouseBoxSize
                                clickY = mouse_game_coords[1] + 10 + randomClickVariation() + (row+1)*mouseBoxSize
                                newClicks.append([clickX, clickY])
                                distance = dist(lastClick[0], lastClick[1], newClicks[0][0], newClicks[0][1])
                                newClicks.append(distance)
                                potentialClicks.append(newClicks)"""
                if gameOver:
                    break
            if change and not bombChange:
                potentialClicks = sorted(potentialClicks, key=lambda x: x[-1])
                for i in range(len(potentialClicks[0])):
                    if potentialClicks[0][i] != potentialClicks[0][-1]:
                        mouseTravel = dist(lastClick[0], lastClick[1], potentialClicks[0][i][0], potentialClicks[0][i][1])
                        toSleep = mouseTravel * MOUSESLEEP
                        if i == 0 and toSleep > screenTime:
                            toSleep -= screenTime
                        sleepyTime += toSleep
                        time.sleep(toSleep)
                        move(lastClick[0], lastClick[1], potentialClicks[0][i][0], potentialClicks[0][i][1])
                        click(potentialClicks[0][i][0], potentialClicks[0][i][1])
                        clicks += 1
                        lastClick = (potentialClicks[0][i][0], potentialClicks[0][i][1])
                        change = True
                        time.sleep(calcSleep())
            loops += 1
            #if flagCount + coveredCount == numBombs:
            #    print(flagCount)
            #    print(coveredCount)
            #    print("flag + cover = numBomb")
            #    gameOver = True
            if gameOver:
                break
            if not change and not bombChange:
                potential = []
                for row in range(len(gameStatus)):
                    for column in range(len(gameStatus[row])):
                        if gameStatus[row][column] == 'c':
                            squares = getAdjacentSquares(row, column)
                            for i in range(len(squares)):
                                if gameStatus[squares[i][0]][squares[i][1]] != 'c' and gameStatus[squares[i][0]][squares[i][1]] != 'f':
                                    potential.append([row, column])
                if len(potential) != 0:
                    choice = random.choice(potential)
                    clickX = mouse_game_coords[0] + 10 + ((choice[1]) * mouseBoxSize) + randomClickVariation()
                    clickY = mouse_game_coords[1] + 10 + ((choice[0]) * mouseBoxSize) + randomClickVariation()
                    mouseTravel = dist(lastClick[0], lastClick[1], clickX, clickY)
                    toSleep = mouseTravel * MOUSESLEEP
                    if toSleep > screenTime:
                        toSleep -= screenTime
                    sleepyTime += toSleep
                    time.sleep(toSleep) #wait a bit before clicking
                    move(lastClick[0], lastClick[1], clickX, clickY)
                    click(clickX, clickY)
                    clicks += 1
                    lastClick = (clickX, clickY)
                    print("random :(")
                    sleepyTime += calcSleep()
                    time.sleep(calcSleep())
            calcTime += time.time() - calcStartTime
        if gameOver:
            hardBreak = True
            print(calcTime - sleepyTime)
            print("SLEEPY TIME: " + str(sleepyTime))
            print("SCREENSHOT TIME: " + str(screenShotTime))
            print("SCREENSHOTS: " + str(timesScreenshot))
            print("CLICKS: " + str(clicks))
            if timesCalled != 0:
                print("AVG LENGTH: " + str(avgLength/timesCalled))
            clicks = 0
            screen = ImageGrab.grab(bbox=game_coords)
            #screen.show()
            screen = screen.load()

            gameStatus = []
            #read in info
            nowReading = [20, 20]
            originalColumn = 20
            for row in range(numBoxesY):
                gameRow = []
                for column in range(numBoxesX):
                    gameRow.append(convertPointToNum(nowReading[0], nowReading[1]))
                    nowReading[0] += 40
                nowReading[1] += 40
                nowReading[0] = originalColumn
                gameStatus.append(gameRow)
                gameRow = []
            time.sleep(random.randrange(102, 445)/100)
            move(lastClick[0], lastClick[1], reset[0], reset[1])
            click(reset[0], reset[1])
            clicks += 1
            lastClick = (reset[0], reset[1])
            time.sleep(1)
            startTime = time.time()
            screen = ImageGrab.grab(bbox=game_coords)
            #screen.show()
            screen = screen.load()
            #read in info
            nowReading = [20, 20]
            originalColumn = 20
            for row in range(numBoxesY):
                gameRow = []
                for column in range(numBoxesX):
                    if convertPointToNum(nowReading[0], nowReading[1]) != gameStatus[row][column]:
                        hardBreak = False
                    nowReading[0] += 40
                nowReading[1] += 40
                nowReading[0] = originalColumn
            import matplotlib.pyplot as plt
            plt.plot(xPoints, yPoints)
            plt.ylabel('some numbers')
            plt.show()
            xPoints = []
            yPoints = []
            if hardBreak:
                print(str(attempts) + " attempts!")
                break
            else:
                move(lastClick[0], lastClick[1], mouse_game_coords[0] + 20, mouse_game_coords[1] + 20)
                click(mouse_game_coords[0] + 20, mouse_game_coords[1] + 20) #first click in the corner
                clicks += 1
                lastClick = (mouse_game_coords[0] + 20, mouse_game_coords[1] + 20)
            #looping through all squares:

#if it's a number with all 8 solved, mark as x
#count surroundings (bombs + covered)
#if bombs match number, left-click covered
#if covered + bombs match number, right click covered
#if changes after full scan, randomly click somewhere
#if there

        #CPS troller (uncomment playOnce = False above)
        #if not playOnce:
        #    start_time = time.time()
        #    while time.time() - start_time < 5:
        #        time.sleep(0.005)
        #        click(topLeft[0]+300, topLeft[1]+160)
        #    playOnce = True

        #click every single square
        #start_time = time.time() #
        #nowClicking = [topLeft[0], topLeft[1]]
        #originalColumn = topLeft[1]
        #for row in range(30):
        #    for column in range(16):
        #        rightClick(nowClicking[0], nowClicking[1])
        #        time.sleep(1)
        #        click(reset[0], reset[1]) #reset key on top
        #        time.sleep(1)
        #        nowClicking[1] += 20
        #    nowClicking[0] += 20
        #    nowClicking[1] = originalColumn
        #print(time.time() - start_time)