from setuptools import setup, find_packages

README = 'set up a working ssh-agent and add keys for any subprocesses you want to run'

requires = []

setup(name='ssh-agent-setup',
      version='1.0.0',
      description=README,
      long_description=README,
      url='https://github.com/haarcuba/ssh-agent-setup',
      classifiers=[
          "Programming Language :: Python",
      ],
      author='Yoav Kleinberger',
      author_email='haarcuba@gmail.com',
      packages=find_packages(),
      keywords='SSH, SSH Agent, ssh-agent',
      entry_points = {},
      zip_safe=False,
      install_requires=requires,
      )
