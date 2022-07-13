#!/usr/bin/python3

from tkinter import *
from tkinter import ttk
import random
import time
import threading
from pathlib import Path

life = 5
points = 0
wpm = 0
scores = []
startTime = time.time()
totalTime = 0
wordsList = []
inGameWords = []
step = 0.5
moveDelay = 20
threadSleepTime = 2
running = True
doOnce = True

main = Tk()

sv = StringVar()
lv = StringVar()
pv = StringVar()
wpmv = StringVar()
phigh = StringVar()
wpmhigh = StringVar()

main.title("Speed Typer")
main.geometry("700x900")
main.resizable(False,False)

c = Canvas(main, bg="white", height=800, width=440)
c.pack(side="left", padx=5, pady=5)

def makeText(word, x):
	wordID = c.create_text(x, 20, text=word, fill="black", font=('Arial', 15, 'bold'))
	inGameWords.append(wordID)
	
def moveWord():	
	global life
	global doOnce
	if(life <= 0 and doOnce):
		life = 0
		lv.set("Life: {}".format(life))
		doOnce = False
		clearCanvas()
	
	if(life > 0):
		global wpm
		global points
		global totalTime
		
		totalTime = time.time() - startTime
		wpm = round(points/(totalTime/60))
		wpmv.set("WPM: {}".format(wpm))
		
		for w in inGameWords:
			y = c.coords(w)[1]
			c.move(w, 0, step)
			
			if(y > 800):
				if(life > 0):
					life -= 3
					lv.set("Life: {}".format(life))
					
					if(life < 0):
						life = 0
						lv.set("Life: {}".format(life))
					
				c.delete(w)
				inGameWords.remove(w)
					
	c.after(moveDelay, moveWord)

def spawnWord():
	global life
	while(running):
		if(life > 0):
			x = random.randint(60,380)
			w = random.choices(wordsList)
			uw = [i.upper() for i in w]
			makeText(uw, x)
			time.sleep(threadSleepTime)
		
def checkText(var, index, mode):
	for w in inGameWords:
		if(e1.get().upper() == c.itemcget(w, 'text')):
			global life
			global points
			global step
			global threadSleepTime
			
			if(life < 5):
				life += 1
				lv.set("Life: {}".format(life))
				
			points += 1
			pv.set("Points: {}".format(points))
			
			step += 0.005
			threadSleepTime -= 0.01
			
			c.delete(w)
			inGameWords.remove(w)
			
			e1.delete(0, 'end')

def restartGame():
	global life
	global points
	global step
	global totalTime
	global startTime
	global threadSleepTime
	global sv
	global doOnce
	
	life = 5
	points = 0
	startTime = time.time()
	totalTime = 0
	wpm = 0
	step = 0.5
	threadSleepTime = 2
	
	c.delete('all')
	inGameWords.clear()
	
	wpmv.set("WPM: {}".format(wpm))
	pv.set("Points: {}".format(points))
	lv.set("Life: {}".format(life))
	sv.set("")
	doOnce = True
	
	loadGame()

def clearCanvas():
	c.delete('all')
	inGameWords.clear()
	
	global scores
	global phigh
	global wpmhigh
	if(points > int(scores[0])):
		saveGame()
		phigh.set("Points: {}".format(scores[0]))
		wpmhigh.set("WPM: {}".format(scores[1]))

def exitGame():
	global running
	running = False
	quit()

def saveGame():
	global points
	global wpm
	
	print(points)
	print(wpm)
	
	save = Path("save.dat")
	save.touch(exist_ok=True)
	
	save = open("save.dat", "w")
	save.write(str(points))
	save.write("\n")
	save.write(str(wpm))
	
	save.close()
	
def loadGame():
	load = Path("save.dat")
	
	load.touch(exist_ok=True)
	
	load = open("save.dat", "r")
	
	global scores
	scores = load.readlines()
	
	load.close()
	
	global phigh
	global wpmhigh
	
	if(len(scores) >= 1):
		phigh.set("Points: {}".format(scores[0]))
		wpmhigh.set("WPM: {}".format(scores[1]))
	else:
		save = open("save.dat", "w")
		save.write("0")
		save.write("\n")
		save.write("0")
		
		save.close()
		
		phigh.set("Points: {}".format(scores[0]))
		wpmhigh.set("WPM: {}".format(scores[1]))
	
	

wlist = open("wlist.txt", "r")
wordsList = wlist.read().strip().split(', ')

loadGame()

t1 = threading.Thread(target=spawnWord)
t1.start()

moveWord()

style = ttk.Style()
style.configure('TEntry', foreground='green')

sv.trace("w", checkText)
e1 = ttk.Entry(main, textvariable=sv, width=23, justify=CENTER, font=('courier', 24, 'bold'))
e1.place(x=5, y=860)
e1.focus_force()

lv.set("Life: {}".format(life))
pv.set("Points: {}".format(points))
wpmv.set("WPM: {}".format(wpm))

lifeLabel = Label(main, textvariable=lv, font=('courier', 15, 'bold')).place(x=470,y=50)
pointsLabel = Label(main, textvariable=pv, font=('courier', 15, 'bold')).place(x=470,y=70)
wpmLabel = Label(main, textvariable=wpmv, font=('courier', 15, 'bold')).place(x=470,y=90)

highScoreLabel = Label(main, text="Highscore:", font=('courier', 15, 'bold')).place(x=470,y=180)
pointsHighLabel = Label(main, textvariable=phigh, font=('courier', 15, 'bold')).place(x=470,y=200)
wpmHighLabel = Label(main, textvariable=wpmhigh, font=('courier', 15, 'bold')).place(x=470,y=220)

b1 = Button(main, text="Restart", width=15, command=restartGame).place(x=470,y=290)
b2 = Button(main, text="Exit", width=15, command=exitGame).place(x=470,y=340)

main.mainloop()
