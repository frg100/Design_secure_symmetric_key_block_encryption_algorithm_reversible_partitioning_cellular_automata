import subprocess
import pexpect
import sys
import re
import time
import random
from tinydb import TinyDB, Query
import numpy as np
from random import randint
import math,time,random
from collections import OrderedDict
import sys as Sys
from time import sleep
import hashlib, datetime, time

file_name = Sys.argv[1]#"/Users/frg100/Desktop/Scholars/Testing_files/pdfs/lotr.pdf"
db = TinyDB(file_name.split(".")[0] + '.json')
nist_root_dir = "/home/frg100/scholars/sts-2.1.2/sts-2.1.2"

child = pexpect.spawn ("bash")
child.sendline ("cd " + nist_root_dir)
child.sendline ('./assess %r' %(raw_input("./assess ____: ")))
child.logfile = sys.stdout
child.expect ('Enter Choice: ')
child.sendline ('0')
child.expect ("User Prescribed Input File: ")
#filename = subprocess.check_output("pwd") + "/" + file_name.split(".")[0] + ".pca"
filename = '/home/frg100/scholars/' + file_name.split(".")[0] + ".pca"
child.sendline (filename)
child.expect ('Enter Choice: ')
child.sendline ('1')
child.expect (": ")
child.sendline ('0')
child.expect ("How many bitstreams?")
child.sendline ('10')
child.expect ("Select input mode:")
child.sendline ('1')
child.expect ("Statistical Testing Complete!!!!!!!!!!!!")
child.sendline ('exit')


with open(nist_root_dir+"/experiments/AlgorithmTesting/finalAnalysisReport.txt", 'r') as content_file:
    nist = content_file.read()

nist_results = {}
counts = {"Serial":2,"NonOverlappingTemplate":2,"CumulativeSums":2,"andomExcursions":2,"andomExcursionsVariant":2}

for x in nist.split('\n')[7:-13]:
	if x[65:] not in nist_results:
		nist_results[ x[65:] ] = ( x[41:49], x[54:59] )
	else:
		try:
			key = x[65:] + str(counts[x[65:]])
			counts[x[65:]] += 1
			nist_results[ key ] = ( x[41:49], x[54:59] )
		except KeyError:
			pass
	#print x[65:], nist_results[ x[65:] ]

db.insert(nist_results)
print nist_results
print "Done with nist"