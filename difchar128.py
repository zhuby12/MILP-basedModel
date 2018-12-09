from gurobipy import *
import string
conv = (
	 3, 1,-1,-1, 2, 3, 1,-1, 0,
	-3,-2,-1, 2, 1,-1,-2,-1, 7,
	-1,-1, 2,-1,-2, 2, 2,-1, 4,
	-1, 2, 0, 0, 2,-1, 2, 1, 0,
	 2, 3, 3, 2,-1,-1, 1,-1, 0,
	-1, 1, 0,-1,-1, 0,-1,-1, 4,
	-1,-1,-2,-2,-1,-2, 2,-1, 8,
	 2,-1,-1, 2, 0, 0, 2, 1, 0,
	 1,-1,-1,-1, 0,-1,-1, 0, 4,
	 1,-2, 0, 0, 2, 1, 2, 1, 0,
	-2,-1,-2,-1,-2, 2,-1, 2, 7,
	-1,-2, 0,-1, 2,-1,-1,-1, 5,
	 2, 1, 3, 2,-1,-1,-1, 1, 0,
	 3, 2, 0,-1, 3, 2,-1,-1, 0,
	 0, 3,-1,-1, 2, 3,-1, 3, 0,
	-1, 1,-3, 2,-1, 0,-3,-3, 8,
	 2,-1, 1, 1, 1,-1, 0, 2, 0,
	-2,-1, 2,-2,-1,-2,-1, 2, 7,
	 1,-1, 1, 0,-1, 1,-1, 0, 2,
	-1,-1, 1, 1, 0, 0, 0,-1, 2,
	-2, 2, 1, 2, 0, 0, 1, 1, 0,
	)
convpbl = (
	 1, 1, 0, 2, 3, 1, 2, 2,-5,-3,-5, 0,
	-1, 1, 0, 2,-1, 0,-3,-3, 5, 8, 5, 0,
	 2,-2,-5,-1,-1,-5,-1,-1, 9,11,14, 0,
	-1, 0, 1, 1, 1,-1, 1,-1, 1, 2, 1, 0,
	-1,-1, 0,-1, 1,-1, 1, 1, 0, 4, 2, 0,
	 1,-3, 2, 0, 4,-4,-4, 1,10, 6, 8, 0,
	-1, 1, 2,-1,-2,-2,-2, 4,-1, 3, 6, 0,
	-2, 1,-2,-3,-1,-2, 1,-4, 4, 8,12, 0,
	 1, 3, 3,-2,-1,-1, 3,-1,-4,-1, 4, 0,
	-2,-2, 3,-2,-3, 3, 3,-1,-3, 3, 7, 0,
	-2,-1,-1, 2, 0, 0,-2,-1, 5, 5, 5, 0,
	 1,-1,-1, 3,-3, 0, 1, 0, 1, 1, 4, 0,
	 1,-1, 0,-2, 1, 0,-2,-2, 5, 6, 5, 0,
	 4, 1,-1,-1, 3, 4, 1,-2, 1,-1, 0, 0,
	 0, 2, 1, 2, 0, 0, 1, 1,-4,-2,-2, 0,
	 0, 4,-1,-5, 2, 4,-1, 3,-5,-2, 4, 0,
	-5,-1,-3,-1,-3, 3,-1, 2, 3, 7,12, 0,
	 4,-1, 4, 2,-1, 1,-1, 2,-1,-2, 0, 0,
	 0, 0, 0, 0, 0, 0, 0, 0,-1,-1,-1, 1,
	)
P64 = (
	 0,17,34,51,48, 1,18,35,32,49, 2,19,16,33,50, 3,
	 4,21,38,55,52, 5,22,39,36,53, 6,23,20,37,54, 7,
	 8,25,42,59,56, 9,26,43,40,57,10,27,24,41,58,11,
	12,29,46,63,60,13,30,47,44,61,14,31,28,45,62,15)
