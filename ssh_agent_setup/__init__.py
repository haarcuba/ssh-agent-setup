import subprocess
import logging
import os
import re
import atexit

def _killAgent():
    logging.info( 'killing previously started ssh-agent' )
    subprocess.run( [ 'ssh-agent', '-k' ] )
    del os.environ[ 'SSH_AUTH_SOCK' ]
    del os.environ[ 'SSH_AGENT_PID' ]

def _setupAgent():
    process = subprocess.run( 'ssh-agent', stdout = subprocess.PIPE, universal_newlines = True )
    OUTPUT_PATTERN = re.compile(  'SSH_AUTH_SOCK=(?P<socket>[^;]+).*SSH_AGENT_PID=(?P<pid>\d+)', re.MULTILINE | re.DOTALL )
    match = OUTPUT_PATTERN.search( process.stdout )
    if match is None:
        raise Exception( 'Could not parse ssh-agent output. It was: {}'.format( process.stdout ) )
    agentData = match.groupdict()
    logging.info( 'ssh agent data: {}'.format( agentData ) )
    logging.info( 'exporting ssh agent environment variables' )
    os.environ[ 'SSH_AUTH_SOCK' ] = agentData[ 'socket' ]
    os.environ[ 'SSH_AGENT_PID' ] = agentData[ 'pid' ]
    atexit.register( _killAgent )

def agentUp():
    return os.environ.get( 'SSH_AUTH_SOCK' ) is not None

def setup():
    if agentUp():
        logging.info( 'ssh-agent already present' )
    else:
        logging.info( 'ssh-agent not present, will now set it up' )
        _setupAgent()

def addKey( keyFile ):
    process = subprocess.run( [ 'ssh-add', keyFile ] )
    if process.returncode != 0:
        raise Exception( 'failed to add the key: {}'.format( keyFile ) )
