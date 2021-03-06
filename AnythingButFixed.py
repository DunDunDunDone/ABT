# Anything but That
# version 0.83

'''
Update notes:
Alex is using git
Cleared update notes (#Sponsered)
'''

from tkinter import *
from turtle import *
import random
from Highscore_tools import *
from math import *
import ABTShapes
from time import time
import os
import sys

class player(Turtle):
    def __init__(self, weapons):
        Turtle.__init__(self)
        self.weapons = list(weapons)
        self.hotbarweapons = list(weapons)
        self.weapon = 0
        self.health = 1120
        self.charge = 0
        self.chargespeed = 1
        self.maxcharge = 5
        self.points = 1000000
        self.cap = 10 #Maximum number of bullets on the screen
        self.level = 0 #Number of bosses defeated; should start as 0
        self.debuffs = {'overheated': 0, 'freeze': 0, 'invisible': 0, 'ion': 0}#Overheated is similar to ion but does not dicolor the player
        self.bulletprice = {'blaster': 1, 'spreadshot': 3,
                            'lazor': 0, 'pewpew': 1,
                            'blaster_2.0': 1, 'freeze': 1,
                            'ion': 1, 'chain': 0, 'pentashot': 5,
                            'shotgun': 7, 'homing_missile': 1,
                            'bombs': 1, 'wave': 0} #This contains the amount of bullets used for each weapon
        self.heatprice = {'blaster': 40, 'spreadshot': 45,
                            'lazor': 30, 'pewpew': 10,
                            'blaster_2.0': 30, 'freeze': 40,
                            'ion': 40, 'chain': 20, 'pentashot': 25,
                            'shotgun': 50, 'homing_missile': 55,
                            'bombs': 40, 'wave': 20} #This contains the frames of cooldown used for each weapon
        self.up()
        self.pencolor((0, 255, 0))

    def spray(self, num, charge, damage, speed, spread = 10, regular = False):
        self.charge -= charge
        for i in range(num): #If the bullet cap is 2 more than the # of bullets, it will exceed that number i. e. 18+3 =21>20
            b = bullet(90, p.pos(), (0, 255, 0))
            bullets.append(b)
            b.damage = 1
            b.speed = 1.5
            b.moveToPos(self.pos())
            if regular:
                b.direction = 90 + (floor(num/2) - i)*regular
                b.seth(b.direction)
            else:
                b.direction = random.randint(90 - spread, 90 + spread)
                b.seth(b.direction)

    def fire(self):
        if self.debuffs['overheated'] <= 0 and len(bullets)+self.bulletprice[self.hotbarweapons[self.weapon]] <= self.cap and self.debuffs['ion'] <= 0:
            self.debuffs['overheated'] = self.heatprice[self.hotbarweapons[self.weapon]]
            if self.hotbarweapons[self.weapon] == 'blaster':
                b = bullet(90, self.pos(), (0, 255, 0))
                bullets.append(b)
                b.damage = 1
                b.speed = 1.5
                b.moveToPos(p.pos())
            elif self.hotbarweapons[self.weapon] == 'freeze' and self.charge >= 1:
                b = bullet(90, self.pos(), (0, 255, 0), debuffs = {'freeze':15})
                b.color((0, 255, 255))
                bullets.append(b)
                self.charge -= 1
                b.damage = 1
                b.speed = 1.5
                b.moveToPos(p.pos())
            elif self.hotbarweapons[self.weapon] == 'ion' and self.charge >= 1:
                b = bullet(90, self.pos(), (0, 255, 0), debuffs = {'ion':15})
                b.color((255, 255, 0))
                bullets.append(b)
                self.charge -= 1
                b.damage = 1
                b.speed = 1.5
                b.moveToPos(p.pos())
            elif self.hotbarweapons[self.weapon] == 'spreadshot' and self.charge >= 2:
                self.spray(3, 2, 1, 1.5)
            elif self.hotbarweapons[self.weapon] == 'lazor' and self.charge >= 3:
                self.charge -= 3
                self.lazorgo()
            elif self.hotbarweapons[self.weapon] == 'blaster_2.0' and self.charge >= 2:
                b = bullet(90, p.pos(), (0, 255, 0))
                bullets.append(b)
                self.charge -= 2
                b.damage = 2
                b.speed = 1
                b.moveToPos(p.pos())
            elif self.hotbarweapons[self.weapon] == 'homing_missile' and self.charge >= 2:
                b = bullet(90, p.pos(), (0, 255, 0), 1.5, 'homing')
                bullets.append(b)
                self.charge -= 2
                b.damage = 1
                b.moveToPos(p.pos())
                b.seth(90)
            elif self.hotbarweapons[self.weapon] == 'bombs' and self.charge >= 3:
                self.charge -= 3
                b = bullet(90, p.pos(), (0, 255, 0), 1.2, 'bomb')
                b.damage = 1
                bullets.append(b)
                b.moveToPos(p.pos())
                b.seth(90)
            elif self.hotbarweapons[self.weapon] == 'pentashot' and self.charge >= 3:
                self.spray(5, 3, 1, 2.5, regular = 40)
            elif self.hotbarweapons[self.weapon] == "shotgun" and self.charge >= 4:
                self.spray(7, 4, 1, 2, spread = 20)
            elif self.hotbarweapons[self.weapon] == "pewpew" and self.charge >= 1:
                self.charge -= 1
                b = bullet(90, p.pos(), (0, 255, 0), 2.8, 'bomb', 1/3)
                b.damage = 1/3
                b.radius = random.randint(5, 15)
                bullets.append(b)
                b.moveToPos(p.pos())
                b.seth(90)
            elif self.hotbarweapons[self.weapon] == "chain" and self.charge >= 4:
                self.charge -= 4
                x = elist+flist
                if fight:
                    x.append(boss)
                self.chaingo(x, (self.xcor(), self.ycor()))
            elif self.hotbarweapons[self.weapon] == "wave" and self.charge >= 3:
                self.charge -= 4
                self.wavego()
        updatecharge()
        return
    
    def move(self):
        if self.debuffs['invisible'] > 0:
            self.hideturtle()
            self.debuffs['invisible'] -= 0.25
        else:
            self.showturtle()
        if self.debuffs['ion'] > 0:
            self.pencolor((min(255, int(200*self.debuffs['ion'])), min(255, int(200*self.debuffs['ion'])), 0))
            self.debuffs['ion'] -= 0.25
        else:
            self.pencolor(0, 255, 0)
        if self.debuffs['overheated'] > 0:
            self.debuffs['overheated'] -= 1
        if self.debuffs['freeze'] <= 0:
            self.setx(self.xcor() + mov)
        else:
            self.debuffs['freeze'] -= 0.25
            self.fillcolor((0, min(255, int(200*self.debuffs['freeze'])), min(255, int(200*self.debuffs['freeze']))))
        if self.xcor() > 300:
            self.setx(-300)
        if self.xcor() < -300:
            self.setx(300)

    def takeDamage(self):
        pass

    def changeWeapon(self):
        self.weapon += 1
        self.weapon %= len(self.hotbarweapons)
        updatescoreboard()
    
    def buy(self, button, weapon, cost):
        if self.points >= cost:
            button.forget()
            self.cap += 3
            self.weapons.append(weapon)
            self.hotbarweapons.append(weapon)
            self.points -= cost

    def lightningbolt(self, pointa, pointb, drawer):
        r = objectdistance(pointa, pointb)
        drawer.up()
        drawer.goto(pointa)
        drawer.down()
        pointer = Turtle()
        pointer.hideturtle()
        pointer.up()
        pointer.goto(pointa)
        pointer.left(pointer.towards(pointb))
        for i in range(10):
            pointer.forward(r/10)
            pointer.right(90)
            x = random.randint(-10, 10)
            pointer.forward(x)
            drawer.goto(pointer.xcor(), pointer.ycor())
            pointer.backward(x)
            pointer.left(90)
        
        
        garbage.append(pointer)
        del pointer #Pretty sure this doesn't do anything

    def chaingo(self, hitable, place, drawer = 0):
        ion = False
        if drawer == 0:
            drawer = Turtle()
            drawer.width(4)
            drawer.pencolor(255, 255, 0)
            drawer.hideturtle()
            ion = True
        hitable = list(hitable)
        closest = 0
        c1osestd = float('inf')
        for thing in hitable:
            x = objectdistance(place, (thing.xcor(), thing.ycor()))
            if x < 100 and x < c1osestd:
                closest = thing
                c1osestd = x
        if closest != 0:
            hitable.remove(closest)
            self.lightningbolt(place, (closest.xcor(), closest.ycor()), drawer)
            self.chaingo(hitable, (closest.xcor(), closest.ycor()), drawer)
            if ion:
                closest.debuffs['ion'] += 15
            if closest in flist:
                if closest.takeDamage():
                    p.health -= random.randint(0, 1)
                p.points -= 1
            else:
                if closest.takeDamage():
                    p.health += random.randint(0, 1)
                p.points += 1
            updatescoreboard()
        else:
            screen.update()
            drawer.clear()
            garbage.append(drawer)
            del drawer #Pretty sure this doesn't do anything

    def wavego(self):
        for i in range(5): #Hits within a 500 radius
            e = explosion(self.pos(), 1.01, 1, (0, 255, 0), radius = 20*i) #Creates explosion objects
            

    def lazorgo(self):
        for e in elist+flist:#MAke collision using shapepoly
            if abs(e.xcor()-self.xcor()) < e.getWidth():
                if e.takeDamage():
                    p.health += random.randint(0, 1)
                p.points += 1
                updatescoreboard()
        if fight:
            sh = list(boss.get_shapepoly())
            for i in range(len(sh)):
                sh[i] = (sh[i][0] + boss.xcor(), sh[i][1] + boss.ycor())
            w = [boss.xcor(), boss.xcor()]
            for i in sh:
                if i[0] < w[0]:
                    w[0] = i[0]
                elif i[0] > w[1]:
                    w[1] = i[0]
            if w[0]-3 < self.xcor() < w[1]+3:
                boss.takeDamage(1)
                self.points += 1
                updatescoreboard()

        x = lazor(1.25, self, color = (0, 255, 0))
        return
            
