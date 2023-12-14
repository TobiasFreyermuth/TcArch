import re
from src.TcArch import TcArchTestResult
from src.PlcProject import PlcProject
from src.utils import simple_naming_convention_tester, Casing

suit_name = __name__.split('.')[-1]


class FunctionBlockNamingConventionTest(object):
    def __init__(self, settings):
        pass

    def run_test(self, prj: PlcProject) -> list[TcArchTestResult]:
        results = []
        for fb in prj.get_function_blocks(path_filter=self.path_filter_func):
            if True:
                msg = f'message'
                results.append(TcArchTestResult(suit_name, self.__class__.__name__, 12, True, msg))
        return results

    @staticmethod
    def path_filter_func(path):
        if '_internal'.upper() in [x.upper() for x in str(path).split('/')]:
            return False
        else:
            return True


class InterfaceNamingConventionTest(object):
    def __init__(self, settings):
        self.prefix = settings.get('prefix', None)
        self.suffix = settings.get('suffix', None)
        self.casing = Casing[settings.get('casing', 'NONE')]

    def run_test(self, prj: PlcProject) -> list[TcArchTestResult]:
        results = []
        for interface in prj.get_interfaces():
            res, msg = simple_naming_convention_tester(interface.name, prefix=self.prefix, suffix=self.suffix,
                                                       casing=self.casing)
            results.append(TcArchTestResult(suit_name, self.__class__.__name__, 12, res, f'Interface name {interface.name}, {msg}'))
        return results
