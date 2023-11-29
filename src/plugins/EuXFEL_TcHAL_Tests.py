from src.TcArch import TcArchTestResult
from src.PlcProject import PlcProject

suit_name = __name__.split('.')[-1]


class TerminalAbstractionConfigFilesTest(object):
    def __init__(self, settings):
        self.settings = settings
        self.folder_ignore_list = settings.get('folderIgnoreList')
        if ',' in self.folder_ignore_list:
            self.folder_ignore_list = [x.strip().upper() for x in self.folder_ignore_list.split(',')]
        self.config_file_prefix = settings.get('configFilePrefix')
        self.config_file_suffix = settings.get('TerminalAbstractionConfigFilesTest', 'configFileSuffix')
        self.config_file_ending = settings.get('TerminalAbstractionConfigFilesTest', 'configFileEnding')
        self.config_file_relative_to_pou_file = settings.get('TerminalAbstractionConfigFilesTest',
                                                           'configFileRelativeToPouFile')

    def run_test(self, prj: PlcProject) -> list[TcArchTestResult]:
        results = []
        left_over_artefacts = prj.artefacts.copy()
        for fb in prj.get_function_blocks(path_filter=self.path_filter_func):
            config_file_name = f'{self.config_file_prefix}{fb.name}{self.config_file_suffix}.{self.config_file_ending}'
            if config_file_name not in prj.artefacts:
                msg = f'Unable to find expected config file {config_file_name} for Function Block {fb.name}'
                results.append(TcArchTestResult(suit_name, self.__class__.__name__, 12, True, msg))
            else:
                left_over_artefacts.pop(config_file_name)

        for key in left_over_artefacts:
            tmp = key.split('.')
            if key.startswith(self.config_file_prefix) and len(tmp) == 2 and tmp[0].endswith(self.config_file_suffix) and tmp[1] == self.config_file_ending:
                msg = f'Dangling config file "{key}" found in \n\t{left_over_artefacts[key].absolute()}.'
                results.append(TcArchTestResult(suit_name, self.__class__.__name__, 12, True, msg))
        return results

#    @staticmethod
    def path_filter_func(self, path):
        if len([v.upper() for v in path.split('/') if v.upper() in self.folder_ignore_list]) > 0:
            return False
        else:
            return True
