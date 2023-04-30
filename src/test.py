import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("walter",username="walter",password="Walter")
stdin, stdout, stderr = ssh.exec_command("sus")
print(stdout.read())