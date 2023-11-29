import argparse
import pathlib
import json
from lxml import etree


class Checker(object):
    def __init__(self, id):
        self.suit_name = self.__class__.__name__
        self.id = id
        self.__results = []

    def get_result_xml(self):
        for has_passed, name, msg, exception_type, stack_trace in self.__results:
            if self.has_passed:
                test_node = etree.Element("testcase")
                test_node.set('name', name)
                test_node.set('assertions', '3')
                test_node.set('classname', self.suit_name)
                test_node.set('status', 'PASS')
            else:
                test_node = etree.Element("testcase")
                test_node.set('name', name)
                test_node.set('assertions', '3')
                test_node.set('classname', self.suit_name)
                test_node.set('status', 'FAILED')
                failure_node = etree.Element("failure")
                failure_node.set('exception-type', exception_type)
                message_node = etree.Element("message")
                message_node.text = etree.CDATA(msg)
                stack_trace_node = etree.Element("stack-trace")
                stack_trace_node.text = etree.CDATA(stack_trace)
                failure_node.append(message_node)
                failure_node.append(stack_trace_node)
                test_node.append(failure_node)

        return test_node

    def _add_result(self, has_passed, check_name, message='', exception_type='no clue', stack_trace='stack-trace'):
        pass


class TcArchTestResult(object):
    def __init__(self, suit_name, name, id, has_passed, message='', exception_type='no clue', stack_trace='stack-trace'):
        self.suit_name = suit_name
        self.name = name
        self.id = id
        self.has_passed = has_passed
        self.message = message
        self.exception_type = exception_type
        self.stack_trace = stack_trace

    def get_xml(self):
        if self.has_passed:
            test_node = etree.Element("testcase")
            test_node.set('name', self.name)
            test_node.set('assertions', '3')
            test_node.set('classname', self.suit_name)
            test_node.set('status', 'PASS')
        else:
            test_node = etree.Element("testcase")
            test_node.set('name', self.name)
            test_node.set('assertions', '3')
            test_node.set('classname', self.suit_name)
            test_node.set('status', 'FAILED')
            failure_node = etree.Element("failure")
            failure_node.set('exception-type', self.exception_type)
            message_node = etree.Element("message")
            message_node.text = etree.CDATA(self.message)
            stack_trace_node = etree.Element("stack-trace")
            stack_trace_node.text = etree.CDATA(self.stack_trace)
            failure_node.append(message_node)
            failure_node.append(stack_trace_node)
            test_node.append(failure_node)

        return test_node


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('project_path', help='TwinCAT project folder path')
    args = parser.parse_args()

    p = pathlib.Path(args.project_path)
    if p.exists():
        from PlcProjectParser.TwinCatProjectParser import TwinCatProjectParser
        prj = TwinCatProjectParser(p)

        test_results = []
        with open('TcArchConfig.json', 'r') as config_file:
            json_config = json.load(config_file)
            import importlib
            for x in json_config.get('plugins'):
                try:
                    cls = getattr(importlib.import_module(x.get("path")), x.get('name'))
                    test = cls(x.get('settings'))
                    test_results.append(test.run_test(prj))
                except AttributeError as e:
                    print('AttributeError', e)
                except ModuleNotFoundError as e:
                    print('ModuleNotFoundError', e)

#
#    if config.get('TcUnit-Checks', 'enable'):
#        from TcUnit_Checks import TcUnit_CheckerRunner
#        unitTestInternal = TcUnit_CheckerRunner(config)
##        tree = etree.ElementTree(unitTestInternal)
##        tree.write("TcArchResults.xml")
#    if config.get('PouConfigFile-Checks', 'enable'):
#        from PouConfigFile_Checks import PouConfigFile_CheckerRunner
#        unitTestInternal = PouConfigFile_CheckerRunner(config)



