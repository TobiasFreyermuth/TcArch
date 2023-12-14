import pathlib

from src.TcArch import TcArchTestResult
from src.PlcProject import PlcProject

suit_name = __name__.split('.')[-1]


class TerminalAbstractionConfigFilesTest(object):
    def __init__(self, settings):
        self.settings = settings
        self.folder_ignore_list = settings.get('folderIgnoreList', False)
        if self.folder_ignore_list and ',' in self.folder_ignore_list:
            self.folder_ignore_list = [x.strip().upper() for x in self.folder_ignore_list.split(',')]
        self.config_file_prefix = settings.get('configFilePrefix', None)
        self.config_file_suffix = settings.get('configFileSuffix', None)
        self.config_file_ending = settings.get('configFileEnding', None)
        self.config_file_relative_to_pou_file = settings.get('configFileRelativeToPouFile', None)

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
        if len([v.upper() for v in str(path).split('/') if v.upper() in self.folder_ignore_list]) > 0:
            return False
        else:
            return True


class PouFolderStructureTest(object):
    def __init__(self, settings):
        self.folder_ignore_list = settings.get('folderIgnoreList', None)
        self.min_folder_nesting_level = int(settings.get('MinFolderNestingLevel', 0))
        self.max_folder_nesting_level = int(settings.get('MaxFolderNestingLevel', 100))
        if self.min_folder_nesting_level > self.max_folder_nesting_level:
            raise ValueError('Invalide settings: "MinFolderNestingLevel" must be smaller or equal to '
                             '"MaxFolderNestingLevel"')

    def run_test(self, prj: PlcProject) -> list[TcArchTestResult]:
        results = []
        for pou in prj.get_pous():
            rel_path = pathlib.Path(pou.path).relative_to(prj.plc_project_file.parent)
            parents = list(rel_path.parents)
            parents.remove(pathlib.Path('.'))
            if self.folder_ignore_list is not None:
                # check if one of the parent folders is one in the folders to be ignored list
                if len([folder for folder in parents if str(folder.stem) in self.folder_ignore_list]) > 0:
                    continue
            if (len(parents) >= self.min_folder_nesting_level) and (len(parents) <= self.max_folder_nesting_level):
                results.append(TcArchTestResult(suit_name, self.__class__.__name__, 12, True, f'Ok'))
            elif len(parents) < self.min_folder_nesting_level:
                msg = (f'POU-file {pou.name} in {pou.path} nested in too flat folder structure with less than '
                       f'{self.min_folder_nesting_level} levels {len(parents)}')
                results.append(TcArchTestResult(suit_name, self.__class__.__name__, 12, False, msg))
            elif len(parents) > self.max_folder_nesting_level:
                msg = (f'POU-file {pou.name} in {pou.path} nested in too deep folder structure with more than '
                       f'{self.max_folder_nesting_level} levels')
                results.append(TcArchTestResult(suit_name, self.__class__.__name__, 12, False, msg))
            else:
                raise ValueError(len(parents))

        return results