class bullet(Turtle):
    def __init__(self, direction, pos, color = (255, 0, 0), sp = 1.5, btype = 'regular', explosion = 1, debuffs = {}):
        Turtle.__init__(self)
        self.movespeed = sp #How fast you are (higher is faster)
        self.damage = 0 #How much damage a bullet deals
        self.radius = 40 #Used for the bomb
        
        self.up()
        self.debuffs = debuffs
        self.btype = btype
        self.turtlesize(0.5, 0.5)
        self.goto(pos)
        self.color(color)
        self.direction = direction
        self.seth(self.direction)
        self.explosion = explosion

    def start(self):
        self.up()
        self.turtlesize(0.5, 0.5)
        self.goto(pos)
        self.color((0, 255, 0))
        self.seth(self.direction)

    def move(self, elist):
        if self.btype == 'homing': #Run homing missile code if this is a homing missile
            bestenemy = ''
            bestdistance = float('inf')
            for enemy in elist:
                x = sqrt((self.xcor()-enemy.xcor())**2+(self.ycor()-enemy.ycor())**2)
                if x<bestdistance:
                    bestdistance = x
                    bestenemy = enemy
            if bestenemy != '':
                x = self.heading()-90
                self.seth(x+(self.towards(bestenemy)-90>x)-(self.towards(bestenemy)-90<x)+90)
            self.forward(self.movespeed)
        elif self.btype == 'phoming':
            x = self.heading()-90
            self.seth(x+(self.towards(p)-90>x)-(self.towards(p)-90<x)+90)
            self.forward(self.movespeed)
        else:
            self.forward(self.movespeed)
        if self.ycor() < -300 or self.ycor() > 300: #Take yourself off the screen when you're off the screen
            self.delete()
        if self.xcor() < -300 or self.xcor() > 300:
            self.delete()

    def moveToPos(self, pos):
        self.goto(pos)

    def resetvars(self):
        self.direction = 90
        self.seth(self.direction)

    def collide(self):
        if self.btype == 'bomb': #Add piercing here
            t = explosion(self.pos(), 1.12, self.explosion, self.pencolor(), self.radius)
        self.delete()

    def delete(self):
        self.hideturtle()

