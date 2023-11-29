from src.PlcProject import Access
from src.TcArch import TcArchTestResult
from src.PlcProject import PlcProject

suit_name = __name__.split('.')[-1]


class TcUnitTestAreInternalTest(object):
    def __init__(self, settings):
        self.settings = settings

    def run_test(self, prj: PlcProject) -> list[TcArchTestResult]:
        results = []
        for fb in prj.get_function_blocks():
            if 'TcUnit' in fb.extends and fb.access_level_modifier != Access.INTERNAL:
                msg = f'message'
                results.append(TcArchTestResult(suit_name, self.__class__.__name__, 12, True, msg))
        return results
