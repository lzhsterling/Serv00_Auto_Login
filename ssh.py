import os
import json
import paramiko
import requests

# 从环境变量中读取 ACCOUNTS_JSON
accounts_json = os.getenv('ACCOUNTS')
accounts = json.loads(accounts_json)

# 尝试通过SSH连接的函数
def ssh_connect(host, username, password, bark):
    transport = None
    try:
        transport = paramiko.Transport((host, 22))
        transport.connect(username=username, password=password)
        ssh_status = "SSH连接成功"
        print(f"SSH连接成功。")
	
	# Exécuter la commande pm2 resurrect
        ssh = transport.open_channel(kind='session')
        ssh.exec_command('./home/username/.npm-global/bin/pm2 resurrect')
        stdout = ssh.makefile('rb', -1)
        stderr = ssh.makefile_stderr('rb', -1)
        output = stdout.read().decode().strip()
        error = stderr.read().decode().strip()
        if error:
            print(f"Erreur lors de l'exécution de la commande : {error}")
        else:
            print(f"PM2保活成功，已重启.")

        if bark:
            url = f"https://api.day.app/{bark}/Serv00自动登录/账号 {username} SSH连接成功。"
            response = requests.get(url)
    except Exception as e:
        ssh_status = f"SSH连接失败，错误信息: {e}"
        print(f"SSH连接失败: {e}")
       
        
        if bark:
            url = f"https://api.day.app/{bark}/Serv00自动登录/账号 {username} SSH连接失败，请检查账号和密码是否正确。"
            response = requests.get(url)
    finally:
        if transport is not None:
            transport.close()

# 循环执行任务
for account in accounts:
    ssh_connect(account['host'], account['username'], account['password'], account["bark"])