class animation(Turtle):
    def __init__(self, stages = 4):
        Turtle.__init__(self)
        animations.append(self)
        self.stages = stages

    def changestate(self, stage):
        if stage < self.stages:
            self.next = lambda: self.changestate(stage+1, damagedenemies) #Modifies the next function
        else:
            self.hideturtle()
        
    def next(self):
        self.changestate(0)

class lazor(animation):
    def __init__(self, fade, firer, color = (255, 0, 0), stages = 6, direction = 90): #firer is who fired the lazor
        animation.__init__(self, stages)
        self.up()
        self.fade = fade
        self.mycolor = color
        self.color([int(x) for x in color])#Integizes the list
        self.shape('square') #This section needs to be generalized for all enemies. Currently this is hard-coded for the player
        self.goto(firer.xcor(), firer.ycor())
        self.seth(direction)
        self.forward(150)
        self.shapesize(0.08, 30, 1)

    def changestate(self, stage):
        if stage < self.stages:
            self.mycolor = (self.mycolor[0]/self.fade, self.mycolor[1]/self.fade, self.mycolor[2]/self.fade)
            self.color((int(self.mycolor[0]), int(self.mycolor[1]), int(self.mycolor[2])))
            self.next = lambda: self.changestate(stage+1) #Modifies the next function
        else:
            self.hideturtle()
        
class explosion(animation): #Fix to inherit correctly later
    def __init__(self, pos, fade, damage, color = (255, 0, 0), radius = 40):
        animation.__init__(self, radius)
        self.fade = fade
        self.up()
        self.goto(pos)
        self.pencolor([int(x) for x in color])#Integizes the list
        self.color = color
        self.radius = radius
        self.shape('Circle')
        self.btype = 'regular'
        self.damage = damage
        self.next()

    def changestate(self, radius, hitenemies = []): #Stage is the radius
        damagedenemies = list(hitenemies)
        self.shapesize(radius/10, outline = 4)#Maybe outline should decrease as the explosion gets bigger?
        for enemy in elist:
            if (not enemy in hitenemies) and sqrt(((enemy.xcor()-self.xcor())**2)+(enemy.ycor()-self.ycor())**2)<=radius:
                enemy.takeDamage(self.damage)
                damagedenemies.append(enemy)
        if radius < self.radius:
            self.color = (self.color[0]/self.fade, self.color[1]/self.fade, self.color[2]/self.fade)
            self.pencolor((int(self.color[0]), int(self.color[1]), int(self.color[2])))
            self.next = lambda: self.changestate(radius+2, damagedenemies) #Modifies the next function
        else:
            self.hideturtle()
            #garbage.append(self) #Explosion gets garbage-collected too fast. This causes hideturtle to fail 

    def next(self):
        self.changestate(1)
     
