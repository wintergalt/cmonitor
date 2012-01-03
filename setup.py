from distutils.core import setup

setup(name='cmonitor',
      version='0.1',
      url='http://www.colescba.org.ar',
      author='Diego Romoli',
      author_email='dromoli@colescba.org.ar',
      packages=['src.system'],
      requires=['PySide (>=1.0.7)', 'paramiko (>=1.7.6)'],
)