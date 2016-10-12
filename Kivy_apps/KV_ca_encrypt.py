# KV_ca_encrypt.py

###### ESSENTIAL DATA ###########
cells_to_config_no = {"0000": 0, "1000" : 1, "0100" : 2, "1100" : 3, "0010" : 4,"1010" : 5,"0110" : 6,"1110" : 7,"0001" : 8,"1001" : 9,"0101" : 10,"1101" : 11,"0011" :12,"1011" :13,"0111": 14,"1111": 15} #Given the cell configuration as the key, has the arbitrary "config number" I assigned
config_no_to_cells = {0: '0000', 1: '1000', 2: '0100', 3: '1100', 4: '0010', 5: '1010', 6: '0110', 7: '1110', 8: '0001', 9: '1001', 10: '0101', 11: '1101', 12: '0011', 13: '1011', 14: '0111', 15: '1111'} #Gives the corresponding cell configuration given the "config number"
###### ESSENTIAL DATA ###########



###### IMPORTING MODULES ########
import numpy as np
from random import randint
import math,time,random
from collections import OrderedDict
import sys as Sys
from multiprocessing import Pool
from time import sleep
import hashlib, datetime, time
###### IMPORTING MODULES ########


########## BLOCK CA ############
def rule_list_reversal(forward_rule_list):
    """Reverses the forward rule list for use in the reverse evolution"""
    reverse_rule_list =  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for x in forward_rule_list:
        reverse_rule_list[x] = forward_rule_list.index(x) #reverses the rule_list for use in the reverse evolution
        
    return reverse_rule_list

def get_current_config(one, two, three, four):
    """Take in the 4 values as input and decide which of the 16 configurations (0-15) it is"""
    string = str(one) + str(two) + str(three) + str(four)
    return cells_to_config_no[string]

def change_config(current_config,rule_list):
	"""
	Changes the configuration by:
		1. Finding out which config the inputted current_config changes to
		2. Creating a new config string for the new config value
		3. Splitting the string, converting to int, and adding values to values_list
		4. Outputs values_list with the new values
	"""
	changes_to = rule_list[current_config]
	new_config_string = config_no_to_cells[changes_to]
	values_list = []
	for x in new_config_string:
		values_list.append(int(x))
	return values_list
        
def margolus1(rule_list,dish):
    """Does the first part of the evolution, can be customized with the appropiate rule_list for the forward and reverse evolutions"""
    
    height = len(dish)
    width = len(dish[0])
    
    for x in range(0,height-2,2):
		for y in (0,width-2,2): #Starts the 2X2 box at 0,0 and then moves onto the next 2X2 box
			square = dish[x:x+2,y:y+2] #Creates a pointer to the 2X2 part of the dish
			#print "Square in Margolus1 = %s" %square
			current_config = get_current_config(square[0,0],square[0,1],square[1,0],square[1,1]) #Gets the current config number
			values = change_config(current_config,rule_list) #Takes the config number and figures out what to change it to based on the rule_list
			square[0,0] = values[0]
			square[0,1] = values[1]
			square[1,0] = values[2]
			square[1,1] = values[3]#Changes the dish to what values it should be based on the rule_list and the current config
    

def margolus2(rule_list,dish):
    """Does the second part of the evolution, can be customized with the appropiate rule_list for the forward and reverse evolutions"""
    
    height = len(dish)
    width = len(dish[0])
    
    for x in range(1,height-2,2):
		for y in range(1,width-2,2): #Starts the 2X2 box at 1,1 (the second pass has a different neighborhood) and then moves onto the next 2X2 box
			square = dish[x:x+2,y:y+2]
			current_config = get_current_config(square[0,0],square[0,1],square[1,0],square[1,1])
			values = change_config(current_config,rule_list)
			square[0,0] = values[0]
			square[0,1] = values[1]
			square[1,0] = values[2]
			square[1,1] = values[3]

def forward_evolution(generations, rule_list, dish):
    """Performs the forward evolution of the block cellular automata"""
    
    for x in range(0,generations):
        margolus1(rule_list,dish) #runs margolus 1 and 2 for the specificed number of generations
        margolus2(rule_list,dish)
        
    return dish