class enemy(Turtle):
    def __init__(self, level):
        Turtle.__init__(self)
        self.speed(0)
        self.pencolor(255, 0, 0)
        self.level = level
        if self.level == 5:
            self.shape('5enemy')
        elif self.level >= 6:
            self.shape('circle')
            self.flying = 150
        self.up()
        self.health = level
        if self.level < 5:
            self.turtlesize(self.health, self.health, 2)
        if self.level == 5:
            self.shape('5enemy')
            self.turtlesize(self.health, self.health, 2)
        elif 6 <= self.level <= 7:
            self.shape('circle')
            self.flying = 150
            self.turtlesize(1, 1, 2)
        self.right(90)
        self.goto(random.randint(-300, 300), 300)
        self.going = 1
        self.debuffs = {'freeze': 0, 'invisible': 0, 'ion': 0}
        elist.append(self)

    def move(self, p):
        if self.debuffs['ion'] > 0:
            self.pencolor((min(255, int(200*self.debuffs['ion'])), min(255, int(200*self.debuffs['ion'])), 0))
            self.debuffs['ion'] -= 0.25
        else:
            self.pencolor(255, 0, 0)
        if self.debuffs['freeze'] <= 0:
            self.forward(0.5)
            if self.ycor() < -300 or self.ycor() > 300:
                self.delete()
            if self.level == 5:
                self.shape('5enemy')
                self.setx(self.xcor() + self.going)
                if self.xcor() > 300:
                    self.setx(-300)
                if self.xcor() < -300:
                    self.setx(300)
            elif 6 <= self.level <= 7: # bat code
                if self.flying > 1:
                    a = self.towards(p)
                    if self.heading()-a>=0:
                        self.right(2)
                    else:
                        self.left(2)
                    self.flying -= 1
                elif self.flying == 1:
                    self.flying = -50
                elif self.flying == -1:
                    self.flying = 100
                elif self.flying < -1:
                    if 90<self.heading()<270:
                        self.right(2)
                    else:
                        self.left(2)
                    self.flying += 1
                self.forward(2)
            if not random.randint(0, 100):
                self.shoot()
        else:
            self.debuffs['freeze'] -= 0.25
            self.fillcolor((0, min(255, int(200*self.debuffs['freeze'])), min(255, int(200*self.debuffs['freeze']))))

    def getWidth(self):
        if self.level <= 5:
            return max(self.turtlesize()[0]*6-3, 0)
        if 6 <= self.level <= 7:
            return 20

    def shoot(self):
        if self.debuffs['ion'] <= 0:
            self.going = self.going * -1
            b = bullet(-90, self.pos(), (255, 0, 0))
            ebullets.append(b)
        return

    def takeDamage(self, damage = 1):
        self.health -= damage
        if self.health > 0:
            if self.level <= 5:
                self.turtlesize(ceil(self.health), ceil(self.health), 2)
            return False #You're alive
        else:
            self.delete() #Die if you're dead
            return True

    def delete(self):
        self.hideturtle()

class friendly(Turtle):
    def __init__(self):
        Turtle.__init__(self)
        self.speed(0)
        self.pencolor(0, 200, 0)
        self.up()
        self.health = 4
        self.turtlesize(self.health, self.health, 2)
        if random_event():
            self.goto(-300, random.randint(-200, 200))
        else:
            self.right(180)
            self.goto(300, random.randint(-200, 200))
        self.debuffs = {'freeze': 0, 'invisible': 0, 'ion': 0}
        flist.append(self)

    def move(self, p):
        if self.debuffs['ion'] > 0:
            self.pencolor((min(255, int(200*self.debuffs['ion'])), min(255, int(200*self.debuffs['ion'])), 0))
            self.debuffs['ion'] -= 0.25
        else:
            self.pencolor(0, 200, 0)
        if self.debuffs['freeze'] <= 0:
            self.forward(0.5)
            if self.ycor() < -300 or self.ycor() > 300:
                self.delete()
        else:
            self.debuffs['freeze'] -= 0.25
            self.fillcolor((0, min(255, int(200*self.debuffs['freeze'])), min(255, int(200*self.debuffs['freeze']))))
        if self.xcor() > 310 or self.xcor() < -310:
            self.delete()

    def takeDamage(self, damage = 1):
        self.health -= damage
        if self.health > 0:
            self.turtlesize(ceil(self.health), ceil(self.health), 2)
            return False #You're alive
        else:
            self.delete() #Die if you're dead
            return True

    def getWidth(self):
        return 3 #This needs to be the width

    def delete(self):
        self.hideturtle()

