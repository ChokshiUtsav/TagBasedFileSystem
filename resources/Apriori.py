#!/usr/bin/python

import math
import itertools
import sys
import pickle

# find input output parameters


f=open('config.csv','r+')
conf=f.read()
f.close()
global confidence

#contains row to itemset mappings
item_sets={}

lines=conf.split('\n')

for line in lines:
	token=line.split(',')
	if token[0]=="input":
		inp=token[1]
	if token[0]=="output":
		out=token[1]
	if token[0]=="flag":
		flag=token[1]
	if token[0]=="support":
		support=float(token[1])
	if token[0]=="confidence":
		confidence=float(token[1])

print inp,out,flag,support,confidence


# Read input file and tokenize find count

tx=0
hash={}
i=0


with open(inp) as f:
    for line in f:
    	l = line.split('\n')
    	token = l[0].split(',')
    	for item in token:
    		t=tuple()
    		t=t+(item,)
    		if t not in hash:
    			hash[t]=set()
    		hash[t].add(i)
    	i=i+1
    	tx=tx+1

#print hash


sup_tx=	int(math.ceil(tx*support))
print "Total transactions = " , tx , " tx"
print "Minimum Support Required = " , sup_tx , " tx"

for key in hash:
	if(len(hash[key])>=sup_tx):
		item_sets[key]=hash[key]


#Methods are defined in this space because they need access to minimum support and item-sets which are global
#------------------------------------------------------------------------------------------------------------------------

def count_opt(l1,cnt): #l1- : contains list size : contao  		
	i=0
	rows=set()
	cnt=0
	temp=set()
	for elem in l1:
		t=tuple()
		t=t+(elem,)
		if(len(temp)==0):
			temp=item_sets[t]
		else:
			temp=temp&item_sets[t]
	cnt=len(temp)
	if(cnt>=sup_tx):
		item_sets[l1]=temp
	return cnt



def combine(l1,size):
	new_list={}  #contains keys which are list and sorted of length size
	i=0
	j=0
	while i<len(l1):
		j=i+1
		while j<len(l1):
			merge_list = tuple(sorted((set(l1[i]+l1[j]))))
			#print merge_list
			if len(merge_list)==size:
				if merge_list not in new_list:
					new_list[merge_list]=0
			j=j+1
		i=i+1


	return sorted(new_list.keys())



def find_rules(l1,size):
	map_rules={}
	i=0
	j=0
	while i < len(l1):
		j=i+1
		while j < len(l1):
			
			if(len(l1[i])+len(l1[j])==size):
				if set(l1[i]).isdisjoint(set(l1[j])):
					if l1[i] not in map_rules:
						map_rules[l1[i]]=l1[j]
					if l1[j] not in map_rules:
						map_rules[l1[j]]=l1[i]
					
			j=j+1
		i=i+1


	# for key in sorted(map_rules.keys()):
	# 	print key,"->",map_rules[key]

	return map_rules


def test_association_opt(l1,l2):

	cnt1=0
	cnt2=0
	cnt1 = len(item_sets[l1])
	cnt2 = len(item_sets[l1]&item_sets[l2])

	#print l1,"->",l2,float(cnt2)/float(cnt1)
	if(cnt1==0):
		return False

	if float(cnt2)/float(cnt1) >=confidence:
		return True
	else:
		return False

#------------------------------------------------------------------------------------------------------------------------





qual_list=tuple(sorted(item_sets.keys()))

# contains all candidates that are greater than min_sup
final_qualifiers=[]

for item in qual_list:
		final_qualifiers.append(item)
cnt=2

list1=tuple(combine(qual_list,cnt))   # new candidates for size=cnt by combining item-sets


while True:
	qual_list=[]
	
	for item in list1:   #these are the pairs
		if(count_opt(item,cnt)>=sup_tx):
			qual_list.append(item)

	
	qual_list.sort()
	#print "qualifiers ",qual_list


	if len(qual_list) == 0:   # if no qualifiers found break out of loop
		break

	#if cnt !=1:
	for item in qual_list:
		final_qualifiers.append(item)	# append into final qualifiers


	cnt=cnt+1
	list2=tuple(combine(tuple(qual_list),cnt))   # new candidates for size=cnt by combining item-sets
	list1=[]

    # we will prune the unnecessary itemsets here
	if(cnt>2):
		qual_map = dict(zip(qual_list,qual_list))  #map of qualified list
		for item in list2:
			fl=True
	  		for subset in itertools.combinations(item, cnt-1):
	  			if subset not in qual_map:
	  				fl=False
	  				break	
	  		if(fl==True):	
	  			list1.append(item)
  	else:
  		list1=list2
	
#print "tuples that qualify" ,final_qualifiers	


f=open(out,"w+")
f.write(str(len(final_qualifiers)))
f.write("\n")
for item in final_qualifiers:
	f.write(",".join(item))
	f.write("\n")



if(flag=="0"):
	f.close()
	exit()

# find all possible association rules

qual_rules=[] # contains rules that qualify confidence
for stuff in final_qualifiers:
	l1=[]
	map_rules={}
	for L in range(1, len(stuff)):
  		for subset in itertools.combinations(stuff, L):  # creates combination of each item
  			l1.append(subset)

  	map_rules = find_rules(l1,len(stuff))			# finds rules for all combinations
  	for key in map_rules:
		if test_association_opt(key,map_rules[key]) == True:    # test association rule confidence
			qual_rules.append([key,map_rules[key]])

#print into file
d = {}
for rule in qual_rules:
	key = tuple(rule[0])
	if d.get(key,0) :
		d[key].update(list(rule[1]))
	else :
		d[key]=set(list(rule[1]))
print d
myfile = open("../resources/rules.txt","wb")
pickle.dump(d,myfile)

if(len(qual_rules)>0):
	f.write(str(len(qual_rules)))
	f.write("\n")
	for item in qual_rules:
		f.write(",".join(item[0]))
		f.write(" => ")
		f.write(",".join(item[1]))
		f.write("\n")

f.close()