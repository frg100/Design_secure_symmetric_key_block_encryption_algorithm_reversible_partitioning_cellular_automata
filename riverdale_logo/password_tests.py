# ca_encrypt.py

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
    

    if tweak == False:
        dishes_completed = 0
    
    
        for key in dish_dict:
            dish = dish_dict[key]
            dish = forward_evolution(generations, rule_list, dish)
            dishes_completed += 1
            printProgress(dishes_completed, len(dish_dict), prefix = 'Forward evolution:', suffix = 'Complete', barLength = 50)
    
        return dish_dict
        
    elif tweak == True:
        dishes_completed = 0
    
        for index in range(len( dish_dict.keys() )):
            start = time.time()
            key = dish_dict.keys()[index]
            dish = dish_dict[key]
        
            if index == 0:
                dish = XOR( dish_dict[key], iv_block) #uses the iv_block to XOR if it's the first block
            else:
                encrypted_key = dish_dict.keys()[index-1] #uses the last encrypted block to XOR after the first block
                dish = XOR ( dish_dict[key], dish_dict[encrypted_key] )          

            dish = forward_evolution(generations, rule_list, dish)
            end = time.time()
            time_taken = end-start
            if dishes_completed % 40 == 0:
            	bits_per_second = round( (float(1) / float(time_taken) ) * 256)
            dishes_completed += 1
            printProgress(dishes_completed, len(dish_dict), prefix = 'Forward evolution:', suffix = 'Complete at %r bits per second' %bits_per_second, barLength = 50)
    
        return dish_dict
              
    
def reverse_block_evolution(generations, rule_list, dish_dict, tweak = False, iv_block = [[]]):
    """Performs the reverse evolution of the block cellular automata on a block_dict"""
    
    if tweak == False:
        dishes_completed = 0
    
        for key in dish_dict:
            dish = dish_dict[key]
            dish = reverse_evolution(generations, rule_list, dish)
            dishes_completed += 1
            printProgress(dishes_completed, len(dish_dict), prefix = 'Reverse Evolution:', suffix = 'Complete', barLength = 50)
    
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
            printProgress(dishes_completed, len(dish_dict), prefix = 'Reverse evolution:', suffix = 'Complete', barLength = 50)
    
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

def calculate_hamming_distance(original_dish,current_dish):
    height = len(current_dish)
    width = len(current_dish[0])
    hamming_distance = 0
    total = 0
    
    for x in range(height):
        for y in range(width):
            if original_dish[x][y] != current_dish[x][y]:
                hamming_distance += 1
                total += 1
            else:
                total += 1
    return float(hamming_distance)/float(total)
    
def calculate_histogram_flatness(dish):
    
    bit_string = ""
    for row in dish:
        for cell in row:
            bit_string += str(cell) #creates a continuous string of all the bits in the dish
    byteArr = [int(x, 2) for x in map(''.join, zip(*[iter(bit_string)]*8)) ] #creates a byte array by taking each 8 characters in the bit_string and using int(x,2) to turn the binary string into decimal integers
    
    # calculate the frequency of each byte value in the file
    freqList = []
    fileSize = len(byteArr)
    for b in range(256):
        ctr = 0
        for byte in byteArr:
            if byte == b:
                ctr += 1#adds one to the frequency of the byte by iterating through each byte in the file
        freqList.append(float(ctr) / fileSize)
    distance = [ abs( x - 0.00390625) for x in freqList]
    average_distance = sum(distance) / len(distance)
    
    return average_distance
    
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

    '''
    rand_block = [[1, 0, 0, 0, 1, 1, 0, 0 ,1, 0 ,1, 1, 0 ,0 ,1, 0],
                  [0, 0, 0, 0, 0, 1 ,0, 0 ,0 ,0 ,1, 1 ,1, 1 ,0, 0],
                  [1, 0, 0, 1, 0, 1 ,1 ,0 ,1, 1, 0 ,0 ,1, 0 ,1, 1],
                  [1, 0, 1, 0, 0, 0 ,0 ,0 ,0, 1, 0, 1, 1, 0 ,0, 0],
                  [0, 0, 0, 0, 0, 0 ,0, 0 ,0 ,0 ,0, 1, 0 ,0 ,0 ,1],
                  [0, 0, 0, 1, 0, 0, 1 ,1, 0 ,0, 1, 0, 0, 0, 0 ,1],
                  [1, 0, 1, 1, 0, 0, 0 ,0 ,0 ,0, 1 ,1, 1 ,1, 1 ,1],
                  [1, 1, 1, 0, 1, 1, 1, 0 ,1 ,0 ,0 ,1 ,1, 1 ,1 ,0],
                  [1, 1, 1, 1, 0, 0 ,0 ,0 ,1 ,1 , 0,0 ,0 ,0 ,0 ,0],
                  [0, 0, 0, 1, 0, 1, 1, 1, 1 ,1 ,1 ,1 ,0 ,1 ,1 ,1],
                  [1, 1, 1, 0, 1, 0 ,0, 0, 0, 0 ,0 ,0 ,1, 0 ,0 ,0],
                  [1, 1, 1, 1, 0, 1 ,1 ,1, 1 ,1, 0, 0, 1 ,0 ,1, 1],
                  [0, 1, 0, 1, 0, 0, 0 ,1 ,1 ,0 ,1, 0, 1 ,1, 0, 0],
                  [1, 1, 1, 0, 0, 1 ,1, 1, 0 ,1 ,0 ,1 ,0, 0 ,0 ,1],
                  [0, 1, 1, 0, 1, 1, 0 ,0 ,1, 1, 1, 1 ,1, 1 ,0 ,1],
                  [0, 0, 1, 1, 0, 1, 1 ,1 ,0 ,1 ,1, 1 ,1 ,0 ,0 ,0]]
    '''

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
    percents        = '{:.2f}'.format(round(100.00 * (iteration / float(total)), decimals))
    bar             = '#' * filledLength + '-' * (barLength - filledLength)
    Sys.stdout.write('%s [%s] %s%s %s\r' % (prefix, bar, percents, '%', suffix)),
    Sys.stdout.flush()
    if iteration == total:
        print("\n")