def reverse_evolution(generations, rule_list, dish):
    """Performs the reverse evolution of the block cellular automata"""
    
    reverse_rule_list = []#initializes the variable
    reverse_rule_list = rule_list_reversal(rule_list)
    
    for x in range(0,generations):
        margolus2(reverse_rule_list,dish)
        margolus1(reverse_rule_list,dish) #runs margolus 1 and 2 for the specificed number of generations
        
    return dish
    
def forward_block_evolution(generations, rule_list, dish_dict, tweak = False, iv_block = [[]]):
    """Performs the forward evolution of the block cellular automata on a block_dict"""
    global progress_bar
    

    if tweak == False:
        dishes_completed = 0
    
    
        for key in dish_dict:
            dish = dish_dict[key]
            dish = forward_evolution(generations, rule_list, dish)
            dishes_completed += 1
            progress_bar.value = dishes_completed
            #printProgress(dishes_completed, len(dish_dict), prefix = 'Forward evolution:', suffix = 'Complete', barLength = 50)
    
        return dish_dict
        
    elif tweak == True:
        dishes_completed = 0
    
        for index in range(len( dish_dict.keys() )):
            key = dish_dict.keys()[index]
            dish = dish_dict[key]
        
            if index == 0:
                dish = XOR( dish_dict[key], iv_block) #uses the iv_block to XOR if it's the first block
            else:
                encrypted_key = dish_dict.keys()[index-1] #uses the last encrypted block to XOR after the first block
                dish = XOR ( dish_dict[key], dish_dict[encrypted_key] )          

            dish = forward_evolution(generations, rule_list, dish)
            dishes_completed += 1
            progress_bar.value = dishes_completed
            printProgress(dishes_completed, len(dish_dict), prefix = 'Forward evolution:', suffix = 'Complete', barLength = 50)
    
        return dish_dict
              
    
def reverse_block_evolution(generations, rule_list, dish_dict, tweak = False, iv_block = [[]]):
    """Performs the reverse evolution of the block cellular automata on a block_dict"""
    global progress_bar
    
    if tweak == False:
        dishes_completed = 0
    
        for key in dish_dict:
            dish = dish_dict[key]
            dish = reverse_evolution(generations, rule_list, dish)
            dishes_completed += 1
            progress_bar.value = dishes_completed
    
        return dish_dict
        
    elif tweak == True:
        dishes_completed = 0
    
        for index in list(reversed( range(len( dish_dict.keys() )) )):
            key = dish_dict.keys()[index]
            dish = dish_dict[key]
            dish = reverse_evolution(generations, rule_list, dish)
            
            if index == 0:
                dish = XOR( dish_dict[key], iv_block) #uses the iv_block to XOR if it's the first block
            else:
                encrypted_key = dish_dict.keys()[index-1] #uses the last encrypted block to XOR after the first block
                dish = XOR ( dish_dict[key], dish_dict[encrypted_key] )
                
            
            dishes_completed += 1
            progress_bar.value = dishes_completed
    
        return dish_dict
        

def calculate_entropy_of_dish(dish):
    """Calculates the entropy of the dish"""
    bit_string = ""
    for row in dish:
        for cell in row:
            bit_string += str(cell) #creates a continuous string of all the bits in the dish
    byteArr = [int(x, 2) for x in map(''.join, zip(*[iter(bit_string)]*8)) ] #creates a byte array by taking each 8 characters in the bit_string and using int(x,2) to turn the binary string into decimal integers
    
    # calculate the frequency of each byte value in the file
    freqList = [0]*256
    fileSize = len(byteArr)
    for byte in byteArr:
        freqList[byte] += 1
    freqList = [float(x)/fileSize for x in freqList]

    """
    for b in range(256):
        ctr = 0
        for byte in byteArr:
            if byte == b:
                ctr += 1#adds one to the frequency of the byte by iterating through each byte in the file
        freqList.append(float(ctr) / fileSize)
    """
    # Shannon entropy
    ent = 0.0
    for freq in freqList:
        if freq > 0:
            ent = ent + freq * math.log(freq, 2)
    return -ent
    
    
    
