#The game opens in 600x900 window
# <b> - show boss key/hide boss key
# <esc> -stop the game/resume the game 
# !if boss key is clicked while playing you have to click <esc> to resume the game
# <space> - fly up
# difficulty increases by increasing pipe speed and decreasing pipe hole
# CHEAT CODES:
# "slow": slows down the pipes
# "holyhole": increases the pipe hole
# "supergareth": speaks for itself
from tkinter import Tk, Canvas, PhotoImage, Button, Label, Entry
import random
import os

#setting main window in the center of user's screen
def setWindowDimensions(w, h):
	window = Tk()
	window.title("Flappy Bird")
	window.resizable(width = False, height = False) #Window cannot be ajusted 
	ws = window.winfo_screenwidth()
	wh = window.winfo_screenheight()
	x = (ws/2) - (w/2)
	y = (wh/2) - (h/2)
	window.geometry('%dx%d+%d+%d' % (w, h, x, y))
	return window

#checking if pipes overlap with the bird
def overLapping(a, b):
	if a[0] < b[2] and a[2] > b[0] and a[1] < b[3] and a[3] > b[1]:
		return True
	return False

#checks if the bird touches the ground or goes beyond the screen
def outOfScreen():
	global birdY
	if birdY < 0 or birdY > 850:
		return True
	return False

#pipes movement
def movePipes():
	global pipesX
	global score
	global pipeSpeed
	global pipeHole
	#loop through each pipe to check its position
	for i in range(len(pipesX)):
		#if pipe still on the screen just move left
		if pipesX[i] > -100:
			pipesX[i] += pipeSpeed 
			canvas.move(upPipes[i], pipeSpeed, 0) #move upper element of a pipe
			canvas.move(downPipes[i], pipeSpeed, 0) #move lower element of a pipe
		#if out of screen move to the right of canvas
		else:
			score += 1 #If the pipe goes out of screen increment score
			#Making game increase in difficulty over time
			#every 10 points increase pipe speed until it reaches maximum
			if score % 10 == 0 and pipeSpeed > -14:
				pipeSpeed-= 2 
			#every 5 points decrease pipe Hole until it reaches Maximum
			if score % 5 == 0 and pipeHole > 200:
				pipeHole -= 25
			canvas.itemconfig(scoreText, text=str(score)) #update score Text
			pipesX[i] = 1400 #assign new x Coord to move the pipe to the right
			pipesY[i] = random.randint(0,600) #Hole appears in a random space between lower and upper pipe
			canvas.coords(upPipes[i], pipesX[i], 0, pipesX[i] + 100, pipesY[i])	#update coords of upper pipe	
			canvas.coords(downPipes[i], pipesX[i], pipesY[i] + pipeHole, pipesX[i] + 100, 900) #update coords of lower pipe

#bird gains velocity upward on space click
def flyUp(event):
	global birdY
	global gravity
	global pause
	#execute only when game is running
	if not pause:
		gravity = -15 #updates velocity to 15 upwards
		birdY+=gravity # move by that amount
		canvas.coords(bird, birdX, birdY) #update the birds position

#bird loses upwards velocity each frame when game is running
#this function will also call move pipes function
def flyDown():
	global birdY
	global gravity
	global pause
	#execute only if game is running
	if not pause:
		gravity +=1 #each call decrease velocity
		birdY += gravity
		canvas.coords(bird, birdX, birdY) #update position of the bird
		window.after(fps, movePipes) #move the pipes
		#check if overlapping if so stop the game
		#I've allowed a little overlapping due to irregural shape of the bird and difficulty of the game
		#also check if bird is out of screen
		birdCoords = [birdX - 40, birdY - 25, birdX + 40, birdY + 25]
		if(overLapping(birdCoords, canvas.coords(upPipes[0])) or overLapping(birdCoords, canvas.coords(upPipes[1])) or overLapping(birdCoords, canvas.coords(upPipes[2])) or overLapping(birdCoords, canvas.coords(downPipes[0])) or overLapping(birdCoords, canvas.coords(downPipes[1])) or overLapping(birdCoords, canvas.coords(downPipes[2])) or outOfScreen()):
			pause = True #stop the game
			gameOver() #display game over menu
		window.after(fps, flyDown) #recursion of a function so the game doesn't stop
	