P128 = (
	  0, 33, 66, 99, 96,  1, 34, 67, 64, 97,  2, 35, 32, 65, 98,  3,
	  4, 37, 70,103,100,  5, 38, 71, 68,101,  6, 39, 36, 69,102,  7,
	  8, 41, 74,107,104,  9, 42, 75, 72,105, 10, 43, 40, 73,106, 11,
	 12, 45, 78,111,108, 13, 46, 79, 76,109, 14, 47, 44, 77,110, 15,
	 16, 49, 82,115,112, 17, 50, 83, 80,113, 18, 51, 48, 81,114, 19,
	 20, 53, 86,119,116, 21, 54, 87, 84,117, 22, 55, 52, 85,118, 23,
	 24, 57, 90,123,120, 25, 58, 91, 88,121, 26, 59, 56, 89,122, 27,
	 28, 61, 94,127,124, 29, 62, 95, 92,125, 30, 63, 60, 93,126, 31
	)

ROUND = 7
act = (1, 2, 3, 5, 7, 10, 13, 17, 19)
FindList = []
def PrintOuter(FindList,BanList):
	opOuter = open("Outer.lp",'w+')
	opOuter.write("Minimize\n")
	buf = ''
	for i in range(0,ROUND):
		for j in range(0,32):
			buf = buf + "a" + str(i) + "_" + str(j)
			if i != ROUND-1 or j != 31:
				buf = buf + " + "
	opOuter.write(buf)
	opOuter.write('\n')
	opOuter.write("Subject to\n")
	buf = ''
	for i in range(0,ROUND):
		buf = ''
		for j in range(0,32):
			buf = ''
			for k in range(0,4):
				buf = buf +  "x" + str(i) + "_" + str(4*j+k)
				if k != 3:
					buf = buf + " + "
			buf = buf + " - a" + str(i) + "_" + str(j) + " >= 0\n"
			for k in range(0,4):
				buf = buf + "x" + str(i) + "_" + str(4*j+k) + " - a" + str(i) + "_" + str(j) + " <= 0\n"
			#
			'''
			for k in range(0,4):
				buf = buf + "4 x" + str(i) + "_" + str(4*j+k)
				if k != 3:
					buf = buf + " + "
			for k in range(0,4):
				buf = buf + " - x" + str(i+1) + "_" + str(P64[4*j+k])
			buf = buf + " >= 0\n"
			for k in range(0,4):
				buf = buf + "4 x" + str(i+1) + "_" + str(P64[4*j+k])
				if k != 3:
					buf = buf + " + "
			for k in range(0,4):
				buf = buf + " - x" + str(i) + "_" + str(4*j+k)
			buf = buf + " >= 0\n"
			'''
			#
			for k in range(0,21):
				for l in range(0,9):
					if conv[9*k+l] > 0:
						if l <= 3:
							buf = buf + " + " + str(conv[9*k+l]) + " x" + str(i) + "_" + str(4*j+3-l)
						if 4 <= l and l <= 7:
							buf = buf + " + " + str(conv[9*k+l]) + " x" + str(i+1) + "_" + str(P128[4*j+7-l])
						if l == 8:
							buf = buf + " >= -" + str(conv[9*k+l]) + "\n"
					if conv[9*k+l] < 0:
						if l <= 3:
							buf = buf + " - " + str(-conv[9*k+l]) + " x" + str(i) + "_" + str(4*j+3-l)
						if 4 <= l and l <= 7:
							buf = buf + " - " + str(-conv[9*k+l]) + " x" + str(i+1) + "_" + str(P128[4*j+7-l])
						if l == 8:
							buf = buf + " >= " + str(-conv[9*k+l]) + "\n"
					if conv[9*k+l] == 0:
						if l == 8:
							buf = buf + " >= " + str(conv[9*k+l]) + "\n"

			opOuter.write(buf)
				 
	buf = ''
	if len(FindList) == 0:
		for i in range(0,128):
			buf = buf + "x0_" + str(i)
			if i != 127:
				buf = buf + " + "
			if i == 127:
				buf = buf + " >= 1\n"
		for i in BanList:
			for j in range(0,len(i)):
				buf = buf + "a" + str(i[j][0]) + "_" + str(i[j][1])
				if j != len(i)-1:
					buf = buf + " + "
				else:
					buf = buf + " <= " + str(len(i)-1) + '\n'
	else:	
		fl = []
		for i in range(0,128):
			fl.append(i)
			if fl in FindList:
				print fl
				print "iii"
				buf = buf + "x0_" + str(i) + " = 1\n"
			else:
				buf = buf + "x0_" + str(i) + " = 0\n"
			fl.pop()
	opOuter.write(buf)
	'''
	buf = ''
	for i in range(0,ROUND):
		buf = ''
		for j in range(0,32):
			buf = buf + "a" + str(i) + "_" + str(j)
			if j != 31:
				buf = buf + " + "
			if j == 31:
				buf = buf + " <= 4\n"
		opOuter.write(buf)
	'''
	'''
	buf = ''
	for i in BanList:
		for j in range(0,len(i)):
			buf = buf + "a" + str(i[j][0]) + "_" + str(i[j][1])
			if j != len(i)-1:
				buf = buf + " + "
			else:
				buf = buf + " <= " + str(len(i)-1) + '\n'
	opOuter.write(buf)
	'''
	buf = ''
	for i in range(0,ROUND):
		for j in range(0,32):
			buf = buf + "a" + str(i) + "_" + str(j)
			if i != ROUND-1 or j != 31:
				buf = buf + " + "
			else:
				buf = buf + " >= "
	
	buf = buf + str(act[ROUND-1]) + "\n"
	
	opOuter.write(buf)

	opOuter.write("Binary\n")
	buf = ''
	for i in range(0,ROUND):
		buf = ''
		for j in range(0,32):
			buf = buf + "a" + str(i) + "_" + str(j) + "\n"
		opOuter.write(buf)
	for i in range(0,ROUND+1):
		buf = ''
		for j in range(0,128):
			buf = buf + "x" + str(i) + "_" + str(j) + "\n"
		opOuter.write(buf)
	opOuter.close()