def XOR(dishA,dishB):
    height = len(dishA)
    width = len(dishA[0])
    dishC = dishA
    
    for x in range(height):
        for y in range(width):
            A = dishA[x][y]
            B = dishB[x][y]
            if A == B:
                dishC[x][y] = 0
            if A != B:
                dishC[x][y] = 1
    
    return dishC

def get_middle_factors(number):
    def factors(n):
        """Function to calculate all the factors of a given number n"""
        return sorted( reduce(list.__add__, ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)) )
        
    factors_list = []
    factors_list =  factors(number)
    #print "Factors: ", factors_list
    middle_factors = [ factors_list[(len(factors_list)/2)-1] , factors_list[(len(factors_list)/2)] ]
    return middle_factors

def open_file_blocks(file_name):
    """Function to open a file and create 256 bit blocks of of all the bits of the file (using random padding at the end)"""
    
    # read the whole file into a byte array
    '''file_name = raw_input("What file would you like to open?: ")'''
    f = open(file_name, "rb")
    print "Opening", file_name
    
    byteArr = map(ord, f.read()) #gets byte number from whatever data the file is in
    byteArr = map(lambda x : '{0:08b}'.format(x), byteArr) #takes the byte number and turns it into binary
    f.close()
    print "Filesize: ", len(byteArr)*8
    bit_sequence = ""
    for row in byteArr:
        for x in row:
            bit_sequence += str(x) #adds the numbers into a bit sequence
    string_list = [bit_sequence[i:i+256] for i in range(0, len(bit_sequence), 256)]
    pad_length = 256 - len(string_list[-1])
    
    for x in range(pad_length-8):
        string_list[-1] += random.choice(["0","1"])
    string_list[-1] += '{0:08b}'.format(pad_length) #append the number of pad bits
    

    dish_dict = OrderedDict()
    for i in range(len(string_list)):
        dish_name = "dish"+str(i)
        dish_dict[dish_name] = np.zeros((16,16), dtype=np.int) #initializes a dish of all zeros
        counter = 0
        for x in range(16):
            for y in range(16): #iterates through the whole dish
                dish_dict[dish_name][x,y] = int(string_list[i][counter])
                counter += 1
                
    return dish_dict
    
def open_file(file_name, _print = False):
    """Function to open a file and create a dish of all the bits of the file"""
    
    def factors(n):
        """Function to calculate all the factors of a given number n"""
        return sorted( reduce(list.__add__, ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)) )
        
    # read the whole file into a byte array
    '''file_name = raw_input("What file would you like to open?: ")'''
    f = open(file_name, "rb")
    byteArr = map(ord, f.read()) #gets byte number from whatever data the file is in
    byteArr = map(lambda x : '{0:08b}'.format(x),byteArr) #takes the byte number and turns it into binary
    f.close()
    factors =  factors(len(byteArr)*8) #gets the factors of the #of bits in the file
    dish_size = [ factors[(len(factors)/2)-1] , factors[(len(factors)/2)] ] #gets the middle two factors (to make the dish as square-like as possible) of a file and uses those as width and height of the file
    height = dish_size[0]
    width = dish_size[1] #makes the dish dimensions equal to the middle factors of the length of the file
    if _print == True:
        print "Opening file %r" %file_name
        print "Dish Height = %s and Dish Width = %s" %(height,width)
    dish = np.zeros((height,width), dtype=np.int) #initializes a dish of all zeros
    bit_sequence = ""
    for row in byteArr:
        for x in row:
            bit_sequence += str(x) #adds the numbers into a bit sequence
    counter = 0
    for x in range(0,len(dish)):
        for y in range(0,len(dish[0])): #iterates through the whole dish
            dish[x,y] = int(bit_sequence[counter]) #goes in order through the whole bit sequence and turns that string into an int to insert to the dish
            counter += 1
    return dish

