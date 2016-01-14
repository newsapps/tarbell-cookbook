#!/usr/bin/env pyton
"""
Get Tarbell settings and site outside of a Blueprint, hook or view

I figured out how to do this by looking at the implementation of some
of the CLI commands at

https://github.com/tarbell-project/tarbell/blob/1.0.4/tarbell/cli.py

I'm not positive, but I'm pretty sure this script has to live and/or
be run from the root of a Tarbell project.
"""

from tarbell.contextmanagers import ensure_settings, ensure_project

class MockCommand(object):
    """Mock class that mimics the necessary API of the Tarbell CLI commands"""
    name = "mock"

if __name__ == "__main__":
    mock_command = MockCommand()
    args = []
    with ensure_settings(mock_command, args) as settings, ensure_project(mock_command, args) as site:
        # Do stuff with settings, site
        pass