class Boss(Turtle):
    def __init__(self):
        Turtle.__init__(self)
        self.health = 0
        self.keeper = Turtle()
        self.debuffs = {'freeze': 0, 'invisible': 0, 'ion': 0}
        self.up()
    
    def showhealth(self):
        self.keeper.up()
        self.keeper.seth(0)
        self.keeper.fillcolor('red')
        self.keeper.hideturtle()
        self.keeper.goto(0, 300)
        self.keeper.down()
        self.keeper.begin_fill()
        self.keeper.forward(self.health/2)
        self.keeper.left(90)
        self.keeper.forward(10)
        self.keeper.left(90)
        self.keeper.forward(self.health)
        self.keeper.left(90)
        self.keeper.forward(10)
        self.keeper.left(90)
        self.keeper.forward(self.health/2)
        self.keeper.backward(self.health/2)
        self.keeper.left(90)
        self.keeper.end_fill()

    def takeDamage(self, damage = 1):
        self.keeper.clear()
        self.health -= damage
        self.keeper.begin_fill()
        self.keeper.forward(10)
        self.keeper.right(90)
        self.keeper.forward(self.health)
        self.keeper.right(90)
        self.keeper.forward(10)
        self.keeper.right(90)
        self.keeper.forward(self.health)
        self.keeper.right(90)
        self.keeper.end_fill()
        if self.health <= 0:
            self.delete()
                    
    def shoot(self, direction = -90, debuffs = {}, btype = 'regular'):
        b = bullet(direction, self.pos(), btype = btype, debuffs = debuffs)
        if 'freeze' in debuffs.keys():
            b.color((0, 255, 255))
        elif 'ion' in debuffs.keys():
            b.color((255, 255, 0))
        elif 'invisible' in debuffs.keys():
            b.color((150, 150, 150))
        ebullets.append(b)

    def spray(self, num, damage, speed, spread = 10, regular = False):
        for i in range(num): #If the bullet cap is 2 more than the # of bullets, it will exceed that number i. e. 18+3 =21>20
            b = bullet(-90, self.pos(), (255, 0, 0))
            ebullets.append(b)
            b.damage = 1
            b.speed = 1.5
            b.moveToPos(self.pos())
            if regular:
                b.direction = -90 + (floor(num/2) - i)*regular
                b.seth(b.direction)
            else:
                b.direction = random.randint(-90 - spread, -90 + spread)
                b.seth(b.direction)
            
    def burst(self, angle, number, spread):
        for i in range(number):
            b = bullet(angle, (self.xcor() + (spread-number/2)*i, self.ycor()), (255, 0, 0))
            ebullets.append(b)

    def fireenemy(self, minlevel, maxlevel, direction = -90):
        e = enemy(random.randint(minlevel, maxlevel))
        e.goto(self.pos())
        e.seth(direction)
        screen._turtles.append(e)

    def lazershot(self, start, direction):
        b = bullet(direction, start, (255, 0, 0))
        b.damage = 0
        b.down()
        b.width(3)
        if abs(p.xcor()-b.xcor()) < max(p.turtlesize()[0]*5, 0):
            p.health -= 1
            p.points += 1
            updatescoreboard()
                
        b.forward(600)
        screen.update()
        b.clear()
        b.collide()
        return

    def delete(self):
        for i in range(boss.points):
            p.points += 1
            updatescoreboard()
        for i in range(10):
            p.health += 1
            updatescoreboard()
        self.hideturtle()
        garbage.append(self)
        garbage.append(self.keeper)
        p.level += 1
        del self.keeper #Pretty sure this doesn't do anything

class boss1(Boss):
    def __init__(self):
        Boss.__init__(self)
        Turtle.__init__(self)
        self.up()
        self.seth(-90)
        self.turtlesize(20, 20, 2)
        self.n = 1
        self.pencolor((255, 0, 0))
        self.goto(0, 300)
        self.health = 200
        self.showhealth()
        self.points = 100
        for i in range(200):
            self.forward(1)
            screen.update()

    def move(self):
        self.setx(self.xcor() + self.n)
        if abs(self.xcor()) > 300:
            self.n *= -1

    def fire(self):
        if not random_event(p=0.01):
            self.fireenemy(1, 4)
        if not random_event(p=0.01):
            self.spray(5, 1, 2)

class boss2(Boss):
    def __init__(self):
        Boss.__init__(self)
        Turtle.__init__(self)
        self.up()
        self.seth(-90)
        self.turtlesize(5, 5, 2)
        self.pencolor((255, 0, 0))
        self.goto(0, 300)
        self.health = 99
        self.showhealth()
        self.points = 100
        self.spraying = 0
        self.alternate = 0
        for i in range(200):
            self.forward(1)
            screen.update()

    def move(self):
        self.setx(self.xcor() + 1)
        if self.xcor() > 300:
            self.setx(-300)

    def fire(self):
##        if abs(self.xcor()-self.spot) < 5:
##            if not random.randint(0, 100):
##                self.lazershot(self.pos(), -90)
##                self.spot = p.xcor()
        alimit = self.health/10
        slimit = 100-self.health/4
        if self.health > 195:
            if not random_event(p=0.005):
                self.shoot(direction = -90)
        else:
            if not random_event(p=0.006667) and not self.spraying:
                self.spraying = int(slimit)
            if self.spraying > 0:
                if not self.alternate:
                    self.spraying -= 1
                    if self.health > 100:
                        if random_event(p=0.5):
                            self.shoot(direction = random.randint(-30, 30)-90, debuffs = {'freeze':30})
                        else:
                            self.shoot(direction = random.randint(-30, 30)-90)
                    else:
                        if random_event(p=0.5):
                            self.shoot(direction = random.randint(-30, 30)-90, debuffs = {'freeze':30}, btype = 'phoming')
                        else:
                            self.shoot(direction = random.randint(-30, 30)-90, btype = 'phoming')
                self.alternate += 1
                if self.alternate >= alimit:
                    self.alternate = 0

class boss3(Boss):
    def __init__(self):
        Boss.__init__(self)
        Turtle.__init__(self)
        self.up()
        self.seth(-90)
        self.turtlesize(10, 20, 2)
        self.n = 1
        self.pencolor((255, 0, 0))
        self.goto(0, 300)
        self.health = 200
        self.showhealth()
        self.points = 100
        for i in range(200):
            self.forward(1)
            screen.update()

    def move(self):
        self.setx(self.xcor() + self.n)
        if abs(self.xcor()) > 300:
            self.n *= -1

    def fire(self):
        if not random_event(p=0.005):
            self.fireenemy(1, 4, self.towards(p.pos()) + random.randint(-20, 20))
        if not random_event(p=0.005):
            self.burst(self.towards(p.pos()), 10, 20)