def write_dish_to_file(file_name,dish):
    """Writes the dish back into a file with name = file_name.pca """
    
    bit_sequence = ""
    for row in dish:
        for cell in row:
            bit_sequence += str(cell) #creates a string of all the bits
    byte_list = [bit_sequence[i:i+8] for i in range(0, len(bit_sequence), 8)] #creates a list of strings of binary length 8 bytes
    byte_list = map(lambda x:int(x,2), byte_list) #turns the binary strings into decimal ints
    byte_list = map(chr, byte_list) #turns the ints back to unicode
    
    file = open(file_name,"w") #opens the file
    for i in byte_list:
        file.write(i) #writes the unicode back to file
    print "File written successfully"

def dish_to_blocks(dish):
	bit_sequence = ""
	for row in dish:
		for cell in row:
			bit_sequence += str(cell) #creates a string of all the bits

	string_list = [bit_sequence[i:i+256] for i in range(0, len(bit_sequence), 256)]
	pad_length = 256 - len(string_list[-1])

	for x in range(pad_length-8):
		string_list[-1] += random.choice(["0","1"])
	string_list[-1] += '{0:08b}'.format(pad_length) #append the number of pad bits


	dish_dict = OrderedDict()
	for i in range(len(string_list)):
		dish_name = "dish"+str(i)
		dish_dict[dish_name] = np.zeros((16,16), dtype=np.int) #initializes a dish of all zeros
		counter = 0
		for x in range(16):
			for y in range(16): #iterates through the whole dish
				dish_dict[dish_name][x,y] = int(string_list[i][counter])
				counter += 1
            
	return dish_dict

def blocks_to_dish(block_dict,remove_padding = False):
    
    bit_sequence = ""
    for key in block_dict:
        dish = block_dict[key]
        for row in dish:
            for cell in row:
                bit_sequence += str(cell) #creates a string of all the bits

    if remove_padding == True and len(bit_sequence)%256 != 0:
        print "Removing Padding"
        pad_length = bit_sequence[-8:]
        pad_length = int(pad_length,2)
        bit_sequence = bit_sequence[:-pad_length]


    dish_size = get_middle_factors(len(bit_sequence)) #gets the middle two factors (to make the dish as square-like as possible) of a file and uses those as width and height of the file
    height = dish_size[0]
    width = dish_size[1] #makes the dish dimensions equal to the middle factors of the length of the dile
    dish = np.zeros((height,width), dtype=np.int) #initializes a dish of all zeros
    counter = 0
    for x in range(len(dish)):
        for y in range(len(dish[0])): #iterates through the whole dish
            dish[x,y] = int(bit_sequence[counter]) #goes in order through the whole bit sequence and turns that string into an int to insert to the dish
            counter += 1
    return dish
########## BLOCK CA ############

########## HASH TEST ############
def checksum(file_name):
	global original_dish
	dish = open_file(file_name)
	bitstring = bin(int(hashlib.sha256(dish).hexdigest(),16))[2:]
	bitstring = "0" * (256-len(bitstring) ) + bitstring

	original_dish = dish

	return initialize(bitstring,16,16)
    
def initialize(bitstring,height,width):
    dish = np.zeros( (height,width), dtype=np.int )

    counter = 0
    for x in range(height):
        for y in range(width): #iterates through the whole dish
            dish[x,y] = int(bitstring[counter]) #goes in order through the whole bit sequence and turns that string into an int to insert to the dish
            counter += 1
    return dish
########## HASH TEST ############


########## KEY PROCESSING ############
def encode(key):
    bitstring = ""
    for x in key:
        bitstring += bin(x)
    
    key = bitstring.split("0b")
    key.remove('')
    for x in range(17):
        key[x] = "0" * (4 - len(key[x]) ) + key[x]
        
    bitstring =  ''.join(key)
    
    pad_length = 256-len(bitstring) 

    for x in range(pad_length-8):
        bitstring += random.choice(["0","1"])
    bitstring += '{0:08b}'.format(pad_length)
    
    return bitstring
    
