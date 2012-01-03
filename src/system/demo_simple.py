import base64
import getpass
import os
import socket
import sys
import traceback

import paramiko
import interactive


print('This is a simple paramiko demo')
print('This will use interactive')
# setup logging
paramiko.util.log_to_file('demo_simple.log')

# get hostname
username = ''
if len(sys.argv) > 1:
    hostname = sys.argv[1]
    if hostname.find('@') >= 0:
        username, hostname = hostname.split('@')
else:
    hostname = raw_input('Hostname: ')
if len(hostname) == 0:
    print '*** Hostname required.'
    sys.exit(1)
port = 22
if hostname.find(':') >= 0:
    hostname, portstr = hostname.split(':')
    port = int(portstr)


# get username
if username == '':
    default_username = getpass.getuser()
    username = raw_input('Username [%s]: ' % default_username)
    if len(username) == 0:
        username = default_username
password = getpass.getpass('Password for %s@%s: ' % (username, hostname))


# now, connect and use paramiko Client to negotiate SSH2 across the connection
try:
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.WarningPolicy)
    print '*** Connecting...'
    client.connect(hostname, port, username, password)
    chan = client.invoke_shell()
    print repr(client.get_transport())
    print '*** Here we go!'
    print
    #interactive.interactive_shell(chan)

    chan.close()
    client.close()

except Exception, e:
    print '*** Caught exception: %s: %s' % (e.__class__, e)
    traceback.print_exc()
    try:
        client.close()
    except:
        pass
    sys.exit(1)
