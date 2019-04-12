from __future__ import print_function, absolute_import, division


class NoVCSRepo(object):

    def __init__(self, working_path, config_obj, files_to_commit=None):
        self.working_path = working_path

    def get_current_branch(self):
        return ''

    def get_tags(self):
        return ''

    def tag(self, *args):
        pass

    def pre_start_release(self):
        pass

    def start_release(self):
        pass

    def finish_release(self):
        pass

    def post_finish_release(self):
        pass

    def get_info(self):
        return []
