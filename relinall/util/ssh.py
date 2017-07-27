import paramiko

class Ssh():

	def connect(hostname, username, password):
		
		error = None

		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		try:
			
			ssh.connect(hostname, username=username, password=password, auth_timeout=5.0, timeout=5.0)
			# ssh.connect('8.8.8.8', username='root', password='msys#123', auth_timeout=5.0, timeout=5.0)
			
		except Exception:
			error = True

		return ssh, error
		
	def execute(ssh, cmd):
		stdin, stdout, stderr = ssh.exec_command(cmd)

		cmd_op = stdout.read()
		result = '----------'
		result += cmd_op.decode('utf-8')
		print(result)