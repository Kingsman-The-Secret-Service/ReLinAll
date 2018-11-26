import paramiko

class Ssh():

	def connect(hostname, username, password, port = 22):
		
		error = None

		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		try:
			ssh.connect(hostname, username=username, password=password, port=int(port), auth_timeout=5.0, timeout=5.0)
		except Exception as e:
			print(e)
			error = True
		# error = False
		# ssh = True

		print(ssh,error)
		return ssh, error
		
	def execute(ssh, cmd):


		stdin, stdout, stderr = ssh.exec_command(cmd)
		return stdout.read()


		cmd_op = stdout.read()
		result = '----------'
		result += cmd_op.decode('utf-8')
		print(result)