def PrintInner(SolveList,ftl):
	opInner = open("Inner.lp","w+")
	opInner.write("Minimize\n")
	buf = ''
	
	for i in range(0,len(SolveList)):
		buf = buf + "1.415 z" + str(SolveList[i][0]) + "_" + str(SolveList[i][1]) + "_0 + 2 z" + str(SolveList[i][0]) + "_" + str(SolveList[i][1]) + "_1 + 3 z" + str(SolveList[i][0]) + "_" + str(SolveList[i][1]) + "_2"
		if i != len(SolveList)-1:
			buf = buf + " + "
		else:
			buf = buf + "\n"
	opInner.write(buf)
	opInner.write("Subject to\n")
	buf = ''
	for i in range(0,len(SolveList)):
		buf = ''
		
			
		for k in range(0,4):
			buf = buf + "4 x" + str(SolveList[i][0]) + "_" + str(4*SolveList[i][1]+k)
			if k != 3:
				buf = buf + " + "
		for k in range(0,4):
			buf = buf + " - y" + str(SolveList[i][0]) + "_" + str(4*SolveList[i][1]+k)
		buf = buf + " >= 0\n"

		for k in range(0,4):
			buf = buf + "4 y" + str(SolveList[i][0]) + "_" + str(4*SolveList[i][1]+k)
			if k != 3:
				buf = buf + " + "
		for k in range(0,4):
			buf = buf + " - x" + str(SolveList[i][0]) + "_" + str(4*SolveList[i][1]+k)
		buf = buf + " >= 0\n"
		opInner.write(buf)
	
		buf = ''
		for k in range(0,19):
			for l in range(0,12):
				if convpbl[12*k+l] > 0:
					if l <= 3:
						buf = buf + " + " + str(convpbl[12*k+l]) + " x" + str(SolveList[i][0]) + "_" + str(4*SolveList[i][1]+3-l)
					if 4 <= l and l <= 7:
						buf = buf + " + " + str(convpbl[12*k+l]) + " y" + str(SolveList[i][0]) + "_" + str(4*SolveList[i][1]+7-l)
					if 8 <=l and l <= 10:
						buf = buf + " + " + str(convpbl[12*k+l]) + " z" + str(SolveList[i][0]) + "_" + str(SolveList[i][1]) + "_" + str(l-8)
					if l == 11:	
						buf = buf + " >= -" + str(convpbl[12*k+l]) + "\n"
				if convpbl[12*k+l] < 0:
					if l <= 3:
						buf = buf + " - " + str(-convpbl[12*k+l]) + " x" + str(SolveList[i][0]) + "_" + str(4*SolveList[i][1]+3-l)
					if 4 <= l and l <= 7:
						buf = buf + " - " + str(-convpbl[12*k+l]) + " y" + str(SolveList[i][0]) + "_" + str(4*SolveList[i][1]+7-l)
					if 8 <= l and l <= 10:
						buf = buf + " - " + str(-convpbl[12*k+l]) + " z" + str(SolveList[i][0]) + "_" + str(SolveList[i][1]) + "_" + str(l-8)
					if l == 11:
						buf = buf + " >= " + str(-convpbl[12*k+l]) + "\n"
				if convpbl[12*k+l] == 0:
					if l == 11:
						buf = buf + " >= " + str(convpbl[12*k+l]) + "\n"

		opInner.write(buf)
	
	buf = ''
	sl = []
	for i in range(0,ROUND):
		buf = ''
		sl = []
		sl.append(i)
		for j in range(0,32):
			sl.append(j)

			if sl not in SolveList:
				for k in range(0,4):
					buf = buf + "x" + str(i) + "_" + str(4*j+k) + " = 0\n"
					buf = buf + "y" + str(i) + "_" + str(4*j+k) + " = 0\n"
			sl.pop()

		if i != ROUND:
			for j in range(0,128):
				buf = buf + "x" + str(i+1) + "_" + str(P128[j]) + " - y" + str(i) + "_" + str(j) + " = 0\n"
		opInner.write(buf)

	buf = ''
	
	buf = ''

	if len(ftl) == 0:
		for i in SolveList:
			if i[0] == 0:
				buf = buf + "x0_" + str(4*i[1]) + " + x0_" + str(4*i[1]+1) + " + x0_" + str(4*i[1]+2) + " + x0_" + str(4*i[1]+3)
				buf = buf + " >= 1\n"
		opInner.write(buf)
	else:
		fl = []

		for i in range(0,128):
			fl.append(i)
			if fl in ftl:
				print fl
				print "iii"
				buf = buf + "x0_" + str(i) + " = 1\n"
			else:
				buf = buf + "x0_" + str(i) + " = 0\n"
			fl.pop()
		opInner.write(buf)
	
	'''
	
	'''
	opInner.write("Binary\n")
	buf = ''
	for i in range(0,ROUND):
		buf = ''
		for j in range(0,128):
			buf = buf + "x" + str(i) + "_" + str(j) + "\n"
		for j in range(0,128):
			buf = buf + "y" + str(i) + "_" + str(j) + "\n"
		opInner.write(buf)
	buf = ''
	for j in range(0,128):
		buf = buf + "x" + str(ROUND) + "_" + str(j) + "\n"
	opInner.write(buf)
	buf = ''
	for i in range(0,len(SolveList)):
		buf = buf + "z" + str(SolveList[i][0]) + "_" + str(SolveList[i][1]) + "_0\n"
		buf = buf + "z" + str(SolveList[i][0]) + "_" + str(SolveList[i][1]) + "_1\n"
		buf = buf + "z" + str(SolveList[i][0]) + "_" + str(SolveList[i][1]) + "_2\n"
		opInner.write(buf)
		buf = ''
	opInner.close()