#games is created after clicking play button
#function takes default values that can be overridden by save
def createGame(score_0 = 0, pipeSpeed_0 = -10, pipeHole_0 = 350):
	global pause
	global birdX
	global birdY
	global pipesX
	global pipesY
	global gravity
	global score
	global pipeSpeed
	global pipeHole

	#clear all the remaining pipes
	for i in range(len(upPipes)):
		canvas.delete(upPipes[i])
		canvas.delete(downPipes[i])
	upPipes.clear()
	downPipes.clear()

	gravity = 0 #sets starting velocity to 0
	#starting settings
	score = score_0
	pipeSpeed = pipeSpeed_0
	pipeHole = pipeHole_0
	birdX = 100 # X pos for Bird
	birdY = 200 # initial y pos for Bird
	pipesX = [600, 1100, 1600] #initial x coords for pipes
	pipesY = [] #random y coords for pipes
	for i in range(3):
		pipesY.append(random.randint(0,600))

	#pipe1
	upPipes.append(canvas.create_rectangle(pipesX[0], 0, pipesX[0] + 100, pipesY[0], fill="#009900", outline="green"))
	downPipes.append(canvas.create_rectangle(pipesX[0], pipesY[0] + pipeHole, pipesX[0] + 100, 900, fill="#009900", outline="green"))
	#pipe2
	upPipes.append(canvas.create_rectangle(pipesX[1], 0, pipesX[1] + 100, pipesY[1], fill="#009900", outline="green"))
	downPipes.append(canvas.create_rectangle(pipesX[1], pipesY[1] + pipeHole, pipesX[1] + 100, 900, fill="#009900", outline="green"))
	#pipe3
	upPipes.append(canvas.create_rectangle(pipesX[2], 0, pipesX[2] + 100, pipesY[2], fill="#009900", outline="green"))
	downPipes.append(canvas.create_rectangle(pipesX[2], pipesY[2] + pipeHole, pipesX[2] + 100, 900, fill="#009900", outline="green"))
	#adding presedence so score is above pipes
	canvas.tag_lower(upPipes[0])
	canvas.tag_lower(upPipes[1])
	canvas.tag_lower(upPipes[2])
	canvas.tag_lower(downPipes[0])
	canvas.tag_lower(downPipes[1])
	canvas.tag_lower(downPipes[2])

	canvas.itemconfig(scoreText, text=str(score)) #display the score
	canvas.itemconfig(endText, text="") #hide endText

	#destroy menu buttons
	playButton.destroy() 
	leaderBoardButton.destroy()
	loadGameButton.destroy()

	pause = False
	window.after(fps, flyDown) #start the game

#places all the buttons of the menu on canvas
def displayMenu():
	global playButton
	global leaderBoardButton
	global loadGameButton
	playButton = Button(canvas, image=playImage, width="115", height="65", command = createGame)
	playButton.place(x = width/2 - 130, y = height/2)
	leaderBoardButton = Button(canvas, image=leaderBoardImage, width="115", height="65", command = showLeaderboard)
	leaderBoardButton.place(x = width/2, y = height/2)
	loadGameButton = Button(canvas, text='LOAD', command=loadGame, width=10, height=3)
	loadGameButton.place(x = width/2 - 50, y=height/2+75)

#if bird hits something game will finish
def gameOver():
	global highScores
	global score
	global endText
	global playButton
	global bestInput
	global bestButton

	#check if the score qualifies for the leaderboard
	newBest = False
	for i in range(len(highScores)):
		if score > highScores[i]:
			newBest = True
			highScores.append(score)
			break
	#if so ask user to enter his name
	if newBest:
		canvas.itemconfig(endText, text="NEW BEST!") #endtext informs about new record
		bestInput = Entry(canvas, width = 10) #create input for name
		bestInput.place(x = width/2 - 100, y = 200, height=30)
		bestButton = Button(canvas, text='Enter your name', command=updateLeaderboard) #create submit button for updating leaderboard
		bestButton.place(x = width/2, y = 200, height=30)
	#if record not set display best record and the menu
	else:
		 canvas.itemconfig(endText, text="BEST OF ALL: " + str(highScores[0]))
		 displayMenu()
	score = 0

#takes user's input for cheat
def applyCheat():
	global pipeSpeed
	global pipeHole
	global bird
	cheat = cheatInput.get() #get the string with cheat
	cheatInput.delete(0, "end") #delete contents of input
	#cheat for slowing down the pipes
	if cheat == "slow":
		if pipeSpeed < -4:
			pipeSpeed = int(pipeSpeed/2)
	#cheat for making the holes bigger
	if cheat == "holyhole":
		pipeHole = 600
		#cheat for gareth sprite
	# if cheat == "supergareth":
	# 	canvas.itemconfig(bird, image=garethImage)
	#back to noraml sprite
	if cheat == "normal":
		canvas.itemconfig(bird, image=birdImage)

