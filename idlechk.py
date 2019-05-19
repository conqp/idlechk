"""A system service to check whether the system is idle."""

from json import load
from logging import getLogger
from pathlib import Path
from subprocess import CalledProcessError, check_call
from sys import argv


__all__ = ['main']


CONFIG_FILE = Path('/etc/idlechk.json')
LOGGER = getLogger(Path(argv[0]).name)


def log_info(what, name):
    """Logs information abount current actions."""

    if name:
        LOGGER.info('%s: %s.', what, name)
    else:
        LOGGER.info('%s.', what)


def load_config():
    """Loads the configuration."""

    try:
        with CONFIG_FILE.open('r') as file:
            return load(file)
    except FileNotFoundError:
        return ()


def run(action):
    """Runs the respective action."""

    command = action.get('command')

    if isinstance(command, bool):
        return command

    if isinstance(command, list):
        try:
            check_call(command)
        except CalledProcessError:
            return False

        return True

    if isinstance(command, str):
        LOGGER.warning('Running insecure command in shell.')

        try:
            check_call(command, shell=True)
        except CalledProcessError:
            return False

        return True

    raise TypeError('Cannot run command of type %s.' % type(command))


def check_condition(condition):
    """Checks the respective condition."""

    name = condition.get('name')
    log_info('Checking condition', name)
    return run(condition)


def run_action(action):
    """Runs the respective action."""

    name = action.get('name')
    log_info('Running action', name)
    return run(action)


def run_check(check):
    """Runs the respective check."""

    name = check.get('name')
    log_info('Running check', name)
    action = check.get('action')

    for condition in check.get('conditions', ()):
        if check_condition(condition):
            if condition.get('sufficient', False):
                LOGGER.info('Sufficient condition succeeded.')
                break
        else:
            if condition.get('necessary', False):
                LOGGER.info('Necessary condition failed.')
                return

    run_action(action)


def main():
    """Runs the respective checks."""

    for check in load_config():
        run_check(check)
