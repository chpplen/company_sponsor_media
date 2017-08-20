from munkres import Munkres, print_matrix
import random
import copy
import numpy as np

def solve_assignment(costMatrix, isProfit):
	if isProfit:
		costMatrix = [[-i for i in row] for row in costMatrix]

	m = Munkres()
	opt_assignment = m.compute(costMatrix)
	
	print_matrix(costMatrix, msg='Lowest cost through this matrix:')

	# print(indexes)
	total = 0
	for row, column in opt_assignment:
		value = costMatrix[row][column]
		total += value
		print('(%d, %d) -> %d' % (row, column, value))
	print('total cost: %d' % total)
	return opt_assignment, total

def add_dummy(matrix):
	numrows = len(matrix) 
	numcols = len(matrix[0])
	if numcols < numrows:
		for row in matrix:
			for i in range(numcols, numrows):
				row.append(0)
	if numrows < numcols:
		for i in range(numrows, numcols): 
			matrix.append([0 for j in range(numcols)])
	return matrix

def modify_costMatrix(temp_costMatrix, all_assignment, c, s):
	k_index = len(all_assignment)
	company_wait_too_long = []
	sponsor_wait_too_long = []

	if k_index >= 2:
		company_all = [i for i in range(c)]
		sponsor_all = [i for i in range(s)]
		for i in range(k_index-2, k_index):	
			for row, column in all_assignment[i]:
				if row >= c or column >= s:
					continue
				if row in company_all:
					company_all.remove(row)
				if column in sponsor_all:
					sponsor_all.remove(column)
		company_wait_too_long = company_all
		sponsor_wait_too_long = sponsor_all
		print(company_wait_too_long)
		print(sponsor_wait_too_long)

	for row, column in all_assignment[-1]:
		if row < c and column < s:
			temp_costMatrix[row][column] = -1000

	for company in range(c):
		if company in company_wait_too_long:
			for i in range(s, c):
				temp_costMatrix[company][i] = -1000
		else:
			for i in range(s, c):
				temp_costMatrix[company][i] = 0
	for sponsor in range(s):
		if sponsor in sponsor_wait_too_long:
			for i in range(c, s):
				temp_costMatrix[i][sponsor] = -1000
		else:
			for i in range(c, s):
				temp_costMatrix[i][sponsor] = 0
	return temp_costMatrix

def assignment_represent(thisK_opt_assignment, c, s):
	if c > s:
		assignment_matrix = [[0]*s+['*']*(c-s) for i in range(c)]
	else:
		assignment_matrix = [[0]*s for i in range(c)] + [['*']*s for i in range(s-c)] 

	for row, column in thisK_opt_assignment:
		assignment_matrix[row][column] = 1

	return np.array(assignment_matrix)

def solve_schedule(c, s, k):

	all_assignment = []
	total_profit = 0


	I = [[random.randint(0,10) for j in range(s)] for i in range(c)]
	M = [[random.randint(0,10) for j in range(s)] for i in range(c)]
	costMatrix = [[I[i][j]+M[i][j] for j in range(s)] for i in range(c)]
	costMatrix = add_dummy(costMatrix)
	# print(I)
	# print(M)
	# print(costMatrix)
	temp_costMatrix = copy.deepcopy(costMatrix)
	

	for i in range(k):		
		# print(costMatrix)
		print('-'*80)
		print('k: '+str(i+1))
		thisK_opt_assignment, thisK_total = solve_assignment(temp_costMatrix, True)

		all_assignment.append(thisK_opt_assignment)
		total_profit += thisK_total

		temp_costMatrix = modify_costMatrix(temp_costMatrix, all_assignment, c, s)

	print('-'*80)
	print('cost(-profit) matrix:')
	print(np.array(costMatrix))
	for index, thisK_opt_assignment in enumerate(all_assignment):
		print('k: ' + str(index+1))
		assignment_matrix = assignment_represent(thisK_opt_assignment, c, s)
		print(assignment_matrix)
	print('total profit: %d' % (total_profit))

c = 16
s = 11
k = 4
solve_schedule(c, s, k)

