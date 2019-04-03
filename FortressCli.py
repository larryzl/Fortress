import paramiko,sys,os,socket,select,getpass,termios,tty
from paramiko.py3compat import u
# from fLoging import logger
import re

def serverInfo():
    pass






class SSHConnect(object):
    def __init__(self,host,port,username,password=None,key=None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.key = key
        self.user = getpass.getuser()


    def currentSessionInfo(self):
        self.__getOSType()
        if self.os == 'centos':
            with open('/var/log/secure') as f:
                session_info = f.readlines()[-2]
            comp = re.compile(r'^.* from (?P<ip>) port.*$')
            try:
                ip = comp.match(session_info).groupdict()[ip]
            except:
                ip = ''




    def __getOSType(self):
        import platform
        os_info = platform.platform(True)
        if 'centos' in os_info:
            self.os = 'centos'
        elif 'Ubuntu' in os_info:
            self.os = 'ubuntu'
        elif 'Darwin' in os_info:
            self.os = 'mac'


    def run(self):
        conn,res = self.__startSession()
        if conn is not True:
            # logger.error(res)
            sys.exit(1)
        else:
            pass
            # logger.info(res)

        self.__execCommand()
        self.__transClose()

    def __startSession(self):

        self.trans = paramiko.Transport((self.host,self.port))
        self.trans.start_client()
        if self.password is not None:
            try:
                self.trans.auth_password(self.username,self.password)
            except Exception as e:
                return [False,e]
        elif self.key is not None:
            try:
                private_key = paramiko.RSAKey.from_private_key_file(self.key)
                self.trans.auth_publickey(username=self.username,key=private_key)
            except Exception as e:
                return [False,e]
        else:
            return [False,"密码或秘钥为空"]
        self.chan = self.trans.open_session()
        self.chan.get_pty()
        self.chan.invoke_shell()
        self.oldtty = termios.tcgetattr(sys.stdin)
        return [True,'连接成功']


    def __transClose(self):
        self.trans.close()
        self.chan.close()

    def __execCommand(self):
        try:
            tty.setraw(sys.stdin.fileno())
            self.chan.settimeout(0.0)
            tab_flag = False
            command_list = []
            while True:
                r,w,e = select.select([self.chan,sys.stdin],[],[],1)
                if self.chan in r:
                    try:
                        x = u(self.chan.recv(1024))

                        if len(x) == 0:
                            # logger.info('*** End of Connection, Exit Connection***')
                            break
                        if tab_flag:
                            if x.startswith('\r\n'):
                                pass
                            else:
                                command_list.append(x)
                            tab_flag = False
                        sys.stdout.write(x)
                        sys.stdout.flush()
                    except socket.timeout:
                        pass
                if sys.stdin in r:
                    x = sys.stdin.read(1)
                    if len(x) == 0:
                        break
                    if x == '\t':
                        tab_flag = True
                    else:
                        command_list.append(x)
                    if x == '\r':
                        # print(''.join(command_list))
                        # logger.info(''.join(command_list))
                        command_list.clear()

                    self.chan.send(x)
        finally:
           termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.oldtty)



if __name__ == '__main__':
    host = '192.168.8.201'
    port = 22
    username = 'root'
    passwrod = None
    key = '/Users/lei/.ssh/id_rsa'

    s = SSHConnect(host,port,username,passwrod,key)
    s.run()