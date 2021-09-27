import re

_OUTPUT_PATTERN = re.compile(r'SSH_AUTH_SOCK=(?P<SSH_AUTH_SOCK>[^;]+).*SSH_AGENT_PID=(?P<SSH_AGENT_PID>\d+)', re.MULTILINE | re.DOTALL)

def parse(output):
    match = _OUTPUT_PATTERN.search(output)
    if match is None:
        raise Exception(f'Could not parse ssh-agent output. It was: {output}')
    return match.groupdict()
