#!/usr/bin/env python

from __future__ import print_function, absolute_import, division

import argparse
import sys
import os
import re

from jinja2 import Template

import punch
from punch import config as cfr
from punch import file_updater as fu
from punch import replacer as rep
from punch import version as ver
from punch import action_register as ar
from punch import helpers as hlp
from punch.vcs_configuration import VCSConfiguration
from punch.vcs_repositories.exceptions import RepositorySystemError
from punch.vcs_repositories.novcs_repo import NoVCSRepo
from punch.vcs_repositories.git_flow_repo import GitFlowRepo
from punch.vcs_repositories.git_repo import GitRepo
from punch.vcs_repositories.hg_repo import HgRepo
from punch.vcs_use_cases.vcs_start_release import VCSStartReleaseUseCase
from punch.vcs_use_cases.vcs_finish_release import VCSFinishReleaseUseCase


def fatal_error(message, exception=None):
    print(message)
    if exception is not None:
        print("Exception {}: {}".format(
            exception.__class__.__name__,
            str(exception)
        ))
    sys.exit(1)


def select_vcs_repo_class(vcs_configuration):
    if vcs_configuration is None:
        repo_class = NoVCSRepo
    elif vcs_configuration.name == 'git':
        repo_class = GitRepo
    elif vcs_configuration.name == 'git-flow':
        repo_class = GitFlowRepo
    elif vcs_configuration.name == 'hg':
        repo_class = HgRepo
    else:
        fatal_error(
            "The requested version control" +
            " system {} is not supported.".format(
                vcs_configuration.name
            )
        )

    return repo_class


default_config_file_name = "punch_config.py"

default_config_file_content = """__config_version__ = 1

GLOBALS = {
    'serializer': '{{major}}.{{minor}}.{{patch}}',
}

FILES = []

VERSION = ['major', 'minor', 'patch']

VCS = {
    'name': 'git',
    'commit_message': (
        "Version updated from {{ current_version }}"
        " to {{ new_version }}")
}
"""

default_version_file_name = "punch_version.py"

default_version_file_content = """major = 0
minor = 1
patch = 0
"""

default_commit_message = \
    "Version update {{ current_version }} -> {{ new_version }}"


def show_version_parts(values):
    for p in values:
        print("{}={}".format(p.name, p.value))


def show_version_updates(version_changes):
    for current, new in version_changes.values():
        print("  - {} -> {}".format(current, new))


def init_config_files():
    if not os.path.exists(default_config_file_name):
        with open(default_config_file_name, 'w') as f:
            f.write(default_config_file_content)

    if not os.path.exists(default_version_file_name):
        with open(default_version_file_name, 'w') as f:
            f.write(default_version_file_content)


def args_initialize(args):
    if args.version is True:
        print("Punch version {}".format(punch.__version__))
        print("Copyright (C) 2016 Leonardo Giordani")
        print("This is free software, see the LICENSE file.")
        print("Source: https://github.com/lgiordani/punch")
        print("Documentation: http://punch.readthedocs.io/en/latest/")
        sys.exit(0)

    if args.init is True:
        init_config_files()
        sys.exit(0)

    if args.simulate:
        args.verbose = True


def args_check_options(args):
    if not any([args.part, args.set_part, args.action]):
        fatal_error("You must specify one of --part, --set-part, or --action")

    set_options = [
        i is not None for i in [args.part, args.set_part, args.action]
    ]
    if sum(set_options) > 1:
        fatal_error(
            "You can only specify one of --part, --set-part, or --action")

    if args.set_part and args.reset_on_set:
        set_parts = args.set_part.split(',')
        if len(set_parts) > 1:
            fatal_error(
                "If you specify --reset-on-set you may set only one value"
            )

    try:
        config = cfr.PunchConfig(args.config_file)
    except (cfr.ConfigurationVersionError, ValueError) as exc:
        fatal_error(
            "An error occurred while reading the configuration file.",
            exc
        )

    if len(config.files) == 0:
        fatal_error("You didn't configure any file")

    if args.part:
        args.action = "punch:increase"
        args.action_options = "part={}".format(args.part)
    elif args.set_part:
        args.action = "punch:set"
        args.action_options = args.set_part

    if args.action and args.action not in config.actions:
        fatal_error(
            "The requested action {} is not defined.".format(args.action)
        )

    return config


def create_action(args, config):
    action_dict = config.actions[args.action]

    try:
        action_name = action_dict.pop('type')
    except KeyError:
        fatal_error("The action configuration is missing the 'type' field.")

    if args.action_options:
        action_dict.update(hlp.optstr2dict(args.action_options))

    action_class = ar.ActionRegister.get(action_name)
    action = action_class(action_dict)

    return action


