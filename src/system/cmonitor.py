import base64
import getpass
import os
import socket
import sys
import traceback

import paramiko
import interactive

class CMonitorWorker():
  def connect(self):
    pass

  def do_work(self):
    pass


class ProcessMonitor(CMonitorWorker):
  def connect(self):
    try:
      username = 'jboss'
      hostname = 'srvdmz2'
      port = 22
      password = 'nolosabe'
      self.client = paramiko.SSHClient()

      self.client.load_system_host_keys()
      self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
      if password == '':
        # ask for one on stdin
        password = getpass.getpass('Password for %s@%s: ' % (username, hostname))
      
      self.client.connect(hostname, port, username, password)
      self.transport = self.client.get_transport()
      self.chan = None

    except Exception, e:
      print '*** Caught exception: %s: %s' % (e.__class__, e)
      traceback.print_exc()
      try:
        self.client.close()
      except:
        pass

  def do_work(self):
    self.chan = self.transport.open_session()
    self.chan.exec_command('ps -ef | grep httpd | wc -l')
    result = self.chan.recv(1024)
    return result

  def close(self):
    if self.chan:
      self.chan.close()
    if self.client:
      self.client.close()

if __name__ == '__main__':
  pm = ProcessMonitor()
  pm.connect()
  print(pm.do_work())
  pm.close()