#Natalie Carlson
#Linda Lee
#William de Schweinitz
#CSCE 405
#A2- TFB
#Due Thurs 10/3

import queue
from random import randint
from random import shuffle
import copy


def main():

	startingFunds = 100000
	#initial investment per stock
	invest = int(startingFunds / 10)
	
	#DJIA data
	stockEarn = {'MMM':(4.46, invest), 'AXP':(-.36, invest), 'AAPL':(6.47, invest), 'BA':(6.36, invest), 'CAT':(10.24, invest), 'CVX':(1.53, invest), 'CSCO':(4.25, invest), 'KO':(-1.43, invest), 'DIS':(-4.8, invest), 'DOW':(10.72, invest), 'XOM':(5.64, invest), 'GS':(4.28, invest), 'HD':(3.55, invest), 'IBM':(7.97, invest), 'INTC':(10.9, invest), 'JNJ':(-.06, invest), 'JPM':(10.24, invest), 'MCD':(-2.23, invest), 'MRK':(-4.13, invest),'MSFT':(1.62, invest), 'NKE':(10.58, invest), 'PFE':(3.25, invest), 'PG':(2.61, invest), 'TRV':(1.16, invest),'UTX':(7.54, invest), 'UNH':(-5.32, invest), 'VZ':(4.07, invest), 'V':(-2.62, invest), 'WMT':(5.07, invest),'WBA':(8.97, invest)}

	#Lists for testing.
	#stockList = ['MRK', 'HD', 'TRV', 'DIS', 'XOM', 'UTX', 'DOW', 'KO', 'INTC', 'MCD']
	#stockList = ['TRV', 'WMT', 'DOW', 'AAPL', 'JPM', 'INTC', 'WBA', 'BA', 'VZ', 'KO']
	#stockList = ['CSCO', 'PG', 'MSFT', 'JPM', 'DIS', 'CVX', 'INTC', 'UTX', 'GS', 'MRK']
	#stockList = ['UTX', 'IBM', 'AXP', 'BA', 'VZ', 'JNJ', 'GS', 'DOW', 'CSCO', 'CAT']
	stockList = ['DIS', 'PG', 'UTX', 'V', 'MMM', 'INTC', 'BA', 'TRV', 'VZ', 'GS']

#	stockList = []
#	selection = ""
#	
#	#Menu
#	print("                   DJIA Companies:\n")
#	print("MMM, AXP, AAPL, BA,  CAT,  CVX, CSCO, KO,  DIS, DOW\n")
#	print("XOM, GS,  HD,   IBM, INTC, JNJ, JPM,  MCD, MRK, MSFT\n")
#	print("NKE, PFE, PG,   TRV, UTX,  UNH, VZ,   V,   WMT, WBA\n")
#
#	#Stock selection
#	print("Enter 10 companies you would like to invest in from the list above.")
#	print("Invalid or duplicate entries will be prompted for new input.")
#	for i in range(1,11):
#		while selection not in stockEarn or selection in stockList: #verify selection is valid with no repeats
#			print(i,". ", end="")
#			selection = input()
#		stockList.append(selection)
#		i += 1

	#Create initial portfolio for TFB
	portfolio = {}
	for stock in stockList:
		portfolio[stock] = stockEarn[stock]
	
	root = Node(portfolio)
	
	
	#Hill Climb technique
	bestHistory = [] #Store bestInvestments from initial portfolio and nine random portfolios
	bestInvestment = hillClimb(root) #best node from initial portfolio
	bestHistory.append(bestInvestment)
	

	for i in range(1,10): #nine random portfolios
		newPortfolio = randRestart(portfolio, startingFunds)
		newRoot = Node(newPortfolio)
		investment = hillClimb(newRoot)
		bestHistory.append(investment)
		if investment.value > bestInvestment.value:
			bestInvestment = investment
		
	#result
	print("The best investment strategy for your portfolio is:")
	for key in bestInvestment.portfolio:
		print(key, bestInvestment.portfolio[key][1])
	
	
#	#Simulated annealing
#	schedule = "To Do: figure out what this is!!!!"	
#	bestInvestment = simAnn(root, schedule)


#This method caluclates the value of a given state
def getValue(portfolio):
	sumTotal = 0
	for key in portfolio:
		sumTotal += (portfolio[key][0]) * (portfolio[key][1]) # percentage gain(or loss) * investment
	return int(sumTotal)

#Node object
class Node:
	
	#Node variables
	def __init__(self, portfolio):
	
		self.portfolio = portfolio
		self.value = getValue(portfolio)
			

	#This method creates neighbors of current node
	def createNeighbors(self):
		neighborList = []
		for stock in self.portfolio:
			new_portfolio = {}
			ten_percent = int(self.portfolio[stock][1] * 0.1)
			if ten_percent < 10:
				ten_percent = self.portfolio[stock][1]
			new_portfolio[stock] = (self.portfolio[stock][0], self.portfolio[stock][1] - ten_percent)
			
			for i in self.portfolio:
				if i == stock: continue
				child_portfolio = copy.deepcopy(new_portfolio)
				child_portfolio[i] = (self.portfolio[i][0], self.portfolio[i][1] + ten_percent)

				for j in self.portfolio:
					if j != stock and j != i:
						child_portfolio[j] = self.portfolio[j]

				neighbor = Node(child_portfolio)
				neighborList.append(neighbor)
		
		
		return neighborList

		

# Hill Climb Technique
def hillClimb(root):
	
	current = root

	while True:
		# get list of neighbors
		neighborList = current.createNeighbors()

		#find best neighbor
		maximum = neighborList[0]
		
		
		for n in neighborList[1:]:
			if n.value > maximum.value:
				maximum = n

		if maximum.value <= current.value:
			return current
		current = maximum


# Simulated-Annealing Technique
def simAnn(root, schedule): #schedule = a mapping from time to "temperature"
	
	t = 1
	current = root
	
	rq = [] #random queue
	current.createNeighbors()
	for n in current.neighborList:
		if n not in rq:
			rq.append(n)
	
	while True:
		T = schedule#(t) #add after learning what schedule is!!!!
		if T == 0:
			return current
		rand = random.randint(0, len(rq)-1)
		nextNode = rq[random]
		E = nextNode.value - current.value
		if E > 0:
			current = nextNode
		else:
			current = nextNode #?? only with probabity e^E/T	
		t += 1

def randRestart(portfolio, availableFunds):
	total = 0
	randList = []
	for i in range(0,9): 
		randNum = randint(0, availableFunds) #generates a single investment amount equal to or less than available funds
		availableFunds = availableFunds - randNum #updates available funds
		randList.append(randNum) #add single investment amount
		total += randNum
	randList.append(availableFunds) #add remaining amount
	total += availableFunds
	shuffle(randList) #shuffle values
	
	
	new_portfolio = {}
	i = 0
	for key in portfolio:
		new_portfolio[key] = (portfolio[key][1],randList[i])
		i += 1

	return new_portfolio
	
	
main()	
