import requests
import math
import hashlib

def get_latest_block():
    response = requests.get("https://programmeren9.cmgt.hr.nl:8000/api/blockchain/next")
    return response.json()

def post_nonce(nonce):
    response = requests.post("https://programmeren9.cmgt.hr.nl:8000/api/blockchain", {
        "nonce"	: str(nonce),
	    "user": "Joey 0942389"
    })
    return response

# Converts any string to ascii characters in an array NOTE: Only alphabetical characters will be converted, numeric will stay
def stripWhiteSpaces(s):
    return "".join(s.split()).replace(" ", "")

def convertToAscii(s):
    ascii_array = []
    # Returned ordered string -> ascii array
    for c in s:
        
        # Only convert characters no numbers!!
        if not c.isdigit():
            c = ord(c)
        
        # Split the character and append the array to the ascii_array
        if len(str(c)) > 1:
            c = list(str(c))
        
        ascii_array.append(c)

    # Finally merge any characters with array (99 => 9,9) into one array    
    merged_list = []
    for l in ascii_array:
        merged_list += l
    
    return merged_list

# Calculates the sum of 2 arrays of characters based on the mod10 hash
def calculate_mod10(x, y):
    tmplist = []
    for i in range(0, 10):
        tmplist.append(str((int(x[i]) + int(y[i])) % 10))
    return tmplist   

# Recursive function to get the 10 characters of the ascii_hash
def mod10(a, row):
    if len(a) > 0: 
        if len(row) > 0:
            row = calculate_mod10(row, a[0:10])
            del a[0:10]
            return mod10(a, row)
        else:
            row = calculate_mod10(a[0:10], a[10:20])
            del a[0:20]
            return mod10(a, row)
    else:
        return row

# Formats the ascii array to a suitable mod_10 iterator
def format_ascii_array(ascii_array):
    array_len = len(ascii_array)
    if array_len % 10 != 0:
        for i in range(0, (10 - array_len % 10)):
            ascii_array.append(i)
    return ascii_array

# Hash the block
def hash_block(block):
    ascii_array = format_ascii_array(convertToAscii(stripWhiteSpaces(block)))
    return hashlib.sha256(''.join(mod10(ascii_array, [])).encode()).hexdigest()

# Validates the hash on the puzzle
def valid_proof(new_hash, nonce):
   guess = (str(new_hash) + str(nonce))
   guess_hash = hash_block(guess)
   print(guess_hash)
   return guess_hash[0:4] == '0000'

# Try to hash to complete the puzzle with the nonce
def pow(hashed_block, last_block):
    nonce = 0
    while not valid_proof(create_new_hash_string(hashed_block, last_block), nonce):
        nonce += 1
    return nonce

# Formats the already HASHED latest block to a compatible string
def create_new_hash_string(last_hash, last_block):
    return "{}{}{}{}{}{}".format(
        last_hash,
        last_block["transactions"][0]["from"],
        last_block["transactions"][0]["to"],
        last_block["transactions"][0]["amount"],
        last_block["transactions"][0]["timestamp"],
        last_block["timestamp"]
    )

# Formats the latest block to a compatible string
def format_latest_block_to_string(block):
    return "{}{}{}{}{}{}{}".format(
        block["blockchain"]["hash"], 
        block["blockchain"]["data"][0]["from"], 
        block["blockchain"]["data"][0]["to"], 
        block["blockchain"]["data"][0]["amount"],
        block["blockchain"]["data"][0]["timestamp"],
        block["blockchain"]["timestamp"],
        block["blockchain"]["nonce"],
    )

# MINES THE BLOCK
def mine_block():
    last_block = get_latest_block()
    
    try:
        hashed_block = hash_block(format_latest_block_to_string(last_block))
        nonce = pow(hashed_block,last_block)
        # If nonce is found post to API! FINISH!
        if nonce:
            post_nonce(nonce)
    except:
        print("Blockchain gives the following message: `{}`".format(last_block['message']))
        print("Please wait {} seconds. Then try it again!".format(last_block['countdown']))


if __name__ == '__main__':
    mine_block()