def decode(bitstring):
    pad_length = bitstring[-8:]
    pad_length = int(pad_length,2)
    bitstring = bitstring[:-pad_length]
    
    key = []
    for x in range(16):
        key.append(bitstring[x*4 : x*4 + 4] )
    key.append( bitstring[64:] )
    for x in range(17):
        key[x] = "0b" + str( key[x] )
        key[x] = int(key[x],2)
        
    return key
    
def back_to_key(dish):
    bitstring = ''
    for x in range(16):
        for y in range(16):
            bitstring += str( dish[x,y] )
            
    return decode(bitstring)
    
    
def generate_key_block(rule_list,generations):
    
    born = [1,3,5,7]#fredkin rule
    survive = [0,2,4,6,8]
    
    rule_list.append(generations)
    key = rule_list

    bitstring = encode(key)
    
    #bitstring = ''.join( [ random.choice(["0","1"]) for x in range(256) ] ) #random initial conditions
    
    dish = initialize(bitstring,16,16)

    dish = evolve(generations,dish,born,survive,print_dish = False,pause = 0)

    bitstring =  ''.join([ str(dish[x,y]) for x in range(16) for y in range(16) ])
    
    #print "".join([chr(int(x, 2)) for x in map(''.join, zip(*[iter(bitstring)]*8)) ])
    return dish
########## KEY PROCESSING ############

########## LIFE-LIKE ############
def iterate(dish,born,survive,print_dish = False):
    width = len(dish)
    height = len(dish[0])
    new_dish = dish.copy()
    for x in range(width):
        for y in range(height):
            cell = dish[x,y]
            neighbors = [    dish[(x-1)%width,(y+1)%height],   dish[x,(y+1)%height], dish[(x+1)%width,(y+1)%height],
                             dish[(x-1)%width,y]  ,            dish[x,y],            dish[(x+1)%width,y],                           
                             dish[(x-1)%width,(y-1)%height],   dish[x,(y-1)%height], dish[(x+1)%width,(y-1)%height]      ]
            neighbor_sum = sum(neighbors) - dish[x,y]
            #print x,y,neighbors,neighbor_sum
            if cell == 1:
                if neighbor_sum in survive:
                    new_dish[x,y] = 1
                else:
                    new_dish[x,y] = 0
            elif cell == 0:
                if neighbor_sum in born:
                    new_dish[x,y] = 1
                else:
                    new_dish[x,y] = 0
    if print_dish == True:
        print "-" * 40
        print new_dish
        print "-" * 40
    return new_dish
        
def evolve(generations,dish,born,survive,print_dish = False,pause = 0):
    
    for x in range(generations):
        sleep(pause)
        dish = iterate(dish,born,survive,print_dish)
    
    return dish
########## LIFE-LIKE ############

def process_random_block(file_name,password):
    key_block = generate_key_block(key,generations*10)
    
    #password = raw_input("Enter password (32 characters is best!): ")
    
    scr_password_block = create_iv(password) #creates the scrambled password block + accompanying stats
    checksum_block = checksum(file_name) 
    pword_checksum = XOR(checksum_block, scr_password_block)
    nonce = XOR(key_block,pword_checksum)


    return nonce

def string_to_bits(string):
    bitlist = [ '{0:08b}'.format(ord(x)) for x in list(string)]
    bitstring = "".join(bitlist)
    return bitstring

def generate_random_block():
    import os
    rand_block = os.urandom(32)
    rand_block = string_to_bits(rand_block)
    rand_block = initialize(rand_block,16,16)
    rand_block_entropy = calculate_entropy_of_dish(rand_block)
    return rand_block

def generate_password_block(password):
    
    if len(password) < 32:
        newstring = password * 32
        password = newstring[0:32]
    else:
    	password = password[0:32]
        
    password = string_to_bits(password)
    password = initialize(password,16,16)
    entropy = calculate_entropy_of_dish(password)
    return password

def create_iv(password):
    rand_block = generate_random_block()
    password = generate_password_block(password)
    iv = XOR(rand_block,password)
    
    return iv
    
