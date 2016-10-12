#!/usr/bin/python

import sys
import numpy as np
import re

REPEATER = re.compile(r"(.+?)\1+$")

def extend(word):
    if len(word) < 32:
        newstring = word * 32
        word = newstring[0:32]
    return word
    
def string_to_bits(string):
    bitlist = [ '{0:08b}'.format(ord(x)) for x in list(string)]
    bitstring = "".join(bitlist)
    return bitstring
    
def initialize(bitstring):
    dish = np.zeros( (16,16), dtype=np.int )

    counter = 0
    for x in range(len(dish)):
        for y in range(len(dish[0])): #iterates through the whole dish
            dish[x,y] = int(bitstring[counter]) #goes in order through the whole bit sequence and turns that string into an int to insert to the dish
            counter += 1
    return dish
    
def XOR(dishA,dishB):
    height = len(dishA)
    width = len(dishA[0])
    dishC = dishA
    
    for x in range(height):
        for y in range(width):
            A = dishA[x,y]
            B = dishB[x,y]
            if A == B:
                dishC[x,y] = 0
            if A != B:
                dishC[x,y] = 1
    
    return dishC
    
def principal_period(s):
    i = (s+s).find(s, 1, -1)
    return None if i == -1 else s[:i] 

def repeated(s):
    match = REPEATER.match(s)
    return match.group(1) if match else None 
    
def dish_to_string(dish):
    bit_sequence = ""
    for row in dish:
        for cell in row:
            bit_sequence += str(cell) #creates a string of all the bits
    byte_list = [bit_sequence[i:i+8] for i in range(0, len(bit_sequence), 8)] #creates a list of strings of binary length 8 bytes
    byte_list = map(lambda x:int(x,2), byte_list) #turns the binary strings into decimal ints
    byte_list = map(chr, byte_list) #turns the ints back to unicode
    return ''.join(byte_list)
    
def send():
    int_list = (sys.argv)[1].split(",")
    keyword = (sys.argv)[2]
    pword_len = int((sys.argv)[3])

    bitarray = map(lambda x : '{0:08b}'.format(x), [int(x) for x in int_list] ) #takes the byte number and turns it into binary
    bitstring = ''.join(bitarray)
    
    bitblock = initialize(bitstring)
    keyword = initialize( string_to_bits( extend(keyword) ) )
    
    password = dish_to_string( XOR(bitblock, keyword) )[:pword_len]

    return password
    

def recieve():
    password = (sys.argv)[1]
    keyword = (sys.argv)[2]
    

    password = initialize( string_to_bits( extend(password) ) )
    keyword = initialize( string_to_bits( extend(keyword) ) )
    
    block = XOR(password,keyword)
    
    
    bitstring = ''
    for row in block:
        for cell in row:
            bitstring += str(cell)
            
    bit_sequence = bitstring
            
    byte_list = [bit_sequence[i:i+8] for i in range(0, len(bit_sequence), 8)] #creates a list of strings of binary length 8 bytes
    byte_list = map(lambda x:str(int(x,2)), byte_list) #turns the binary strings into decimal ints
    
    return ','.join(byte_list)
    
            
    #sys.stdout.write(bitstring)

if __name__ == "__main__":
    if (sys.argv)[3] == '-r':
        int_list = recieve()
        sys.stdout.write(str(int_list))
        print ""
    elif (sys.argv)[4] == '-s':
        password = send()
        sys.stdout.write(str(password))
        print ""
        
"""11,10,10,17,23,27,17,10,31,8,11,11,6,12,17,29,3,28,9,10,28,29,6,29,20,0,29,8,29,7,23,10"""
    