class boss4(Boss):
    def __init__(self):
        Boss.__init__(self)
        Turtle.__init__(self)
        self.up()
        self.seth(-90)
        self.turtlesize(2, 2, 2)
        self.pencolor((255, 0, 0))
        self.shape('boss2')
        self.goto(0, 300)
        self.health = 200
        self.showhealth()
        self.points = 100
        self.spot = p.xcor()
        for i in range(200):
            self.forward(1)
            screen.update()

    def move(self):
        self.setx(self.xcor() + 3*((self.xcor()<self.spot) - (self.xcor()>self.spot)))

    def fire(self):
        if abs(self.xcor()-self.spot) < 5:
            if not random_event(p=0.01):
                self.lazershot(self.pos(), -90)
                self.spot = p.xcor()
            
def isColliding(x, y, turtle):
    '''Checks if x, y is inside the turtle'''
    t = radians(-(turtle.heading()+90))
    nx = ((x-turtle.xcor())*cos(t)-(y-turtle.ycor())*sin(t))
    ny = ((y-turtle.ycor())*cos(t)+(x-turtle.xcor())*sin(t))+turtle.shapesize()[2]
    sx, sy = turtle.shapesize()[0], turtle.shapesize()[1]#x stretch, y stretch
    if abs(sy*tan(radians(61))*nx/sx) <= ny and abs(sy*tan(radians(21))*nx/sx) + abs(7*sy) >= ny:
        return True
    return False

def movel():
    global mov
    mov = -2

def stopmovel():
    global mov
    if mov == -2:
        mov = 0

def mover():
    global mov
    mov = 2

def stopmover():
    global mov
    if mov == 2:
        mov = 0

def updatescoreboard():
    global scoreboard, score, hitpoints, battery, weaponl
    try:
        score.forget()
        hitpoints.forget()
        weaponl.forget()
        battery.forget()
        score = Label(scoreboard, text = 'points: ' + str(int(p.points)), font = ('Monaco', 16))
        score.pack()
        hitpoints = Label(scoreboard, text = 'health: ' + str(p.health), font = ('Monaco', 16))
        hitpoints.pack()
        weaponl = Label(scoreboard, text = 'weapon: ' + str(p.hotbarweapons[p.weapon]), font = ('Monaco', 16))
        weaponl.pack()
        battery = Label(scoreboard, text = 'charge: ' + str(int(p.charge)), font = ('Monaco', 16))
        battery.pack()
    except TclError:
        scoreboard = Tk()
        score = Label(scoreboard, text = 'points: ' + str(int(p.points)), font = ('Monaco', 16))
        score.pack()
        hitpoints = Label(scoreboard, text = 'health: ' + str(p.health), font = ('Monaco', 16))
        hitpoints.pack()
        weaponl = Label(scoreboard, text = 'weapon: ' + str(p.hotbarweapons[p.weapon]), font = ('Monaco', 16))
        weaponl.pack()
        battery = Label(scoreboard, text = 'charge: ' + str(int(p.charge)), font = ('Monaco', 16))
        battery.pack()

def updatecharge(): #Delete if this doesn't make things faster
    global scoreboard, score, hitpoints, battery, weaponl
    try:
        battery.forget()
        battery = Label(scoreboard, text = 'charge: ' + str(int(p.charge)), font = ('Monaco', 16))
        battery.pack()
    except TclError:
        scoreboard = Tk()
        score = Label(scoreboard, text = 'points: ' + str(p.points), font = ('Monaco', 16))
        score.pack()
        hitpoints = Label(scoreboard, text = 'health: ' + str(p.health), font = ('Monaco', 16))
        hitpoints.pack()
        weaponl = Label(scoreboard, text = 'weapon: ' + str(p.hotbarweapons[p.weapon]), font = ('Monaco', 16))
        weaponl.pack()
        battery = Label(scoreboard, text = 'charge: ' + str(int(p.charge)), font = ('Monaco', 16))
        battery.pack()

def shop(root):#k???
    global weapons
    c = Canvas(root)
    c.pack()
    root.title("turtle man's shop :D")
    rt = RawTurtle(c)
    bg = rt.getscreen()
    bg.bgcolor('black')
    bg.colormode(255)
    rt.shape('turtle')
    rt.turtlesize(3, 3, 2)
    rt.right(90)
    rt.pencolor(0, 255, 0)

    
    f = open("Weapons.txt").read().split('\n')
    for weapond in f:
        weapon = weapond.split()
        if weapon[0] not in p.weapons and weapon[1] in p.weapons and p.level >= int(weapon[2]):
            button = Button(root, text = ' '.join(weapon[4:]), command = lambda: 1+1)
            button.configure(command=lambda b=button, weapon=weapon[0], cost=int(weapon[3]): p.buy(b, weapon, cost)) #button, weapon, cost
            button.pack()
    chargeb = Button(root, text = 'max charge + 2 [self explanatory] (10 pts)', command = chargeboost)
    chargeb.pack()
    if p.level > 0:
        hb = Button(root, text = 'health + 1 [self explanatory] (20 pts)', command = healthboost)
        hb.pack()
    if p.level > 1:
        cb = Button(root, text = 'increase charge speed [self explanatory] (20 pts)', command = csboost)
        cb.pack()
    hb = Button(root, text = 'Change weapon loadout', command = loadout)
    hb.pack()

