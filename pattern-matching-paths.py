from __future__ import print_function
import sys
import collections

inputFile = open(sys.argv[1])
outputFile = sys.argv[2]

def readIn(delimiter):
	numPaths = int(inputFile.readline())
	paths = []
	for n in range(0, numPaths):
		item = inputFile.readline().strip()
		#remove slashes from both ends, if they exist
		if item[0] == '/':
			item = item[1:]
		if item[len(item) - 1] == '/':
			item = item[:len(item) - 1]
		item = item.split(delimiter)
		paths.append(item)
	return paths

def breakTies(matchesList):
	matchLength = len(matchesList[0])
	#Start at the end of the match and work backwards
	index = -1;
	#Stop after we look at all of the items in the match
	while -(index) <  matchLength:
		wildcardExists = False;
		for match in matchesList:
			if match[index] == "*":
				wildcardExists = True;
		if wildcardExists:
			for match in matchesList:
				if match[index] != '*':
					del matchesList[matchesList.index(match)]
		index = index - 1;

def findBestMatch(matchesList):
	#Make list that records the number of wildcards in each match.
	countWildcards = []
	for pattern in matchesList:
		count = 0
		for item in pattern:
			if item == "*":
				count = count + 1
		countWildcards.append(count)
	mostWildcards = max(countWildcards)
	minWildcards = min(countWildcards)
	#Delete the matches that have more wildcards than any other.
	while len(matchesList) > 1  and mostWildcards != minWildcards:
	 	index = countWildcards.index(mostWildcards)
	 	del countWildcards[index]
	 	del matchesList[index]
	 	#recalculate max and min
	 	mostWildcards = max(countWildcards)
	 	minWildcards = min(countWildcards)
	if len(matchesList) > 1:
		breakTies(matchesList)

def printResult(result):
	with open(outputFile, 'w') as f:
		for matchesList in result:
			for match in matchesList:
				match = ','.join(match)
				f.write(match + '\n')
				print(match)

def main():
	patterns = readIn(',')
	paths = readIn('/')
	result = []
	#Find patterns that match each path
	for path in paths:
		matchesList = []
		for pattern in patterns:
			if len(pattern) == len(path):
				#Check that each value in the pattern matches for path
				patternMatches = True;
				for index in range(0, len(path)):
					if not pattern[index] == '*':
						if not path[index] == pattern[index]:
							patternMatches = False;
				if patternMatches:
					matchesList.append(pattern)
		if len(matchesList) > 1:
			findBestMatch(matchesList)
		if len(matchesList) == 0:
			matchesList.append(["NO MATCH"])
		result.append(matchesList)
	printResult(result)	


main()

