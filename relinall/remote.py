from relinall.window import *

class Remote(Window):

    def __init__(self):
        super().__init__()
        print("Remote")

    def remote(self):

        self.docker()
        self.tabber('remote')


import paramiko

class CLIAccess:
    def __init__(self,server):
        self.IPAddress=server['IP']
        self.Uname=server['Uname']
        self.Pword=server['Pword']

    def connectServer(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.ssh.connect(self.IPAddress, username=self.Uname, password=self.Pword)
            print("########################")
            print("#  connection Success  #")
            print("########################\n")
        except paramiko.SSHException:
            print("########################")
            print("#  connection Failed  #")
            print("########################\n")
            quit()

    def executeCommand(self,cmd):
        self.result='The Command Received is : '+cmd+'\n'
        self.result+='-------------------------\n'
        self.stdin, self.stdout, self.stderr = self.ssh.exec_command(cmd)
        self.cmd_op=self.stdout.read()
        self.result+=self.cmd_op.decode('utf-8')
        return(self.result)

server_details={'IP':'172.30.60.48','Uname':'root','Pword':'msys#123'}
result=CLIAccess(server_details)
result.connectServer()

output=""
#output+=result.executeCommand("ls")
output+=result.executeCommand("ifconfig")
import pdb
#pdb.set_trace()
print(type(output),output)
import re
ipaddr=re.findall("(?<=inet)(.*)(?=netmask)",output)
print(ipaddr)
output+=result.executeCommand("exit")