def printProgress (iteration, total, prefix = '', suffix = '', decimals = 2, barLength = 100):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : number of decimals in percent complete (Int) 
        barLength   - Optional  : character length of bar (Int) 
        #http://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
    """
    filledLength    = int(round(barLength * iteration / float(total)))
    percents        = round(100.00 * (iteration / float(total)), decimals)
    bar             = '#' * filledLength + '-' * (barLength - filledLength)
    Sys.stdout.write('%s [%s] %s%s %s\r' % (prefix, bar, percents, '%', suffix)),
    Sys.stdout.flush()
    if iteration == total:
        print("\n")


########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################


import kivy
kivy.require('1.9.0')

__version__ = "1"

import random
import numpy as np


from kivy.clock import Clock
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.togglebutton import ToggleButton
#import plyer.facades.FileChooser.open_file
from kivy.uix.progressbar import ProgressBar

Builder.load_string("""

<Menu>:
    id: menu
    name: 'menu_screen'
    BoxLayout:
        id: box_layout
        orientation: 'vertical'
        Label:
            id: label1
            text: "CA ENCRYPT:"
        Label:
            id: label1
            text: "Developed by Federico Reyes"
        BoxLayout:
	        id: box_layout
	        orientation: 'horizontal'
	        Button:
	            id: encrypt
	            text: "ENCRYPT"
	            on_press: root.change_encrypt()
	        Button:
	            id: decrypt
	            text: "DECRYPT"
	            on_press: root.change_decrypt()



<EncryptParameterScreen>
	id: encrypt_parameter_screen
	name: 'encrypt_parameter_screen'
	BoxLayout:
        id: box_layout
        orientation: 'vertical'
        TextInput:
            id: file_name
            hint_text: 'Enter file path:'
        TextInput:
            id: generations
            hint_text: 'Enter generations:'
        TextInput:
            id: password
            hint_text: 'Enter password (32 characters is best!) :'
        BoxLayout:
        	id: rule_list
        	orientation: 'horizontal'
    		TextInput:
	            id: rule_0
	            hint_text: '0'
	        TextInput:
	            id: rule_1
	            hint_text: '1'
	        TextInput:
	            id: rule_2
	            hint_text: '2'
	        TextInput:
	            id: rule_3
	            hint_text: '3'
	        TextInput:
	            id: rule_4
	            hint_text: '4'
	        TextInput:
	            id: rule_5
	            hint_text: '5'
	        TextInput:
	            id: rule_6
	            hint_text: '6'
	        TextInput:
	            id: rule_7
	            hint_text: '7'
	        TextInput:
	            id: rule_8
	            hint_text: '8'
	        TextInput:
	            id: rule_9
	            hint_text: '9'
	        TextInput:
	            id: rule_10
	            hint_text: '10'
	        TextInput:
	            id: rule_11
	            hint_text: '11'
	        TextInput:
	            id: rule_12
	            hint_text: '12'
	        TextInput:
	            id: rule_13
	            hint_text: '13'
	        TextInput:
	            id: rule_14
	            hint_text: '14'
	        TextInput:
	            id: rule_15
	            hint_text: '15'
	    Button:
	    	name: start
            id: start
            text: "Done"
            on_release: root.start()
        Button:
        	id: test_done
        	text: "Test Done"
        	on_release: root.test_done()



<DecryptParameterScreen>
	id: decrypt_parameter_screen
	name: 'decrypt_parameter_screen'
	BoxLayout:
        id: box_layout
        orientation: 'vertical'
        TextInput:
            id: file_name
            hint_text: 'Enter file path:'
        TextInput:
            id: key_file_name
            hint_text: 'Enter key file path:'
        TextInput:
            id: generations
            hint_text: 'Enter generations:'
        BoxLayout:
        	id: rule_list
        	orientation: 'horizontal'
    		TextInput:
	            id: rule_0
	            hint_text: '0'
	        TextInput:
	            id: rule_1
	            hint_text: '1'
	        TextInput:
	            id: rule_2
	            hint_text: '2'
	        TextInput:
	            id: rule_3
	            hint_text: '3'
	        TextInput:
	            id: rule_4
	            hint_text: '4'
	        TextInput:
	            id: rule_5
	            hint_text: '5'
	        TextInput:
	            id: rule_6
	            hint_text: '6'
	        TextInput:
	            id: rule_7
	            hint_text: '7'
	        TextInput:
	            id: rule_8
	            hint_text: '8'
	        TextInput:
	            id: rule_9
	            hint_text: '9'
	        TextInput:
	            id: rule_10
	            hint_text: '10'
	        TextInput:
	            id: rule_11
	            hint_text: '11'
	        TextInput:
	            id: rule_12
	            hint_text: '12'
	        TextInput:
	            id: rule_13
	            hint_text: '13'
	        TextInput:
	            id: rule_14
	            hint_text: '14'
	        TextInput:
	            id: rule_15
	            hint_text: '15'
	    Button:
	    	name: start
            id: start
            text: "Done"
            on_release: root.start()

