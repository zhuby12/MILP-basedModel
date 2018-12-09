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

ROUND = 12
act = (1, 2, 3, 5, 7, 10, 13, 16, 18, 20, 22, 24, 26)
BanListlen = 0
def PrintOuter(BanList):
	opOuter = open("Outer.lp",'w+')
	opOuter.write("Minimize\n")
	buf = ''
	for i in range(0,ROUND):
		for j in range(0,16):
			buf = buf + "a" + str(i) + "_" + str(j)
			if i != ROUND-1 or j != 15:
				buf = buf + " + "
	opOuter.write(buf)
	opOuter.write('\n')
	opOuter.write("Subject to\n")
	buf = ''
	for i in range(0,ROUND):
		buf = ''
		for j in range(0,16):
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
							buf = buf + " + " + str(conv[9*k+l]) + " x" + str(i+1) + "_" + str(P64[4*j+7-l])
						if l == 8:
							buf = buf + " >= -" + str(conv[9*k+l]) + "\n"
					if conv[9*k+l] < 0:
						if l <= 3:
							buf = buf + " - " + str(-conv[9*k+l]) + " x" + str(i) + "_" + str(4*j+3-l)
						if 4 <= l and l <= 7:
							buf = buf + " - " + str(-conv[9*k+l]) + " x" + str(i+1) + "_" + str(P64[4*j+7-l])
						if l == 8:
							buf = buf + " >= " + str(-conv[9*k+l]) + "\n"
					if conv[9*k+l] == 0:
						if l == 8:
							buf = buf + " >= " + str(conv[9*k+l]) + "\n"

			opOuter.write(buf)
				 
	buf = ''
	for i in range(0,64):
		buf = buf + "x0_" + str(i)
		if i != 63:
			buf = buf + " + "
		if i == 63:
			buf = buf + " >= 1\n"
	opOuter.write(buf)
	buf = ''
	for i in range(0,ROUND):
		buf = ''
		for j in range(0,16):
			buf = buf + "a" + str(i) + "_" + str(j)
			if j != 15:
				buf = buf + " + "
			if j == 15:
				buf = buf + " <= 4\n"
		opOuter.write(buf)
	buf = ''
	for i in BanList:
		for j in range(0,len(i)):
			buf = buf + "a" + str(i[j][0]) + "_" + str(i[j][1])
			if j != len(i)-1:
				buf = buf + " + "
			else:
				buf = buf + " <= " + str(len(i)-1) + '\n'
	opOuter.write(buf)
	buf = ''
	for i in range(0,ROUND):
		for j in range(0,16):
			buf = buf + "a" + str(i) + "_" + str(j)
			if i != ROUND-1 or j != 15:
				buf = buf + " + "
			else:
				buf = buf + " >= "
	if act[ROUND-1] > BanListlen:
		buf = buf + str(act[ROUND-1]) + "\n"
	else:
		buf = buf + str(BanListlen) + "\n"
	opOuter.write(buf)

	opOuter.write("Binary\n")
	buf = ''
	for i in range(0,ROUND):
		buf = ''
		for j in range(0,16):
			buf = buf + "a" + str(i) + "_" + str(j) + "\n"
		opOuter.write(buf)
	for i in range(0,ROUND+1):
		buf = ''
		for j in range(0,64):
			buf = buf + "x" + str(i) + "_" + str(j) + "\n"
		opOuter.write(buf)
	opOuter.close()


def PrintInner(SolveList):
	opInner = open("Inner.lp","w+")
	opInner.write("Minimize\n")
	buf = ''
	sl = []
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
		for j in range(0,16):
			sl.append(j)

			if sl not in SolveList:
				for k in range(0,4):
					buf = buf + "x" + str(i) + "_" + str(4*j+k) + " = 0\n"
					buf = buf + "y" + str(i) + "_" + str(4*j+k) + " = 0\n"
			sl.pop()

		if i != ROUND-1:
			for j in range(0,64):
				buf = buf + "x" + str(i+1) + "_" + str(P64[j]) + " - y" + str(i) + "_" + str(j) + " = 0\n"
		opInner.write(buf)

	buf = ''
	for i in SolveList:
		if i[0] == 0:
			buf = buf + "x0_" + str(4*i[1]) + " + x0_" + str(4*i[1]+1) + " + x0_" + str(4*i[1]+2) + " + x0_" + str(4*i[1]+3)
			buf = buf + " >= 1\n"
	opInner.write(buf)
	buf = ''
	'''
	
	'''
	opInner.write("Binary\n")
	buf = ''
	for i in range(0,ROUND):
		buf = ''
		for j in range(0,64):
			buf = buf + "x" + str(i) + "_" + str(j) + "\n"
		for j in range(0,64):
			buf = buf + "y" + str(i) + "_" + str(j) + "\n"
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

def OuterChange():
	outeri = open("Outer.lp")
	outero = open("Outer_change.lp","w+")
	while True:
		line = outeri.readline()
		if not line:
			break;
		for key,value in a_dict.items():
			line = line.replace(key,value)
		outero.write(line)
	outeri.close()
	outero.close()

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

BanList = []
bl = []
blstring = []
resreg = 64
filename = "Result_" + str(ROUND) + "_1.txt"
opResult = open(filename,'w+')
while True:
	PrintOuter(BanList)
	
	o = read("Outer.lp")
	o.optimize()
	obj = o.getObjective()
	if obj.getValue() < act[ROUND-1]+5:
		bl = []
		blstring = []
		for v in o.getVars():
			if v.x == 1 and v.VarName[0] == 'a':
				blstring.append(v.VarName)
		for b in blstring:
			bl.append(strtoint(b))
		BanList.append(bl)
		BanListlen = len(bl)
		print bl
		PrintInner(bl)

		i = read("Inner.lp")
		i.optimize()
		buf = ''
		buf = buf + str(bl) + " " + str(i.getObjective().getValue()) + "\n"
		if i.getObjective().getValue() < resreg:
			resreg = i.getObjective().getValue()
			ot = open("mini.txt","w+")
			ot.write(str(resreg))
			ot.close()
		for v in i.getVars():
			if v.x == 1:
				buf = buf + v.VarName + " "
		buf = buf + "\n"
		opResult.write(buf)
		opResult.flush()
	else:
		break


#print len(BanList)
