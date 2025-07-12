import paramiko
import socket
import datetime
import threading

host_key = paramiko.RSAKey(filename='server.key')

class Honeypot(paramiko.ServerInterface):
    def __init__(self, client_ip):
        self.client_ip = client_ip
    
    def check_auth_password(self, username, password):
        timestamp = datetime.datetime.now().isoformat()
        with open("login.txt", "a") as log:
            log.write(f"[{timestamp}] {self.client_ip} - USER: {username} | PASS: {password}\n")
        return paramiko.AUTH_SUCCESS
    
    def get_allowed_auths(self, username):
        return "password"
    
    def check_channel_request(self, kind, chanid):
        return paramiko.OPEN_SUCCEEDED if kind == "session" else paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
    
    