#allows the user to pause at any moment in the game
def pauseTheGame(event):
	global pause
	global cheatInput
	global cheatButton
	global saveButton
	#if game is on then display options 
	if not pause:
		pause = True
		#create cheat input
		cheatInput = Entry(canvas, width = 10,)
		cheatInput.place(x = width/2 - 100, y = 200, height=30)
		cheatButton = Button(canvas, text='APPLY CHEAT', command=applyCheat) 
		cheatButton.place(x = width/2, y = 200, height=30)
		#possibilty of saving the game and quiting
		saveButton = Button(canvas, text='SAVE & QUIT', command=saveGame, width=10, height=3)
		saveButton.place(x = width/2 - 50, y=250)
	#if game is paused then unpause
	else:
		pause = False
		#destroy all menu elements
		saveButton.destroy()
		cheatInput.destroy()
		cheatButton.destroy()
		flyDown() #continue the game

#allows user to see the leaderboard
lbShown = False
def showLeaderboard():
	global lbShown
	global highScores
	global bestPlayers
	global upPipes
	global downPipes
	global playButton
	global loadGameButton
	global lbArray
	if not lbShown:
		#hide elements all elements
		playButton.destroy()
		loadGameButton.destroy()
		canvas.itemconfig(endText, text="")
		canvas.itemconfig(scoreText, text="")
		for i in range(len(upPipes)):
			canvas.delete(upPipes[i])
			canvas.delete(downPipes[i])
		upPipes.clear()
		downPipes.clear()

		#display 5 highest recorded scores with users
		lbArray = []
		for i in range(5):
			lbArray.append(canvas.create_text(width/2, 50*(i+1), fill="white", font="Impact 30 bold", text= str(i + 1) + ". " + bestPlayers[i] + ": " + str(highScores[i])))
		lbShown = True #mark that leaderboard is shown
	else:
		#recreate menu elements
		playButton = Button(canvas, image=playImage, width="115", height="65", command = createGame)
		playButton.place(x = width/2 - 130, y = height/2)
		loadGameButton = Button(canvas, text='LOAD', command=loadGame, width=10, height=3)
		loadGameButton.place(x = width/2 - 50, y=height/2+75)
		lbShown = False #mark that leaderboard is closed
		#dclear leaderboard
		for i in range(5):
			canvas.delete(lbArray[i])
		lbArray.clear()

def sortLeaderboard():
	global highScores
	global bestPlayers

	#apply bubble sorting algorithm 
	n = len(highScores)
	swapped = True
	while swapped:
		swapped = False
		for i in range(n - 1):
			if highScores[i] > highScores[i+1]:
				highScores[i], highScores[i+1] = highScores[i+1], highScores[i]
				bestPlayers[i], bestPlayers[i+1] = bestPlayers[i+1], bestPlayers[i]
				swapped = True

	#reverse arrays
	highScores = highScores[::-1]
	bestPlayers = bestPlayers[::-1]
	#truncate if more than 5 scores
	highScores = highScores[0:5]
	bestPlayers = bestPlayers[0:5]
	#update the files with current values
	with open("scores.txt", "w") as f:
		scoresToStr = [str(i) for i in highScores]
		for i in range(len(highScores)):
			f.write(scoresToStr[i] + "\n")
	with open("bestPlayers.txt", "w") as f:
		for i in range(len(bestPlayers)):
			f.write(bestPlayers[i] + "\n")

#if new best score recorded
def updateLeaderboard():
	global bestPlayers
	global bestInput
	global bestButton
	global playButton

	bestPlayers.append(bestInput.get())
	#hide iput for name of the player
	bestInput.destroy()
	bestButton.destroy()

	sortLeaderboard()
	displayMenu() #go back to menu

#
biShown = False
def bossKey(event):
	global biShown
	global bossKeyButton
	global pause
	global cheatInput
	global cheatButton
	if not biShown:
		#display some random code to appear working
		bossKeyButton = Button(canvas, image = bossKeyImage, width=width, height=height, command = None)
		bossKeyButton.place(x = 0, y = 0)
		biShown = True
		#if boss key is pressed while playing stop the game
		if not pause:
			pauseTheGame(event)
			cheatInput.destroy()
			cheatButton.destroy()
			saveButton.destroy()
	#if user clicks b again image is gone
	else:
		bossKeyButton.destroy()
		biShown = False

