# Copyright 2013, AnsibleWorks Inc.
# Michael DeHaan <michael@ansibleworks.com>
# Chris Church <cchurch@ansibleworks.com>
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

import JobTemplateBaseCommand
import awx_cli.common as common


class JobTemplateReplaceCommand(JobTemplateBaseCommand.JobTemplateBaseCommand):

    """ replace job template """

    def __init__(self, toplevel):
        super(JobTemplateReplaceCommand, self).__init__(toplevel)
        self.name = "jobtemplatereplace"

    def get_parser(self):
        parser = super(JobTemplateReplaceCommand, self).get_parser()
        parser.add_option('--id', type="int")
        return parser

    def get_missing_option_errors(self, options):
        # All fields required when replacing, as well as an id.
        super_method = super(JobTemplateReplaceCommand, self)
        errors = super_method.get_missing_option_errors(options)
        if options.id is None:
            errors.append("--id is required")
        return errors

    def make_requests(self, handle, options):
        data = self.get_request_data_with_defaults(options)
        url = "/api/v1/job_templates/%s/" % options.id
        result = handle.patch(url, data)
        print common.dump(result)