def changewaepons(weapons):
    global root
    newhotbarweapons = []
    for w in range(len(weapons)):
        if weapons[w].get():
            newhotbarweapons.append(p.weapons[w])
    if len(newhotbarweapons) == 0:
        newhotbarweapons.append(p.hotbarweapons[p.weapon])
    p.hotbarweapons = newhotbarweapons
    p.weapon = 0
    root.destroy()
    root = Tk()
    shop(root)
    updatescoreboard()

def loadout():
    global root
    root.destroy()
    root = Tk()

    weapons = []
    for w in p.weapons:
        var = IntVar(root)
        var.set(int(w in p.hotbarweapons))

        c = Checkbutton(root, text=w, variable=var)
        c.pack()
        weapons.append(var)

    back = Button(root, text = 'SAVE AND EXIT', command = lambda: changewaepons(weapons))
    back.pack()
        
        
def healthboost():
    global p
    if p.points >= 20:
        p.points -= 20
        p.health += 1
        updatescoreboard()
        
def chargeboost():
    global p
    if p.points >= 10:
        p.points -= 10
        p.maxcharge += 2
        updatescoreboard()

def csboost():
    global p
    if p.points >= 20:
        p.points -= 20
        p.chargespeed += 0.2
        updatescoreboard()
        
def garbage_collect(turtles):
    '''Takes in turtles and deletes them'''
    for b in turtles:
        turtles.remove(b)
        screen._turtles.remove(b)

def random_event(p=0.5):
    return random.random()<p

def start_tutorial():
    screen.onkey(lambda: speech(turtor, []), "e")
    screen.onkey(lambda: speech(turtor, []), "E")
    turtor = Turtle()
    turtor.up()
    turtor.seth(-90)
    turtor.shapesize(2)
    turtor.shape('turtle')
    turtor.pencolor((0, 255, 0))
    turtor.goto(20, 20)
    turtor.write('Hi there', font=("Ariel", 10, "normal"))
    turtor.goto(0, 0)
    screen.update()
    f = open("tutorial.txt").read().split(':::')
    speech(turtor, f)

def speech(turtor, words):
    if words != []:
        turtor.clear()
        turtor.goto(20, 20)
        turtor.write(words[0], font=("Ariel", 10, "normal"))
        turtor.goto(0, 0)
        screen.update()
        screen.onkeypress(lambda: speech(turtor, words[1:]), "space")
    else:
        turtor.hideturtle()
        turtor.clear()
        screen.onkeypress(p.fire, "space")
        bullets.append(turtor)
        while True: #Runs the game
            if not stopped:
                main()
            else:
                screen.update()

def objectdistance(pointa, pointb):
    return sqrt((pointa[0]-pointb[0])**2+(pointa[1]-pointb[1])**2)

def areLinesIntersecting(lin1, lin2):
    if lin1[0][0] == lin1[1][0]:
        pass
    if lin2[0][0] == lin2[1][0]:
        pass
    nx = ((x-turtle.xcor())*cos(t)-(y-turtle.ycor())*sin(t))
    ny = ((y-turtle.ycor())*cos(t)+(x-turtle.xcor())*sin(t))
                
def stop(): #This method is not used
    global stopped, root
    stopped = True
    screen.onkey(main, "e")
    screen.onkey(main, "E")
    root = Tk()
    shop(root)
                
def loop_iteration():
    '''Iterates once and returns whether you're done'''
    global cdistance
    p.move()
    cdistance += 1
    if p.charge < p.maxcharge and cdistance % 20 == 0:
        p.charge += p.chargespeed
        p.charge = min(p.charge, p.maxcharge)
        cdistance = 0
        updatecharge()
    if random_event(p=0.01) and not fight:
        x = enemy(random.randint(p.level+1, p.level+2))
    if p.level > 3 and random.randint(0, 200) == 100 and not fight:
        x = friendly()
    for i in range(len(elist)):
        try:
            e = elist[i]
            e.move(p) #p is Player
            if elist[i].ycor() < -300:
                e.delete()
        except IndexError:
            pass
    for i in range(len(flist)):
        try:
            f = flist[i]
            f.move(p) #p is Player
            if flist[i].ycor() < -300:
                f.delete()
        except IndexError:
            pass
                
    for b in bullets:
        b.move(elist)
        if type(b) == bullet: #This should be removed if nothing adds nonbullet things to bullet
            for e in elist:
                if (isColliding(b.xcor(), b.ycor(), e) and e.level <= 5) or\
                (objectdistance(e.pos(), b.pos()) <= 13 and 6 <= e.level <= 7):
                    if not e.takeDamage(b.damage):
                        for debuff in b.debuffs:
                            e.debuffs[debuff] += b.debuffs[debuff]
                    b.collide()
                    p.points += b.damage
                    updatescoreboard()
            for f in flist:
                if isColliding(b.xcor(), b.ycor(), f):
                    if not f.takeDamage(b.damage): #True if it dies
                        for debuff in b.debuffs:
                            f.debuffs[debuff] += b.debuffs[debuff]
                    b.collide()
                    p.points -= b.damage*2
                    updatescoreboard()

    for b in ebullets:
        b.move(elist)
        if isColliding(b.xcor(), b.ycor(), p):
            p.health -= 1
            for debuff in b.debuffs:
                p.debuffs[debuff] += b.debuffs[debuff]
            b.delete()
            updatescoreboard()
    if stopped:
        screen.onkey(main, "e")
        screen.onkey(main, "E")
        root = Tk()
        shop(root)
    if p.health < 1:
        print('you lose haha')
        print('points: ', round(p.points))
        print('distance: ', distance + 1000*kdistance)
        if round(p.points) > get_highscore('Anything_But_That'):
            change_highscore('Anything_But_That', round(p.points))
            print('NEW POINTS HIGH SCORE!!!!')
        if distance + 1000*kdistance > get_highscore('Anything_But_Thatd'):
            change_highscore('Anything_But_Thatd', distance + 1000*kdistance)
            print('NEW DISTANCE HIGH SCORE!!!!')
        print('highscore: ', get_highscore('Anything_But_That'))
        print('distance highscore: ', get_highscore('Anything_But_Thatd'))
        raise done 
    return False
                        
