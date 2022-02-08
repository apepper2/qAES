import cirq
from sage.all import *
from itertools import combinations, permutations
from sbox_gates import *

from mix_columns import *
from key_schedule import *

class SboxVariables():
    def __init__(self):
        self.word_slots = [ cirq.LineQubit.range(32) for i in range(8)] 
        self.T = [
            cirq.NamedQubit("T" + str(i)) for i in range(6)
        ]
        # self.g, self.d, self.h, self.i = self.T
        # S = eng.allocate_qureg(8)
        self.S = [
            cirq.NamedQubit("S" + str(i)) for i in range(8)
        ]

def configure_circuit_input(configuration, orig_circuit=None, input_bit_list = []):
    moment_ops = []
    for k in range(len(input_bit_list)):  # initialize Ubox to given ival
        if input_bit_list[k]:
            # X | U[k]
            # circuit.append()
            moment_ops.append(cirq.ops.X.on(configuration.U[k]))
    # TODO: Doubts
    circuit = cirq.Moment(moment_ops) + orig_circuit
    return circuit

def rot_word(word):
	pass

def rcon(word):
	pass

def sub_word(word):
	pass


def sub_bytes(msg):
	for i in range s16:
		msg[i*8:(i+1)*8] = sbox(msg[i*8:(i+1)*8]) #need outputs+ function construction
	return(msg)

def sub_bytes_inverse(msg):
	pass

def shift_rows(msg):
	msg[32:40],msg[40:48],msg[48:56],msg[56:64]=msg[40:48],msg[48:56],msg[56:64],msg[32:40]
	msg[64:72],msg[72:80],msg[80:88],msg[88:96]=msg[80:88],msg[88:96],msg[64:72],msg[72:80]
	msg[96:104],msg[104:112],msg[112:120],msg[120:128]=msg[120:128],msg[96:104],msg[104:112],msg[112:120]
	return(msg)

def shift_rows_inverse(msg):
	msg[40:48],msg[48:56],msg[56:64],msg[32:40]=msg[32:40],msg[40:48],msg[48:56],msg[56:64]
	msg[80:88],msg[88:96],msg[64:72],msg[72:80]=msg[64:72],msg[72:80],msg[80:88],msg[88:96]
	msg[120:128],msg[96:104],msg[104:112],msg[112:120]=msg[96:104],msg[104:112],msg[112:120],msg[120:128]
	return(msg)


def aes_round(input_array, output_array, keylist):
	output_array = sub_bytes(input_array)

	#shiftrow
	output_array = shift_rows(output_array)

	#mix columns
	from mix_columns import mix_columns
	for start_byte in range(0,32,8):
		column = []
		for i in range(4):
			column += output_array[i*64 + start_byte: i*64 + start_byte+8]

		new_column = [i for i in range(32)] ##Initialize y to 32 bits
		ancilla60 = [i for i in range(60)] ##initialize ancilla to 60 bits

		mix_columns(column, new_column, ancilla60)
	add_round_key(output_array,round_number, key)

def mix_columns_inverse(column, new_column, ancilla):
	pass

def aes_round_inverse(input_array, output_array, keylist):
	## ROUND KEY?
	for start_byte in range(0,32,8):
		column = []
		for i in range(4):
			column += output_array[i*64 + start_byte: i*64 + start_byte+8]
		mix_columns_inverse(column, new_column, ancilla)
	output_array = shift_rows_inverse(output_array)
	output_array = sub_bytes_inverse(output_array)

def aes_encrypt(msg, first_array, second_array, key):
	'''
	input -> first_array
	first_array -> second_array
	'''
	keylist = key_expansion(key)
	add_round_key(msg,keylist.pop(0)) #necessary?

	aes_round(msg, first_array, keylist) #r1

	aes_round(first_array, second_array, keylist) #r2
	aes_round_inverse(second_array, first_array, keylist)#r1'
	aes_round(second_array, first_array, keylist)#r3
	aes_round_inverse(first_array, second_array, keylist)#r2'
	aes_round(first_array, second_array, keylist)#r4
	aes_round_inverse(second_array, first_array, keylist)#r3'

	aes_round(second_array, first_array, keylist)#r5
	aes_round_inverse(first_array, second_array, keylist)#r4'
	aes_round(first_array, second_array, keylist)#r6
	aes_round_inverse(second_array, first_array, keylist)#r5'
	aes_round(second_array, first_array, keylist)#r7
	aes_round_inverse(first_array, second_array, keylist)#r6'
	aes_round(first_array, second_array, keylist)#r8
	aes_round_inverse(second_array, first_array, keylist)#r7'
	aes_round(second_array, first_array, keylist)#r9
	aes_round_inverse(first_array, second_array, keylist)#r8'
	aes_round(first_array, second_array, keylist)#r10
	aes_round_inverse(second_array, first_array, keylist)#r9'


	msg = sub_bytes(msg)
	shift_rows(msg)
	add_round_key(msg,keylist.pop(0))





