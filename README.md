# SSH Agent Setup

Sometimes you want to run some SSH subprocesses. It is convenient to use `ssh-agent` to hold your keys instead of passing them as arguments to said subprocesses. However, `ssh-agent` is not always available with zero configuration, due to various environment issues. This library offers an easy way to make sure you have `ssh-agent` at your disposal.

# Installation

    pip install ssh-agent-setup

# Features

Make sure `ssh-agent` is available (start one if needed)

```python
import ssh_agent_setup
ssh_agent_setup.setup()
```

Add a private key (and identity) to the `ssh-agent`:

```python
ssh_agent_setup.addKey( '/path/to/my_key_rsa' )
```

If an `ssh-agent` was started by `ssh_agent_setup`, it will be killed when the process exists via `atexit`.