def loadGame():
	global savedSpecs
	saveExists = True
	#save should be loaded only if there isn't any 0's in it
	for i in savedSpecs:
		if i == 0:
			saveExists = False
	if saveExists:
		#create game with saved values
		createGame(score_0 = savedSpecs[0], pipeSpeed_0 = savedSpecs[1], pipeHole_0 = savedSpecs[2])
		savedSpecs = [0,0,0] #clears the save
		with open("save.txt", "w") as f:
			f.write("0\n0\n0")
	else:
		#if there are 0's display that save doesn't exist
		loadGameButton.config(text="Save not found")

def saveGame():
	global score
	global pipeSpeed
	global pipeHole
	global window
	#save to specs txt file
	with open("save.txt", "w") as f:
		f.write(str(score) + "\n")
		f.write(str(pipeSpeed) + "\n")
		f.write(str(pipeHole) + "\n")
	window.destroy() #quit the game

#check for files and if they don't exist create them with default values
highScores = [0,0,0,0,0]
if os.path.isfile("scores.txt"):
	with open("scores.txt", "r") as f:
		scoresStr = f.read()
		temphighScores = scoresStr.split("\n")
		for i in range(5):
			highScores[i] = int(temphighScores[i])
else:
	with open("scores.txt", "w") as f:
		f.write("0\n0\n0\n0\n0")
		highScores = [0, 0, 0, 0, 0]

bestPlayers = ["nobody"]*5
if os.path.isfile("bestPlayers.txt"):
	with open("bestPlayers.txt", "r") as f:
		playersStr = f.read()
		tempbestPlayers = playersStr.split("\n")
		for i in range(5):
			bestPlayers[i] = tempbestPlayers[i]
else:
	with open("bestPlayers.txt", "w") as f:
		f.write("nobody\nnobody\nnobody\nnobody\nnobody")
		bestPlayers = ["nobody"]*5

savedSpecs = [0,0,0] #[score, pipeSpeed, pipeHole]
if os.path.isfile("save.txt"):
	with open("save.txt", "r") as f:
		specsStr = f.read()
		tempSpecs = specsStr.split("\n")
		for i in range(3):
			savedSpecs[i] = int(tempSpecs[i])
else:
	with open("save.txt", "w") as f:
		f.write("0\n0\n0")
		savedSpecs = [0, 0, 0]

sortLeaderboard() #make sure that leaderboard is sorted

fps = 20 #frame rate after which canvas will be updated
birdX = 100 # X pos for Bird
birdY = 200 # initial y pos for Bird
pause = True #variable used to stop the game

#INITIAL VALUES WHICH GET ASSIGNED IN METHODS
# pipesX = [1000, 1500, 2000] #x coords for pipes
# pipesY = [] #random y coords for pipes
# for i in range(3):
# 	pipesY.append(random.randint(0,600))
# pipeHole = 250 #height of the hole between pipes
# score = 0 
# highScore = 0
# gravity = 0 #not actual gravity but velocity updated each frame
# pipeSpeed = -10 #speed with which pipes move left


width = 600
height = 900
window = setWindowDimensions(width, height) #set dimensions of a window and center it
canvas = Canvas(window, bg="light blue", width=width, height=height) #create canvas on whole window

#create image of a bird
birdImage = PhotoImage(file="bird.png") #source: original flappy bird game
#garethImage = PhotoImage(file="gareth.png")
bird = canvas.create_image(birdX, birdY, image=birdImage)

playImage = PhotoImage(file="play.png")
leaderBoardImage = PhotoImage(file="leaderboard.png") #source: original flappy bird game
bossKeyImage = PhotoImage(file="bosskey.png") #source: original flappy bird game


upPipes = [] #holds objects of upper pipes
downPipes = [] #holds objects of down pipes
scoreText = canvas.create_text(width/2, 100, fill="white", font="Impact 100 bold", text="0") #diplays score in the middle
endText = canvas.create_text((width/2), 300, fill="white", font="Impact 75 bold", text="WELCOME")
canvas.tag_raise(scoreText)

displayMenu()

window.bind("<space>", flyUp) #bind space for flying up
window.bind("<Escape>", pauseTheGame) #bind escape for  pausing the game
window.bind("<b>", bossKey) #bind b for boss key
canvas.pack()

window.mainloop()