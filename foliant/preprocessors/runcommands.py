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
        'verbose': False
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.logger = self.logger.getChild('runcommands')

        self.logger.debug(f'Preprocessor inited: {self.__dict__}')

    def apply(self):
        self.logger.info('Applying preprocessor')

        self.logger.debug(f'Allowed targets: {self.options["targets"]}')
        self.logger.debug(f'Current target: {self.context["target"]}')

        if not self.options['targets'] or self.context['target'] in self.options['targets']:
            if self.options['commands']:
                for command in self.options['commands']:
                    command = command.replace(
                        '${PROJECT_DIR}',
                        f'{self.project_path.absolute().as_posix()}'
                    )

                    command = command.replace(
                        '${SRC_DIR}',
                        f'{(self.project_path / self.config["src_dir"]).absolute().as_posix()}'
                    )

                    command = command.replace(
                        '${WORKING_DIR}',
                        f'{self.working_dir.absolute().as_posix()}'
                    )

                    command = command.replace(
                        '${BACKEND}',
                        f'{self.context["backend"]}'
                    )

                    command = command.replace(
                        '${TARGET}',
                        f'{self.context["target"]}'
                    )
                    try:
                        self.logger.debug(f'Running command: {command}')

                        if self.options['verbose'] and not self.quiet:
                            # showing command output to user
                            run(command, shell=True, check=True, stderr=STDOUT)
                        else:
                            # suppressing output
                            buffer = run(command, shell=True, check=True, stdout=PIPE, stderr=STDOUT)
                            self.logger.debug(f'Command output: {buffer.stdout}')
                    except CalledProcessError as exception:
                        self.logger.error(str(exception))

                        raise RuntimeError(f'Failed: {exception.output.decode()}')

        self.logger.info('Preprocessor applied')
