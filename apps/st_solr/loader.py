from django.template.loaders.app_directories import Loader as AppDirectoriesLoader
import os

class Loader(AppDirectoriesLoader):

    is_usable = True

    def __call__(self, template_name, template_dirs=None):
        return self.load_template_from_other_solr_core(template_name, template_dirs)

    def load_template_from_other_solr_core(self, template_name, template_dirs=None):
        """
        Returns the absolute paths to "template_name", when appended to each
        directory in "template_dirs". Any paths that don't lie inside one of the
        template dirs are excluded from the result set, for security reasons.
        """

        core_name, template_name = template_name.split(":", 1)
        template_dirs = [os.path.join(os.path.dirname(__file__), 'templates/', core_name)]
        return self.load_template_source(template_name, template_dirs)

