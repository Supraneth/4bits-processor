#!/usr/bin/python3
# coding: utf-8

import argparse
import os

# 4 write_reg input
# 4 address RAM
# 2 select input reg
# 2 choix registre input
# 4 Reset
# 1 enable write register
# 2 Output 1
# 2 Output 2
# 2 Operations
# 1 Enable RAM
# 1 write RAM
# 1 clear RAM

def read_and_convert(filename):
	destination_file, extension = os.path.splitext(filename)
	destination_file = destination_file + ".bin"

	bin = []

	with open(filename) as source_file:
		lines = source_file.readlines()

	for line in lines:
		if "LD" in line:
			bin.append(load_value(line[3:]))
		elif "AND" in line:
			bin.append(operation("AND", line[4:]))
		elif "XOR" in line:
			bin.append(operation("XOR", line[4:]))
		elif "OR" in line:
			bin.append(operation("OR", line[3:]))
		elif "ADD" in line:
			bin.append(operation("ADD", line[4:]))
		elif "RST" in line:
			bin.append(reset())
    #END FOR
	bin_file = open(destination_file, 'w')
	bin_file.write('v2.0 raw' + "\n")

	for value in bin:
		bin_file.write("{:07}".format(int(hex(int(value, 2)), 16)) + "\n")
		print(value)
		print("{:07}".format(int(hex(int(value, 2)), 16)))
	#END FOR

	bin_file.close()

def load_value(line):
	write_reg_input = "0000"
	address_RAM = "0000"
	select_input_reg = "00"
	choix_registre_input = "00"
	reset = "0000"
	enable_write_register = "0"
	output_1 = "00"
	output_2 = "00"
	operations = "00"
	enable_RAM = "0"
	write_RAM = "0"
	clear_RAM = "0"

	if line[0] == "R":
		choix_registre_input = get_value(line[0:2])
		enable_write_register = "1"

		if line[3] == "R":
			select_input_reg = "00"
			output_1 = get_value(line[4:6])
		elif line[4] == "@":
			select_input_reg = "01"
			address_RAM = get_value(line[4:8])
		else:
			write_reg_input = '{0:04b}'.format(int(line[4:]))

	return write_reg_input + address_RAM + select_input_reg + choix_registre_input + reset + enable_write_register + output_1 + output_2 + operations + enable_RAM + write_RAM + clear_RAM

def operation(operand, line):
	write_reg_input = "0000"
	address_RAM = "0000"
	select_input_reg = "00"
	choix_registre_input = "00"
	reset = "0000"
	enable_write_register = "0"
	output_1 = "00"
	output_2 = "00"
	operations = "00"
	enable_RAM = "0"
	write_RAM = "0"
	clear_RAM = "0"

	if line[0] == "R" and line[4] == "R":
		if operand == "AND":
			operations = "00"
		elif operand == "OR":
			operations = "01"
		elif operand == "XOR":
			operations = "10"
		elif operand == "ADD":
			operations = "11"

		output_1 = get_value(line[0:2])
		output_2 = get_value(line[4:6])

		if line[8] == "R":
			enable_write_register = "1"
			choix_registre_input = get_value(line[8:10])
		elif line[8] == "@":
			enable_RAM = "1"
			write_RAM = "1"
			address_RAM = get_value(line[8:11])

	return write_reg_input + address_RAM + select_input_reg + choix_registre_input + reset + enable_write_register + output_1 + output_2 + operations + enable_RAM + write_RAM + clear_RAM

def reset():
	write_reg_input = "0000"
	address_RAM = "0000"
	select_input_reg = "00"
	choix_registre_input = "00"
	reset = "0000"
	enable_write_register = "1"
	output_1 = "00"
	output_2 = "00"
	operations = "00"
	enable_RAM = "1"
	write_RAM = "1"
	clear_RAM = "1"

	return write_reg_input + address_RAM + select_input_reg + choix_registre_input + reset + enable_write_register + output_1 + output_2 + operations + enable_RAM + write_RAM + clear_RAM

def get_value(value):
	if value[0] == "R":
		return '{0:02b}'.format(int(value[1:]))
	elif value[0] == "@":
		return '{0:04b}'.format(int(value[1:]))

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Convert a pseudo ASM file to bin')
	parser.add_argument('file', type=str, help='File to convert')
	args = parser.parse_args()

	read_and_convert(args.file)
