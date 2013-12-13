import BaseCommand
import awx_cli.common as common


class JobTemplateBaseCommand(BaseCommand.BaseCommand):

    def run(self, args):
        # Subclasses should not have to override this method.
        parser = self.get_parser()
        (options, args) = parser.parse_args()
        option_errors = self.get_missing_option_errors(options)
        if option_errors:
            raise common.BaseException(", ".join(option_errors))

        handle = common.connect(options)
        self.make_requests(handle, options)
        return 0

    def make_requests(self, handle, options):
        raise NotImplementedError("implement in subclass")

    def get_parser(self):
        parser = common.get_parser()
        parser.add_option('--allow-callbacks', dest="callbacks",
                          action="store_true")
        parser.add_option('--disable-callbacks', dest="callbacks",
                          action="store_false")
        parser.add_option('--cloud-credential', type="int")
        parser.add_option('--credential', type="int")
        parser.add_option('--description', type="str")
        parser.add_option('--extra-vars', type="str")
        parser.add_option('--forks', type="int")
        parser.add_option('--host-config-key', type="str")
        parser.add_option('--inventory', type="int")
        parser.add_option('--job-tags', type="str")
        parser.add_option('--job-type', type="str")
        parser.add_option('--limit', type="str")
        parser.add_option('--name', type="str")
        parser.add_option('--playbook', type="str")
        parser.add_option('--project', type="int")
        parser.add_option('--verbosity', type="str")
        return parser

    def get_request_data_fields(self):
        "Get list of (request key, option dest, default value) tuples. "
        return [
            ("allow_callbacks", "callbacks", False),
            ("cloud_credential", "cloud_credential", ""),
            ("credential", "credential", None),
            ("description", "description", ""),
            ("extra_vars", "extra_vars", ""),
            ("forks", "forks", 0),
            ("host_config_key", "host_config_key", ""),
            ("inventory", "inventory", None),
            ("job_tags", "job_tags", ""),
            ("job_type", "job_type", "run"),
            ("limit", "limit", ""),
            ("name", "name", None),
            ("playbook", "playbook", None),
            ("project", "project", None),
            ("verbosity", "verbosity", "0"),
        ]

    # get_request_data_with_defaults(options) is clearer than
    # get_request_data(options, True) and a default value for
    # add_defaults may lead to subtle bugs.

    def get_request_data_with_defaults(self, options):
        return self.get_request_data(options, True)

    def get_request_data_no_defaults(self, options):
        return self.get_request_data(options, False)

    def get_request_data(self, options, add_defaults):
        data = {}
        for key, option, default in self.get_request_data_fields():
            val = getattr(options, option)

            # Add default value if we should.
            if val is None and add_defaults:
                if default is None:
                    raise ValueError("no default value for %s" % option)
                val = default

            if val is not None:
                data[key] = val

        return data

    def get_missing_option_errors(self, options):
        errors = []

        if options.credential is None:
            errors.append("--credential is required")

        if options.inventory is None:
            errors.append("--inventory is required")

        if options.callbacks is True and options.host_config_key is None:
            errors.append("--host-config-key is required")

        if options.name is None:
            errors.append("--name is required")

        if options.playbook is None:
            errors.append("--playbook is required")

        if options.project is None:
            errors.append("--project is required")

        return errors