<EncryptingScreen>
	id: encrypting_screen
	name: "encrypting_screen"
	BoxLayout:
		id: box_layout
        orientation: 'vertical'
        Button:
        	id: start
        	text: "Start Encryption"
        	on_release: root.start()
        Button:
        	id: key_processing_label
        	text: "Process Key"
        	on_release: root.process_key()
        Button:
        	id: opening_file_label
        	text: "Open File"
        	on_release: root.open_file()
        Button:
        	id: original_entropy_label
        	text: "Calculate entropy of original file"
        	on_release: root.original_entropy()
        Button:
        	id: encrypting_label
        	text: "Encrypt data"
        	on_release: root.encrypt()
        ProgressBar:
        	id: progress_bar
        Button:
        	id: evolved_entropy_label
        	text: "Calculate entropy of encrypted file"
        	on_release: root.evolved_entropy()
        Button:
        	id: ciphertext_label
        	text: "Write ciphertext to new file"
        	on_release: root.write_ciphertext()
        Button:
        	id: quit
        	text: "Quit"
        	on_release: root.quit()

""")

class EncryptingScreen(Screen):

	def start(self):
		global progress_bar

	def process_key(self):
		self.ids.box_layout.remove_widget(self.ids.start)
		self.ids.key_processing_label.text = "Processing key..."
		self.IV = process_random_block(file_name,password)

		write_dish_to_file(file_name.rsplit("/",1)[0] + "/" +  file_name.rsplit("/",1)[-1].split(".")[0] + "_key.pca", self.IV)
		self.ids.key_processing_label.text = "Key processed! Key can be found at %s" %(file_name.rsplit("/",1)[0] + "/" +  file_name.rsplit("/",1)[-1].split(".")[0] + "_key.pca") 

	def open_file(self):
		self.ids.opening_file_label.text = "Opening file %s..." %file_name
		self.dish_dict = dish_to_blocks(original_dish)
		self.ids.opening_file_label.text = file_name + " opened!"

	def original_entropy(self):
		global original_dish
		self.ids.original_entropy_label.text = "Calculating entropy of original file..."
		original_entropy = calculate_entropy_of_dish( original_dish )
		self.ids.original_entropy_label.text = "Original entropy of file = %r" %original_entropy

	def encrypt(self):
		global progress_bar

		start = time.time()
		self.ids.encrypting_label.text = "Encrypting..."
		progress_bar = self.ids.progress_bar
		progress_bar.max = len(self.dish_dict)
		self.evolved_dict = forward_block_evolution(generations, rule_list, self.dish_dict, tweak = True, iv_block = self.IV)
		end = time.time()
		self.ids.encrypting_label.text = "Encryption completed! Encryption took %r seconds!" %int(round(end-start))
		self.ids.box_layout.remove_widget(progress_bar)

	def evolved_entropy(self):
		self.ids.evolved_entropy_label.text = "Calculating entropy of encrypted file..."
		self.evolved_dish = blocks_to_dish(self.evolved_dict).copy()
		evolved_entropy = calculate_entropy_of_dish( self.evolved_dish )
		self.ids.evolved_entropy_label.text = "Entropy of encrypted file = %r" %evolved_entropy

	def write_ciphertext(self):
		write_dish_to_file(file_name.rsplit("/",1)[0] + "/" + file_name.rsplit("/",1)[-1].split(".")[0] + ".pca", self.evolved_dish)
		self.ids.ciphertext_label.text = "Encryption Completed! Encrypted file %s written"%(file_name.rsplit("/",1)[0] + "/" + file_name.rsplit("/",1)[-1].split(".")[0] + ".pca")

		'''
		from pympler import tracker
		tr = tracker.SummaryTracker()
		tr.print_diff() 
		'''

		return None
		
	def quit(self):
		exit()

class Menu(Screen): 
	global sm

	def change_encrypt(self,*args):
		global sm,encrypt_parameter_screen
		encrypt_parameter_screen = EncryptParameterScreen()
		sm.add_widget( encrypt_parameter_screen )
		sm.current = 'encrypt_parameter_screen' #changes the screen to game_screen instance

	def change_decrypt(self,*args):
		global sm,decrypt_parameter_screen
		decrypt_parameter_screen = DecryptParameterScreen()
		sm.add_widget( decrypt_parameter_screen )
		sm.current = 'decrypt_parameter_screen' #changes the screen to game_screen instance


class EncryptParameterScreen(Screen):
	global sm

	def switch_screen(self):
		encrypting_screen = EncryptingScreen()
		sm.add_widget( encrypting_screen )
		sm.current = 'encrypting_screen' #changes the screen to game_screen instance



	def start(self):
		global size,generations,rule_list,file_name,password,key

		try:
			rule_list = [ int(self.ids.rule_0.text), int(self.ids.rule_1.text),int(self.ids.rule_2.text),int(self.ids.rule_3.text),int(self.ids.rule_4.text),int(self.ids.rule_5.text),int(self.ids.rule_6.text),int(self.ids.rule_7.text),int(self.ids.rule_8.text),int(self.ids.rule_9.text),int(self.ids.rule_10.text),int(self.ids.rule_11.text),int(self.ids.rule_12.text),int(self.ids.rule_13.text),int(self.ids.rule_14.text),int(self.ids.rule_15.text)]
			generations = int( self.ids.generations.text)
			file_name = str(self.ids.file_name.text)
			password = str(self.ids.password.text)
			key = rule_list[:]
			key.append(generations)
			self.switch_screen()
		except ValueError:
			pass

	def test_done(self):
		global size,generations,rule_list,file_name,password,key

		try:
			rule_list = [6,15,8,13,3,7,0,14,12,5,9,1,11,4,10,2]
			generations = 20
			file_name = "/Users/frg100/Desktop/riverdale_logo.jpeg"
			password = "riverdale_logo.jpeg"
			key = rule_list[:]
			key.append(generations)
			self.switch_screen()
		except ValueError:
			pass

class DecryptParameterScreen(Screen):
	global sm


	def start(self):
		global size,generations,rule_list

		try:
			rule_list = [ int(self.ids.rule_0.text), int(self.ids.rule_1.text),int(self.ids.rule_2.text),int(self.ids.rule_3.text),int(self.ids.rule_4.text),int(self.ids.rule_5.text),int(self.ids.rule_6.text),int(self.ids.rule_7.text),int(self.ids.rule_8.text),int(self.ids.rule_9.text),int(self.ids.rule_10.text),int(self.ids.rule_11.text),int(self.ids.rule_12.text),int(self.ids.rule_13.text),int(self.ids.rule_14.text),int(self.ids.rule_15.text)]
			generations = int( self.ids.generations.text)
			file_name = self.ids.file_name.text
			key_file_name = self.ids.key_file_name.text
			self.switch_screen(rule_list,generations,file_name,key_file_name)
		except ValueError:
			pass

class MargolusCAApp(App):
	global sm

	def build(self):
		global sm,game_screen,score_screen
		sm = ScreenManager() #initializes a new screenmanager instance
		menu = Menu() #initializes a new menu instance
		sm.add_widget(menu) #adds the menu instance to the screenmanager instance
		return sm #returns the screenmanager to start the app





if __name__=='__main__':
	MargolusCAApp().run()


# Opening file (filename.pca)
# Opening key file
# Decrypting
# File processed: filename