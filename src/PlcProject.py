from dataclasses import dataclass, field
from enum import Enum


class PlcProject(object):
    """
    This class holds parsed data of a PLC project and should be used as the data source for most, if not all TcArch test
    against a PLC project.
    I provides methods to retrieve, files and folder structures, POU implementations, POU declarations and so on.
    """
    def __init__(self):
        self.name = 'PlcProjectName'
        self.project_type = 'project type'  # type of the source the project was parsed from e.g. TwinCAT, PLC open export, ...
        self.__pous = []
        self.gvls = {}
        self.duts = {}
        self.artefacts = {}  # all other artefacts which do not belong into POUs, GVLs or DUTs e.g. xml files

    def add_pou(self, pou):
        if pou is not None:
            self.__pous.append(pou)

    def get_function_blocks(self, path_filter=None):
        return [pou for pou in self.get_pous(path_filter) if isinstance(pou, FunctionBlock)]

    def get_functions(self, path_filter=None):
        return [pou for pou in self.get_pous(path_filter) if isinstance(pou, Function)]

    def get_programms(self, path_filter=None):
        return [pou for pou in self.get_pous(path_filter) if isinstance(pou, Programm)]

    def get_interfaces(self, path_filter=None):
        return [pou for pou in self.get_pous(path_filter) if isinstance(pou, Interface)]

    def get_pous(self, path_filter=None):
        if path_filter is None:
            return self.__pous
        else:
            return [pou for pou in self.__pous if path_filter(pou.path)]

    def __repr__(self):
        return str(self)

    def __str__(self):
        return (f'PlcProject: {self.name}\n\tPOUs: \t\t{len(self.__pous)}\n\tGVLs: \t\t{len(self.gvls)}'
                f'\n\tDUTs: \t\t{len(self.duts)}\n\tartefacts: \t{len(self.artefacts)}')


class Access(Enum):
    NONE = 0
    PUBLIC = 1  # Access is not restricted (equivalent to specifying no access modifier).
    PRIVATE = 2  # Access to the method is restricted to the function block or the program respectively.
    PROTECTED = 3  # Access to the method is restricted to the program or the function block and its derivatives respectively.
    INTERNAL = 4  # Access to the method is limited to the namespace (the library).


@dataclass
class Pou:
    name: str
    path: str
    declaration: str = field(repr=False, default='')
    final: bool = field(default=False)
    access_level_modifier: Access = field(default=Access.NONE)
    extends: list[str] = field(default_factory=list)
    implements: str = field(repr=False, default='')


@dataclass
class Programm(Pou):
    implementation: str = field(repr=False, default='')


@dataclass
class Method(Pou):
    path = ''
    abstract: bool = field(default=False)
    final: bool = field(default=False)  # Overwriting the method in a derivative of the function block is not allowed. This means that the method may not be overwritten/extended in a possibly existing subclass.
    implementation: str = field(repr=False, default='')


@dataclass
class FunctionBlock(Pou):
    abstract: bool = field(default=False)
    implementation: str = field(repr=False, default='')
    methods: list[str] = field(default_factory=list)


@dataclass
class Function(Pou):
    implementation: str = field(repr=False, default='')


@dataclass
class Interface(Pou):
    pass


@dataclass
class Property(Pou):
    path = ''
    abstract: bool = field(default=False)
