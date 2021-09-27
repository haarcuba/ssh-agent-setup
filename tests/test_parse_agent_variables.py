import pytest
from ssh_agent_setup import parse_agent_variables


def test_parser():
    EXAMPLE_OUTPUT =    "SSH_AUTH_SOCK=/tmp/ssh-QQ0LK6EvhQS1/agent.3313844; export SSH_AUTH_SOCK;\n"\
                        "SSH_AGENT_PID=3313845; export SSH_AGENT_PID;\n"\
                        "echo Agent pid 3313845;"
    environment_variables = parse_agent_variables.parse(EXAMPLE_OUTPUT)
    assert environment_variables['SSH_AUTH_SOCK'] == '/tmp/ssh-QQ0LK6EvhQS1/agent.3313844'
    assert environment_variables['SSH_AGENT_PID'] == '3313845'

def test_raise_if_output_is_bad():
    with pytest.raises(Exception, match='ssh-agent.*some bad string'):
        parse_agent_variables.parse('some bad string')


