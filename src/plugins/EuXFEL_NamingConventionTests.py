from src.TcArch import TcArchTestResult
from src.PlcProject import PlcProject

suit_name = __name__.split('.')[-1]


class FunctionBlockNamingConventionTest(object):
    def __init__(self, settings):
        self.settings = settings

    def run_test(self, prj: PlcProject) -> list[TcArchTestResult]:
        results = []
        for fb in prj.get_function_blocks(path_filter=self.path_filter_func):
            if True:
                msg = f'message'
                results.append(TcArchTestResult(suit_name, self.__class__.__name__, 12, True, msg))
        return results

    @staticmethod
    def path_filter_func(path):
        if '_internal'.upper() in [x.upper() for x in path.split('/')]:
            return False
        else:
            return True
