from ParkingLane import *
from collections import OrderedDict
import uuid
import random
import time

class ParkingArea:
	def __init__(self, height, width):
		self.height = height
		self.width = width
		self.lanes = []
		self.stallStackHeights = {}
		self.spaces = {}
		self.laneLimit = 3

	def addNewLane(self, initialStackHeight = 0):
		if len(self.lanes) < self.laneLimit:
			tempLane = ParkingLane(self.width)
			self.lanes.append(tempLane)
			return True
		else:
			return False

	def addParkingSpace(self, space):
		# if no parking lanes, add one
		if self.lanes == []:
			self.addNewLane()
		# iterate through all parking lanes, checking heights, and get all available lanes which have the correct height of stall stack
		self._updateHeightsAvailable()
#### Check exact height ####
		if space.height in self.stallStackHeights:
			laneNos = []
			laneNos = self.stallStackHeights[space.height]
			# Try to add to all selected lanes
			for i in laneNos:
				if (self.lanes[i].addParkingSpace(space, True, False, False)):
					space.lane = i
					self.spaces[space.ID] = space
					return True
#### Check empty stacks ####
		if 0 in self.stallStackHeights:
			laneNos = []
			#No stacks of the exact right height
			#get all empty stacks
			laneNos = self.stallStackHeights[0]
			# Try to add to all selected lanes
			for i in laneNos:
				if (self.lanes[i].addParkingSpace(space, False, True, False)):
					space.lane = i
					self.spaces[space.ID] = space
					return True		
#### Add New Lane ####
		# parking space couldn't be added to any these lanes, so create a new lane if possible
		if self.addNewLane():
			if (self.lanes[len(self.lanes)-1].addParkingSpace(space)):
				space.lane = len(self.lanes)-1
				self.spaces[space.ID] = space
				return True

#### Find gaps in not-exact fit lanes ####
		#No empty stacks which could have spaces added
		#find all heights over the required height, and sort lowest to highest
		heights = []
		for key in self.stallStackHeights:
			if key > space.height:
				heights.append(key)
		heights.sort()
		laneNos = []
		for h in heights:
			laneNos.extend(self.stallStackHeights[h])
		laneNos = list(OrderedDict.fromkeys(laneNos))
		# Try to add to all selected lanes
		for i in laneNos:
			if (self.lanes[i].addParkingSpace(space)):
				space.lane = i
				self.spaces[space.ID] = space
				return True

		return False

	def removeSpace(self, spaceID):
		self.lanes[self.spaces[spaceID].lane].removeSpace(spaceID)
		if len(self.lanes[self.spaces[spaceID].lane]._spaces) == 0 and len(self.lanes)-1 == self.spaces[spaceID].lane:
			del self.lanes[self.spaces[spaceID].lane]
		del self.spaces[spaceID]

	def _updateHeightsAvailable(self):
		self.stallStackHeights = {}
		for i in xrange(len(self.lanes)):
			for j in [0,1]:
				h = self.lanes[i].stallStacks[j].height
				if h in self.stallStackHeights:
					self.stallStackHeights[h].append(i)
				else:
					self.stallStackHeights[h] = [i]
					
	def __str__(self):
		printString = ""
		for lane in self.lanes:
			printString += str(lane) + '\n'
		return printString