def boss_iteration():
    '''Only called when there's a boss. Does all boss related actions'''
    global distance, kdistance, fight, boss
    distance = 0
    boss.move()
    boss.fire()
    for b in bullets:
        if (boss.shape() == 'classic' and isColliding(b.xcor(), b.ycor(), boss)):
            if boss.health > 0:
                boss.takeDamage(b.damage)
                for debuff in b.debuffs:
                    boss.debuffs[debuff] += b.debuffs[debuff]
            else:
                garbage_collect(garbage)
                fight = False
                break
            b.collide()
            updatescoreboard()
        elif (boss.shape() != 'classic' and abs(b.xcor() - boss.xcor()) < boss.turtlesize()[0]*6):
            if boss.health > 0:
                for debuff in b.debuffs:
                    boss.debuffs[debuff] += b.debuffs[debuff]
                boss.takeDamage(b.damage)
            else:
                garbage_collect(garbage)
                fight = False
                break
            b.collide()
            updatescoreboard()

def main():
    '''Controls the whole program, garbage collection, update distance, add boss if necessary'''
    global distance, kdistance, root, stopped, fight
    stopped = False
    garbage_collect(garbage)
    for b in bullets:
        if not b.isvisible():
            garbage.append(b)
            bullets.remove(b)
    for b in ebullets:
        if not b.isvisible():
            garbage.append(b)
            ebullets.remove(b)
    for e in elist:
        if not e.isvisible():
            garbage.append(e)
            elist.remove(e)
    for f in flist:
        if not f.isvisible():
            garbage.append(f)
            flist.remove(f)
    for a in animations: 
        a.next() 
        if not a.isvisible(): 
            animations.remove(a) 
            garbage.append(a)
    distance += 1
    if distance % 1000 == 0:
        distance = 0
        kdistance += 1
        if kdistance % 10 == 0:
            fight = True
            global boss
            if kdistance == 10:
                boss = boss1()
            elif kdistance == 20:
                boss = boss2()
            elif kdistance == 30:
                boss = boss3()
            elif kdistance == 40:
                boss = boss4()
    loop_iteration()
    if fight:
        boss_iteration()
    if root != 0:
        try:
            root.destroy()
        except:
            pass
    screen.onkey(stop, "e")
    screen.onkey(stop, "E")
    screen.update()

colormode(255)

p = player(['blaster', 'bombs', 'chain'])
screen = p.getscreen()
screen.colormode(255)
screen.tracer(0)
canvas = screen.getcanvas()
ABTShapes.registerABTShapes(screen) #Raw turtle is created in this line
screen.bgcolor(0, 0, 0)
p.turtlesize(3, 4, 2)
p.left(90)
p.back(260)

bullets = [] #Holds the players bulletsd
ebullets = [] #Holds the enemy bullets
elist = [] #Holds all the enemies
flist = [] #Holds all the friendly's
garbage = [] #Holds all the garbage (stuff to be deleted)
animations = [] #Holds animations

mov = 0
distance = 0## 0
kdistance = 0## 0
cdistance = 0#This is the charge count
fight = False
stopped = False
scoreboard = Tk()
root = 0 #measured in grams
boss = 0

screen.listen()
screen.onkeypress(movel, "Left")
screen.onkey(stopmovel, "Left")
screen.onkeypress(mover, "Right")
screen.onkey(stopmover, "Right")
screen.onkey(p.changeWeapon, "w")
screen.onkey(p.changeWeapon, "W")
screen.onkeypress(p.fire, "space")
screen.title('Anything but That')

score = Label(scoreboard, text = 'points: ' + str(p.points), font = ('Monaco', 16))
score.pack()
hitpoints = Label(scoreboard, text = 'health: ' + str(p.health), font = ('Monaco', 16))
hitpoints.pack()
weaponl = Label(scoreboard, text = 'weapon: ' + str(p.weapons[p.weapon]), font = ('Monaco', 16))
weaponl.pack()
battery = Label(scoreboard, text = 'charge: ' + str(p.charge), font = ('Monaco', 16))
battery.pack()

start_tutorial()