def check_release_notes(config, changes):
    wrong_release_notes = []
    new_versions = dict((n, v[1]) for n, v in changes.items())
    for file_name, regex_template in config.release_notes:
        template = Template(regex_template)
        render = template.render(**new_versions)
        with open(file_name, 'r') as f:
            content = f.read()
            if not re.search(render, content, re.MULTILINE):
                wrong_release_notes.append((file_name, regex_template, render))

    if len(wrong_release_notes):
        print("The following files have been configured to contain "
              "release notes, but they don't have an entry that matches "
              "the new version that Punch is about to create.")
        for file_name, regex_template, render in wrong_release_notes:
            print("  *", file_name)
            print("    - Template:", regex_template)
            print("    - Rendered:", render)
        fatal_error(
            "Please update the files and commit them if you use a VCS")


def main(original_args=None):
    parser = argparse.ArgumentParser(
        description="Manages file content with versions."
    )
    parser.add_argument('-c', '--config-file', action='store',
                        help="Config file", default=default_config_file_name)
    parser.add_argument('-v', '--version-file', action='store',
                        help="Version file", default=default_version_file_name)
    parser.add_argument('-p', '--part', action='store')
    parser.add_argument('--set-part', action='store')
    parser.add_argument('-a', '--action', action='store')
    parser.add_argument('--action-options', action='store')
    parser.add_argument('--action-flags', action='store')
    parser.add_argument('--reset-on-set', action='store_true')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='Ignore warnings')
    parser.add_argument('--verbose', action='store_true',
                        help="Be verbose")
    parser.add_argument('--version', action='store_true',
                        help="Print the Punch version and project information")
    parser.add_argument(
        '--init',
        action='store_true',
        help="Writes default initialization files" +
             " (does not overwrite existing ones)"
    )
    parser.add_argument(
        '-s',
        '--simulate',
        action='store_true',
        help="Simulates the version increment and" +
             " prints a summary of the relevant data (implies --verbose)"
    )

    args = parser.parse_args()

    # This is here just to avoid "can be not defined" messages by linters
    repo = None

    args_initialize(args)
    config = args_check_options(args)

    if args.verbose:
        print("## Punch version {}".format(punch.__version__))

    action = create_action(args, config)

    current_version = ver.Version.from_file(args.version_file, config.version)
    new_version = action.process_version(current_version)

    global_replacer = rep.Replacer(config.globals['serializer'])

    file_updaters = []
    for file_configuration in config.files:
        file_replacer = rep.Replacer(config.globals['serializer'])
        file_replacer.update(file_configuration.config['serializer'])
        file_updaters.append(fu.FileUpdater(file_configuration, file_replacer))

    if config.vcs is not None:
        try:
            current_version_string, new_version_string = \
                global_replacer.run_serializer(
                    config.vcs_serializer,
                    current_version.as_dict(),
                    new_version.as_dict()
                )
        except rep.MissingSerializer:
            fatal_error(
                "The requested serializer {} has not been declared".format(
                    config.vcs_serializer
                )
            )

        vcs_configuration = VCSConfiguration.from_dict(
            config.vcs,
            config.globals,
            {
                'current_version': current_version_string,
                'new_version': new_version_string
            }
        )
    else:
        vcs_configuration = None

    # Prepare the VCS repository
    repo_class = select_vcs_repo_class(vcs_configuration)

    # Prepare the files that have been changed by Punch
    # Including the version file of Punch itself
    files_to_commit = [f.path for f in config.files]
    files_to_commit.append(args.version_file)

    # Initialise the VCS reposity class
    try:
        repo = repo_class(os.getcwd(), vcs_configuration, files_to_commit)
    except RepositorySystemError as exc:
        fatal_error(
            ("An error occurred while initialising "
             "the version control repository"),
            exc
        )

    changes = global_replacer.run_all_serializers(
        current_version.as_dict(),
        new_version.as_dict()
    )

    if args.verbose:
        print("\n# Current version")
        show_version_parts(current_version.values)

        print("\n# New version")
        show_version_parts(new_version.values)

        print("\n# Global version updates")
        show_version_updates(changes)

        print("\n# Configured files")
        for file_updater in file_updaters:
            print("+ {}:".format(file_configuration.path))
            changes = file_updater.get_summary(
                current_version.as_dict(),
                new_version.as_dict()
            )
            show_version_updates(changes)

        vcs_info = repo.get_info()

        if len(vcs_info) != 0:
            print("\n# VCS")

            for key, value in vcs_info:
                print('+ {}: {}'.format(key, value))

    if args.simulate:
        sys.exit(0)

    check_release_notes(config, changes)

    VCSStartReleaseUseCase(repo).execute()

    try:
        for file_updater in file_updaters:
            file_updater.update(
                current_version.as_dict(), new_version.as_dict()
            )
    except ValueError as e:
        if not args.quiet:
            print("Warning:", e)

    # Write the updated version info to the version file.
    new_version.to_file(args.version_file)

    VCSFinishReleaseUseCase(repo).execute()
