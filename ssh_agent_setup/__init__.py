import subprocess
import logging
import os
import re
import atexit


def _kill_agent():
    logging.info('killing previously started ssh-agent')
    subprocess.run(['ssh-agent', '-k'])
    del os.environ['SSH_AUTH_SOCK']
    del os.environ['SSH_AGENT_PID']


def _setup_agent():
    process = subprocess.run(['ssh-agent', '-s'], stdout=subprocess.PIPE, text=True)
    OUTPUT_PATTERN = re.compile('SSH_AUTH_SOCK=(?P<socket>[^;]+).*SSH_AGENT_PID=(?P<pid>\d+)', re.MULTILINE | re.DOTALL)
    match = OUTPUT_PATTERN.search(process.stdout)
    if match is None:
        raise Exception('Could not parse ssh-agent output. It was: {}'.format(process.stdout))
    agent_data = match.groupdict()
    logging.info('ssh agent data: {}'.format(agent_data))
    logging.info('exporting ssh agent environment variables')
    os.environ['SSH_AUTH_SOCK'] = agent_data['socket']
    os.environ['SSH_AGENT_PID'] = agent_data['pid']
    atexit.register(_kill_agent)


def agent_up():
    return os.environ.get('SSH_AUTH_SOCK') is not None


def setup():
    if agent_up():
        logging.info('ssh-agent already present')
    else:
        logging.info('ssh-agent not present, will now set it up')
        _setup_agent()


def add_key(key_file):
    process = subprocess.run(['ssh-add', key_file])
    if process.returncode != 0:
        raise Exception('failed to add the key: {}'.format(key_file))
