import paramiko,sys,os,socket,select,getpass,termios,tty
import time
from paramiko.py3compat import u
from fLoging import fortressLogger
import re



def serverInfo():
    pass

class SSHConnect(object):
    def __init__(self,host,port,username,password=None,key=None,logger=None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.key = key
        self.logger = logger
        try:
            client_ip = os.environ['SSH_CLIENT']
        except:
            client_ip = "IP"
        self.logger.extra={'username':getpass.getuser(),'ip':client_ip}
        self.is_debug = True


    def _debug(self,msg):
        if self.is_debug:
            time_stf = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
            print("[%s] [debug] %s" % (time_stf,msg))



    def run(self):
        conn,res = self.__startSession()
        if conn is not True:
            self._debug(res)
            self.logger.error(res)
            sys.exit(1)
        else:
            self._debug(res)
            self.logger.info(res)
            pass

        self.__execCommand()
        self.__transClose()

    def __startSession(self):
        self._debug("start connect %s" % self.host)
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
            return [False,"Password or Private Key Is Null"]
        self.chan = self.trans.open_session()
        self.chan.get_pty()
        self.chan.invoke_shell()
        self.oldtty = termios.tcgetattr(sys.stdin)
        return [True,'Connect Success']


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
                            self._debug('End of Connectioon,Exit Connection')
                            self.logger.info('End of Connection, Exit Connection')
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
                        self.logger.info(''.join(command_list).rstrip('\r\n'))
                        self._debug(''.join(command_list))
                        command_list.clear()

                    self.chan.send(x)
        finally:
           termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.oldtty)



if __name__ == '__main__':
    host = '192.168.8.201'
    port = 22
    username = 'root'
    passwrod = None

    logger = fortressLogger.flogger()
    key = os.path.join(os.environ['HOME'],'./.ssh/id_rsa')
    s = SSHConnect(host,port,username,passwrod,key,logger)
    s.run()