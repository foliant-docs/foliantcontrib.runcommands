'''
Preprocessor for Foliant documentation authoring tool.
Allows to run arbitrary external commands.
'''

from subprocess import run, PIPE, STDOUT, CalledProcessError

from foliant.preprocessors.base import BasePreprocessor


class Preprocessor(BasePreprocessor):
    defaults = {
        'commands': [],
        'targets': [],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def apply(self):
        if not self.options['targets'] or self.context['target'] in self.options['targets']:
            if self.options['commands']:
                for command in self.options['commands']:
                    try:
                        run(command, shell=True, check=True, stdout=PIPE, stderr=STDOUT)

                    except CalledProcessError as exception:
                            raise RuntimeError(f'Failed: {exception.output.decode()}')