def bit_flip(file_name):
    f = open(file_name, "rb")
    print "Opened file %r" %file_name
    byteArr = map(ord, f.read()) #gets byte number from whatever data the file is in
    f.close()
    byteArr = map(lambda x : '{0:08b}'.format(x),byteArr) #takes the byte number and turns it into binary
    f.close()
    bit_sequence = ""
    for row in byteArr:
        for x in row:
            bit_sequence += str(x) #adds the numbers into a bit sequence
            
    bit_sequence = list(bit_sequence)
        
    rand_num = random.randint(0, len(bit_sequence) )
    print "Bit flip rand num: " + rand_num
    if bit_sequence[ rand_num ] == "0":
        bit_sequence[ rand_num ] = "1"
    else:
        bit_sequence[ rand_num ] = "0"
        
    bit_sequence = "".join(bit_sequence)
        
            
    byte_list = [bit_sequence[i:i+8] for i in range(0, len(bit_sequence), 8)] #creates a list of strings of binary length 8 bytes
    byte_list = map(lambda x:int(x,2), byte_list) #turns the binary strings into decimal ints
    byte_list = map(chr, byte_list) #turns the ints back to unicode
    
    file = open("flipped_" + file_name ,"w") #opens the file
    for i in byte_list:
        file.write(i) #writes the unicode back to file
    return "flipped_" + file_name



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
# pca_tests.py

import subprocess
import pexpect
import sys
import re
import time
import random
from tinydb import TinyDB, Query
from block_ca import *


file_name = Sys.argv[1]
password = "KHJSDGVJHSsadjhdZJBDHS"
rule_list = [3,6,1,8,11,14,2,4,15,12,13,5,7,10,9,0]
generations = 25
key = rule_list[:]
key.append(generations)

def authorize_gsheets(credentials_file,url):
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
    
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
    gc = gspread.authorize(credentials)
    
    #sh = gc.open_by_url(url)
    worksheet = gc.open('pca_tests_data').sheet1
    return worksheet

credentials_file = 'block-ca-caf120fef8db.json'
url = "https://docs.google.com/spreadsheets/d/1EFTsd8IN7WFHjcXCTu7_dlG2J_eVg-chp80u45h0roc/edit#gid=0"
worksheet = authorize_gsheets(credentials_file, url)

def key_flip(file_name):
    key_name = file_name.split(".")[0] + "_key.pca"
    #encrypted_name = file_name.split(".")[0] + ".pca"
    key = process_random_block(file_name,password)
    write_dish_to_file(key_name,key)

    randnum = random.randint(15,35)
    generations = randnum

    encrypted_dish_dict = forward_block_evolution(generations,rule_list, open_file_blocks(file_name), True, key)


    processed_dish_dict = reverse_block_evolution(generations, rule_list, encrypted_dish_dict, True, key)
    processed_dish = blocks_to_dish(processed_dish_dict, True).copy()
    write_dish_to_file("2_"+file_name, processed_dish)

    if random.randint(0,1) == 0:
        generations -= 1
        operation = '-'
    else:
        generations += 1
        operation = '+'
    
    wrong_processed_dish_dict = reverse_block_evolution(generations, rule_list, encrypted_dish_dict, True, key)
    wrong_processed_dish = blocks_to_dish(wrong_processed_dish_dict,True).copy()
    write_dish_to_file("wrong_" + file_name, wrong_processed_dish)
    difference = 100 * calculate_hamming_distance(wrong_processed_dish, processed_dish)
    return difference, generations, operation

    
for x in range(2,102):
    print x
    difference, generations, operation = key_flip(file_name)
    worksheet.update_cell(120, x, difference)
    worksheet.update_cell(121, x, generations)
    worksheet.update_cell(122, x, difference)
