import uuid
import random
import time

class ParkingLane:
	def __init__(self, length, position = 0, roadWidth = 3, initialStackHeight = 0):
		self._length = length
		self._roadWidth = roadWidth
		self._position = position
		self._spaces = {} # Space.ID -> Space
		
		self.stallStacks = (StallStack(length), StallStack(length))


	"""
	space	ParkingSpace to add
	RETURNS	True if space was added, False otherwise
	"""
	def addParkingSpace(self, space, exactHeight = True, zeroHeight = True, anyHeight = True):
		# Call _addParkingSpace on each Stall Stack
		success = False
# Check exact height
		if exactHeight:
			for i in [0,1]:
				if self.stallStacks[i].height == space.height: 
					success = self.stallStacks[i].addParkingSpace(space)
					if (success):
						space.stallStack = i
						self._spaces[space.ID] = space
						return True

# Check zero height (if couldn't find exact height, or not looking for exact height)
		if zeroHeight:
			for i in [0,1]:
				# If a stall stack has height 0, make it the correct height
				if self.stallStacks[i].height == 0: 
					self.stallStacks[i].height = space.height
					success = self.stallStacks[i].addParkingSpace(space)
				if (success):
					space.stallStack = i
					self._spaces[space.ID] = space
					return True

# Check any height in ascending order of height (if couldn't find space previously, or not looking for any previous things)
		if anyHeight:
			order = []
			if self.stallStacks[0].height > self.stallStacks[1].height:
				order = [1,0]
			else: 
				order = [0,1]

			for i in order:
				# Check for any gap
				success = self.stallStacks[i].addParkingSpace(space)
				if (success):
					space.stallStack = i
					self._spaces[space.ID] = space
					return True
		return False
		# return true if parking space was added, false otherwise

	def removeSpace(self, ID):
		stallStackIndex = self._spaces[ID].stallStack
		self.stallStacks[stallStackIndex].removeSpace(self._spaces[ID])
		del self._spaces[ID]

	def totalHeight(self):
		return self._roadWidth + self.stallStacks[0].height + self.stallStacks[1].height
	
	def __str__(self):
		return "Height=" + str(self.stallStacks[0].height) + ": " + str(self.stallStacks[0].layout) + '\n' + "ROAD\n" + "Height=" + str(self.stallStacks[1].height) + ": " + str(self.stallStacks[1].layout) + '\n'



class StallStack:
	def __init__(self, length):
		self.layout = [0 for i in xrange(length)]
		self.height = 0
		self.standardSize = []

	def addParkingSpace(self, space):
		# Check the corresponding lane to see if height can fit it in
		if (self.height < space.height):
			return False
		checkFromLeft = False
		if self.standardSize == []:
			self.standardSize = [space.height, space.width]
			checkFromLeft = True
		elif self.standardSize[0] == space.height and self.standardSize[1] == space.width:
			checkFromLeft = True
				

		# Otherwise
		#Iterate through StallStackLayout for chosen stall stack and find an empty element
		position = -1
		if not checkFromLeft:
			for i in xrange(len(self.layout)-1,-1,-1):
				if self.layout[i] == 0:
					if (i - space.width+1 < 0):
						return False
					fail = False
					for j in range(i, i - space.width,-1):
						if (self.layout[j] != 0):
							i -= space.width
							fail = True
							break
					if not fail:
						position = i
						break
		else:
			for i in xrange(len(self.layout)-1):
				if self.layout[i] == 0:
					if (i + space.width-1 >= len(self.layout)):
						return False
					fail = False
					for j in range(i,i + space.width):
						if (self.layout[j] != 0):
							i += space.width
							fail = True
							break
					if not fail:
						position = i
						break
		
		#COuldn't find suitable gap, so return false
		if (position == -1):
			return False

#If a position is returned:		
#Set the elements of the stall stack from position to (position+width) to uuid of parking space
		if checkFromLeft:
			for i in range(position, position+space.width):
				self.layout[i] = space.ID
		else:
			for i in range(position, position-space.width, -1):
				self.layout[i] = space.ID
		if (checkFromLeft):
			space.position = position
		else:
			space.position = position-space.width+1

		return True

	def removeSpace(self, space):
		ID = space.ID
		position = space.position
		for i in range(position, position + space.width):
			if self.layout[i] == ID:
				self.layout[i] = 0



class ParkingSpace:
	def __init__(self, height, width):
		self.ID = uuid.uuid4()
		self.height = height
		self.width = width
		self.position = None
		self.stallStack = None
		self.lane = None
		

	def setStallStackStackAndPosition(self, stallStack, position):
		self.position = position
		self.stallStack = stallStack


