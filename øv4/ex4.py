import math as m
import random as r
from copy import copy
import sys

class Node():

	def __init__(self, attributes):
		self.attributes = attributes
		self.children = {}

	def addBranch(self, key, value):
		self.children[key] = value



	def getTree(self):
		if len(self.children) == 0:
			return "[" + str(self.attributes) + "]"
		else:
			temp = "[" + str(self.attributes) + " "
		for key, value in self.children.items():
			temp += self.children[key].getTree()
		return temp + "]"
		



def decision_tree_learning(examples, attributes, parent_examples, random):
	#if there are no more examples return the most common value of parent examples. 
	if not examples:
		return Node(plurality_value(parent_examples))
	#if test to see if the set is pure
	elif same_classification(examples):
		return Node(examples[0][-1])
	#if there are no further atributes to split on return the most common value
	elif not attributes:
		return Node(plurality_value(examples))
	else:
		#check to see if random importance or expected gain is used
		if random == False:
			a = importance(examples, attributes)
		else:
			position = r.randint(0,len(attributes)-1)
			a = attributes[position]
		#creates tree with atribute a in root node
		tree = Node(a)
		#splits examples and adds all the exsamples with same value on attribute to tree as branches
		for i in xrange(1,3):
			list = []
			for exs in examples:
				if str(exs[a]) == str(i):
					list.append(exs)
			new_attributes = copy(attributes)
			#removes attribute that has been used
			new_attributes.remove(a)
			subtree = decision_tree_learning(list, new_attributes, examples, random)
			tree.addBranch(i, subtree)
	return tree








#function for reading txt file with examples 
def read_file(name):
	list = []
	file = open(name, 'r')
	for line in file.readlines():
		list.append(line.rstrip("\n").split("\t"))
	return list



#check if all examples have same class
def same_classification(examples):
	classification = examples[0][-1]
	for n in examples:
		if n[-1]!=classification:
			return False
	return True
# used to return the most common value in data
def plurality_value(data):
	output1 = 0
	output2 = 0
	for i in range(len(data)):
		if data[-1] == '1':
			output1+=1
		else:
			output2+=1
	if output1>output2:
		return output1
	elif output2>output1:
		return output2
	else: 
		r.randint(1,2)




def ent(q):
	if q == 0.0 or q==1.0:
		return 0.0
	else:
		return -(q*m.log(q,2) + (1-q)*m.log(1-q,2))



def importance(examples, pos):
	entropy = []
	for po in pos:
		
		ones = 0.0
		twos = 0.0
		posOnes = 0.0
		posTwoes =0.0
		tp=0.0
		tn=0.0
		for list in examples:
			#adds up total positive and total negative
			if str(list[-1]) == "1":
				tp+=1
			else:
				tn+=1
			#adds up all examples with value 1	
			if str(list[po])== "1":
				ones += 1
				#adds up all examples with value 1 and classification 1
				if str(list[-1]) == "1":
					posOnes+=1
			#adds up all examples with value 2
			elif str(list[po])== "2":
				twos += 1
				#adds up all examples with value 2 and classification 2
				if str(list[-1]) == "1":
					posTwoes+=1
		#calculates attributes information gain	
		a = ent(tp/(tp+tn))
		b = (ones/(ones+twos))*ent(posOnes/ones)
		c = (twos/(ones+twos))*ent(posTwoes/twos)
		gain = a - b - c
		entropy.append(gain)
	maximum = -0.01
	index = None
	#finds and returns the atribute which has highest expected information gain
	for i in range(len(entropy)):
		if entropy[i] > maximum:
			index = i
			maximum = entropy[i]
	
	return pos[index]


#function that takes in examples and a decision tree and sees how correct the decision tree is. 
def treTest(examples, tree):
	correct = 0
	
	for exs in examples:
		root = tree
		while True:
			if root.children:
				root = root.children[int(exs[int(root.attributes)])]


			else:
				break
		
		if root.attributes==exs[-1]:
			correct+=1
	return correct






#print importance(read_file("training.txt"), range(6))
tree = decision_tree_learning(read_file("training.txt"), range(7), [], False)
print "tree Test for amount of correct out of 28: "
print treTest(read_file("test.txt"),tree)

#print tree.getTree()

#name = 'output.txt' 
#try:
#	file = open(name, 'w')
#	file.write(tree.getTree())
#	file.close
#except:
#	print ""
#tree = decision_tree_learning(read_file("training.txt"), range(7), [], True)
#print treTest(read_file("test.txt"),tree)



