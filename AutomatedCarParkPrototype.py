from ParkingArea import *
from ParkingLane import *
from collections import OrderedDict
import uuid
import random
import time

def removeRandomSpace(area):
	if len(spaces) == 0:
		return
	spaceIndex = random.randint(0,len(spaces)-1)
	area.removeSpace(spaces[spaceIndex].ID)
	del spaces[spaceIndex]

def addRandomSpace(area):
	tempSpace = generateRandomSpace()
	if area.addParkingSpace(tempSpace):
		spaces.append(tempSpace)
		return True
	return False

def addNRandomSpaces(n, area):
	for i in xrange(n):
		addRandomSpace(area)

def generateRandomSpace():
	spaceDimensions = spaceSizes[random.randint(0,3)]
	return ParkingSpace(spaceDimensions[1], spaceDimensions[0])

def drawParkingArea(area):
	for lane in area.lanes:
		for i in xrange(lane.stallStacks[0].height):
			j = 0
			printString = ""
			lastItem = None
			for item in lane.stallStacks[0].layout:
				if item == 0:
					printString +=' '
				else:
					if lastItem != item:
						j+=1
					if (lane.stallStacks[0].height-i) <= lane._spaces[item].height:
						printString += chr(65+j%2)
					else:
						printString += ' '
				lastItem = item
			print printString

		for i in xrange(lane._roadWidth):
			print "="*lane._length
		
		for i in xrange(lane.stallStacks[1].height):
			j = 0
			printString = ""
			lastItem = None
			for item in lane.stallStacks[1].layout:
				if item == 0:
					printString +=' '
				else:
					if lastItem != item:
						j+=1
					if  i < lane._spaces[item].height:
						printString += chr(65+j%2)
					else:
						printString += ' '
				lastItem = item
			print printString
		print " "

def calculateEfficiency(area):
	totalNeededArea = 0
	for space in area.spaces:
		totalNeededArea += area.spaces[space].width*area.spaces[space].height
	
	totalUsedArea = 0
	for lane in area.lanes:
		for j in [0,1]:
			n = 0
			for index in lane.stallStacks[j].layout:
				if index != 0:
					n+=1
			totalUsedArea += lane.stallStacks[j].height*n
	

	print "Total Needed Area: " + str(totalNeededArea) + "m^2"
	
	print "Total Used Area:   " + str(totalUsedArea) + "m^2"

	print "Total Wasted Area: " + str(int(totalUsedArea-totalNeededArea)) + "m^2"

	efficiency = ""
	if totalUsedArea != 0:
		efficiency = float(totalNeededArea)/float(totalUsedArea)
		print "Efficiency:        " + str(efficiency)
	else:
		efficiency = float(1)
		print "Efficiency:        1"

	return efficiency

def simulateFull(area, timeDelay = 0.1, limit = 650):
	rejected = 0
	accepted = 0
	(accepted, rejected, efficiency, highestNoOfCars) = simulate(area, timeDelay, limit)
	simulateAllCarsLeaving(area, timeDelay, limit)
	print "No of accepted cars:            " + str(accepted)
	print "No of rejected cars:            " + str(rejected)
	print "Highest no of cars in car park: " + str(highestNoOfCars)
	print "Lowest efficiency:              " + str(efficiency)

def simulate(area, timeDelay = 0.1, limit = 650):
	rejected = 0
	accepted = 0
	lowestEfficiency = float(1)
	highestNoOfCars = 0
	for i in xrange(limit):
		x = float(float(i)/float(limit))
		prob = (-x**2+0.8*x+0.2)/0.4
		if (random.random() < prob):
			if(addRandomSpace(area)):
				accepted += 1
			else:
				rejected += 1
		if (random.random() < 1-prob):
			removeRandomSpace(area) 
		for j in xrange(200):
			print " "
		drawParkingArea(area)
		efficiency = calculateEfficiency(area)
		if efficiency < lowestEfficiency:
			lowestEfficiency = efficiency
		if highestNoOfCars < len(area.spaces):
			highestNoOfCars = len(area.spaces)
		print ""
		print "Simulating Car Park Day"
		print "Iteration:                       " + str(i)
		print "No of cars in car park:          " + str(len(area.spaces))
		print "No of rejected cars:             " + str(rejected)
		print str(x)
		print "Probability of vehicle arriving: " + str(prob)
		print "Probability of vehicle leaving:  " + str(1-prob)
		time.sleep(timeDelay)
	return (accepted, rejected, lowestEfficiency, highestNoOfCars)

def simulateAllCarsLeaving(area, timeDelay = 0.1, limit = 500):
	for i in xrange(len(spaces)):
		removeRandomSpace(area) 
		for j in xrange(1000):
			print " "
		drawParkingArea(area)
		calculateEfficiency(area)
		print ""
		print "Clearing Car Park"
		print "Iteration: " + str(i)
		time.sleep(timeDelay)
		
		

spaceSizes = [(2,3),(2,4),(3,4),(4,6)]
spaces = []

area = ParkingArea(100,100)

#addNRandomSpaces(700, area)
#drawParkingArea(area)
#calculateEfficiency(area)
#area.addParkingSpace(ParkingSpace(3,2))
#simulate(area, 0.1, 300)
simulateFull(area)


