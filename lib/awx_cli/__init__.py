# Copyright 2013, AnsibleWorks Inc.
# Michael DeHaan <michael@ansibleworks.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# TODO: add a plugin loader sometime
from commands.VersionCommand import VersionCommand
from commands.JobLaunchCommand import JobLaunchCommand
from commands.JobTemplateCreateCommand import JobTemplateCreateCommand
from commands.JobTemplateReplaceCommand import JobTemplateReplaceCommand
from commands.JobTemplateEditCommand import JobTemplateEditCommand
from commands.JobTemplateDeleteCommand import JobTemplateDeleteCommand

import sys

__version__ = "1.3.0"
__author__ = "Michael DeHaan"

class AwxCli:

    def __init__(self):
        """ constructs the top level control system for the AWX CLI """

        self.commands = [
            JobLaunchCommand(self),
            JobTemplateCreateCommand(self),
            JobTemplateReplaceCommand(self),
            JobTemplateEditCommand(self),
            JobTemplateDeleteCommand(self),
            # awx-cli version
            VersionCommand(self),
        ]

    def show_commands(self):
        """ all available commands to the screen """

        for name in self.get_command_names():
            print name
        print ""

    def get_command_names(self):
        """ get the names of all the commands """

        return [ command.name for command in self.commands ]

    def get_commands(self):
        """ return all of the available commands """

        return [ self.commands ]

    def activate(self, args):
        """ find what command class to use """

        length = len(sys.argv)
        if length < 2:
            return self.show_commands()
        elif length == 2 and sys.argv[1] == "--help":
            return self.show_commands()
        else:
            first = sys.argv[1]
            for cmd in self.commands:
                if cmd.name == first:
                   return cmd.run(args[1:])
            raise common.CommandNotFound("unknown command: %s" % first)