def strtoint(s):
	reg = 0
	s1 = ''
	s2 = ''
	res = 0
	result = []
	for i in range(0,len(s)):
		if s[i] == '_':
			reg = 1
		if s[i] >= '0' and s[i]<= '9':
			if reg == 0:
				s1 = s1 + s[i]
			if reg == 1:
				s2 = s2 + s[i]
		
	result.append(string.atoi(s1))
	result.append(string.atoi(s2))
	return result
def strtoint2(s):
	reg = 0
	s1 = ''
	s2 = ''
	res = 0
	result = []
	for i in range(0,len(s)):
		if s[i] == '_':
			reg = 1
		if s[i] >= '0' and s[i]<= '9':
			if reg == 0:
				s1 = s1 + s[i]
			if reg == 1:
				s2 = s2 + s[i]
		
	#result.append(string.atoi(s1))
	result.append(string.atoi(s2))
	return result

'''
PrintInner([[0,1],[1,8],[2,2],[3,0],[3,4]])
m = read("Inner.lp")
m.optimize()
for v in m.getVars():
	if v.x == 1:
		print v.x
		print v.VarName
obj = m.getObjective()
print obj.getValue()
'''
'''
BanList = []
bl = []
blstring = []
PrintOuter(BanList)
m = read("Outer.lp")
m.optimize()
#obj = m.getObjective()
#print obj.getValue()
#print m.getAttr('x')
#print m.getAttr('VarName')
for v in m.getVars():
	if v.x == 1 and v.VarName[0] == 'a':
		blstring.append(v.VarName)
for b in blstring:
	bl.append(strtoint(b))
BanList.append(bl)
bl = []
blstring = []
PrintOuter(BanList)
m = read("Outer.lp")
m.optimize()
for v in m.getVars():
	if v.x == 1 and v.VarName[0] == 'a':
		blstring.append(v.VarName)
for b in blstring:
	bl.append(strtoint(b))
BanList.append(bl)
print BanList
'''
count = 0
count1 = 0
FindSBoxList = []
fsl = []
fslstring = []
resreg = 128
FindTailList = []
ftl = []
ftlstring = []
BanList = []
bl = []
blstring = []
filename = "Result_" + str(ROUND) + ".txt"
opResult = open(filename,'w+')
while True:
	count = 0
	
	fsl = []
	fslstring = []
	ftl = []
	ftlstring = []
	bl = []
	opResult.write("*\n*\n*\n")
	while True:
		PrintOuter(ftl,BanList)
		count = count + 1
		
		if count == 15:
			break
		o = read("Outer.lp")
		o.optimize()
		obj = o.getObjective()
		
		if obj.getValue() < act[ROUND-1]+10:
			fsl = []
			fslstring = []
			for v in o.getVars():
				if v.x == 1 and v.VarName[0] == 'a':
					fslstring.append(v.VarName)
			for f in fslstring:
				fsl.append(strtoint(f))
			if count == 1:
				for f in fslstring:
					bl.append(strtoint(f))
				BanList.append(bl)
				print "*\n*\n*\n*\n"
				print BanList
				print "*\n*\n*\n*\n"
			
			print fsl
			PrintInner(fsl,ftl)
			ftl = []
			i = read("Inner.lp")
			i.optimize()
			if i.getObjective().getValue() > 78:
				break
			buf = ''
			buf = buf + str(fsl) + " " + str(i.getObjective().getValue()) + "\n"
			'''
			if i.getObjective().getValue() < 30:
				resreg = i.getObjective().getValue()
				ot = open("mini.txt","w+")
				ot.write(str(resreg))
				ot.close()
			'''
			ftlstring = []
			for v in i.getVars():
				if v.x == 1:
					buf = buf + v.VarName + " "
				if v.x == 1 and v.VarName[0] == 'x' and v.VarName[1] == str(ROUND-2):
					ftlstring.append(v.VarName)
			for f in ftlstring:
				ftl.append(strtoint2(f))

			print ftl
			print "well"
			buf = buf + "\n"
			opResult.write(buf)
			opResult.flush()

		else:
			break
			#count = count + 1
			#ftl = []
	
opResult.close()
#print len(BanList)
