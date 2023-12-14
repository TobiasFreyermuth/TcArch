import pathlib
from src.PlcProject import Pou
from src.TcArch import TcArchTestResult
from src.plugins.EuXFEL_TcHAL_Tests import PouFolderStructureTest


class PlcProjectMock:

    def __init__(self):
        self.pous = []
        self.__path = pathlib.Path('.')

    def add_pou(self, pou):
        pass

    def get_function_blocks(self, path_filter=None):
        pass

    def get_functions(self, path_filter=None):
        pass

    def get_programms(self, path_filter=None):
        pass

    def get_interfaces(self, path_filter=None):
        pass

    def get_pous(self, path_filter=None):
        return self.pous

    @property
    def path(self) -> pathlib.Path:
        return self.__path

    @path.setter
    def path(self, val: pathlib.Path):
        self.__path = val

    @property
    def artefacts(self) -> dict:
        return {}

    @property
    def plc_project_file(self) -> pathlib.Path:
        return pathlib.Path('.')


def test_folder_structure_ok():
    setting = {'folderIgnoreList': None, 'MinFolderNestingLevel': 3, 'MaxFolderNestingLevel': 3}
    prj_mock = PlcProjectMock()
    prj_mock.pous.append(Pou('name', pathlib.Path('level_1/level_2/level_3/pou')))
    test = PouFolderStructureTest(setting)

    assert test.run_test(prj_mock) == [TcArchTestResult(name='PouFolderStructureTest', has_passed=True, message='Ok')]


def test_folder_structure_too_deep():
    setting = {'folderIgnoreList': None, 'MinFolderNestingLevel': 3, 'MaxFolderNestingLevel': 3}
    prj_mock = PlcProjectMock()
    prj_mock.pous.append(Pou('name', pathlib.Path('level_1/level_2/level_3/level_4/pou')))
    test = PouFolderStructureTest(setting)
    err_msg = ('POU-file name in level_1/level_2/level_3/level_4/pou nested in too deep folder structure with more '
               'than 3 levels')

    assert test.run_test(prj_mock) == [TcArchTestResult(name='PouFolderStructureTest', has_passed=False, message=err_msg)]


def test_folder_structure_too_flat():
    setting = {'folderIgnoreList': None, 'MinFolderNestingLevel': 3, 'MaxFolderNestingLevel': 3}
    plc_project_mock = PlcProjectMock()
    plc_project_mock.pous.append(Pou('name', pathlib.Path('level_1/level_2/pou')))
    test = PouFolderStructureTest(setting)
    err_msg = 'POU-file name in level_1/level_2/pou nested in too flat folder structure with less than 3 levels 2'

    assert test.run_test(plc_project_mock) == [TcArchTestResult(name='PouFolderStructureTest', has_passed=False,
                                                                message=err_msg)]

