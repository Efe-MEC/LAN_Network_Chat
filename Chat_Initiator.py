import json
import os
import time


ip_file = "ip.json"


def main ():

	while True:

		op_code = input("Please enter the operation code:\nUsers (1)\nChat (2)\nHistory (3)\n")

		if op_code == "1":
			print("Users")
		elif op_code == "2":
			print("Chat")
		elif op_code == "3":
			print("History")
		else:
			print("Invalid operation code. Enter 1, 2 or 3.")