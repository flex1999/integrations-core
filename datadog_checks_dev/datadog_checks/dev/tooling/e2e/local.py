# (C) Datadog, Inc. 2018
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import os
import re

import click
from shutil import copyfile, move

from .agent import (
    AGENT_CMD, DEFAULT_AGENT_VERSION, FAKE_API_KEY, MANIFEST_VERSION_PATTERN,
    get_agent_conf_dir, get_agent_exe,
    get_agent_service_cmd, get_agent_version_manifest,
    get_rate_flag
)
from .config import (
    config_file_name, locate_config_dir, locate_config_file, write_env_data, remove_env_data
)
from .platform import LINUX, MAC, WINDOWS
from ..constants import get_root
from ..commands.console import echo_info
from ...utils import ON_MACOS, ON_WINDOWS, ON_LINUX, path_join, file_exists
from ...subprocess import run_command


class LocalAgentInterface(object):
    def __init__(self, check, env, base_package=None, config=None, metadata=None, agent_build=None, api_key=None):
        self.check = check
        self.env = env
        self.base_package = base_package
        self.config = config or {}
        self.metadata = metadata or {}
        self.agent_build = agent_build
        self.api_key = api_key or FAKE_API_KEY

        self._agent_version = self.metadata.get('agent_version')
        self.config_dir = locate_config_dir(check, env)
        self.config_file = locate_config_file(check, env)
        self.config_file_name = config_file_name(self.check)

    @property
    def platform(self):
        if ON_LINUX:
            return LINUX
        elif ON_MACOS:
            return MAC
        elif ON_WINDOWS:
            return WINDOWS
        else:
            raise Exception("Unsupported OS for Local E2E")

    @property
    def agent_version(self):
        return self._agent_version or DEFAULT_AGENT_VERSION

    @property
    def agent_command(self):
        return '{}'.format(get_agent_exe(self.agent_version, platform=self.platform))

    def write_config(self):
        write_env_data(self.check, self.env, self.config, self.metadata)
        self.copy_config_to_local_agent()

    def remove_config(self):
        remove_env_data(self.check, self.env)
        self.remove_config_from_local_agent()

    def copy_config_to_local_agent(self):
        check_conf_file = os.path.join(
            get_agent_conf_dir(self.check, self.agent_version, self.platform),
            '{}.yaml'.format(self.check)
        )
        if file_exists(check_conf_file):
            copyfile(check_conf_file, '{}.bak'.format(check_conf_file))
        copyfile(self.config_file, check_conf_file)

    def remove_config_from_local_agent(self):
        check_conf_file = os.path.join(
            get_agent_conf_dir(self.check, self.agent_version, self.platform),
            '{}.yaml'.format(self.check)
        )
        backup_conf_file = '{}.bak'.format(check_conf_file)
        os.remove(check_conf_file)
        if file_exists(backup_conf_file):
            move(backup_conf_file, check_conf_file)

    def run_check(self, capture=False, rate=False):
        command = '{} check {}{}'.format(
            self.agent_command,
            self.check,
            ' {}'.format(get_rate_flag(self.agent_version)) if rate else ''
        )
        return run_command(command, capture=capture)

    def update_check(self):
        value = click.confirm('Env will started with an editable check install for the {} package. \
This check will remain in an editable install after \
the environment is torn down. Would you like to proceed? '.format(self.check))
        if value:
            import pdb; pdb.set_trace()
            install_cmd = AGENT_CMD[self.platform]['pip_install'] + ['-e',  path_join(get_root(), self.check)]
            return run_command(install_cmd, capture=True, check=True)
        else:
            return

    def update_base_package(self):
        value = click.confirm('Env will started with an editable check install for the base package. \
This check will remain in an editable install after \
the environment is torn down. Would you like to proceed? ')
        if value:
            install_cmd = AGENT_CMD[self.platform]['pip_install'] + ['-e', self.base_package]
            run_command(install_cmd, capture=True, check=True)
        else:
            return

    def update_agent(self):
        # The Local E2E assumes an Agent is already installed on the machine
        echo_info("Using the locally installed Agent")

    def detect_agent_version(self):
        if self.agent_build and self._agent_version is None:
            with open(get_agent_version_manifest(self.platform)) as f:
                ver = f.readline()
                match = re.search(MANIFEST_VERSION_PATTERN, ver)
            if match:
                self._agent_version = int(match.group(1))

            self.metadata['agent_version'] = self.agent_version

    def start_agent(self):
        command = get_agent_service_cmd(self.agent_version, self.platform, 'start')
        return run_command(command, capture=True)

    def stop_agent(self):
        command = get_agent_service_cmd(self.agent_version, self.platform, 'stop')
        run_command(command, capture=True)