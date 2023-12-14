import pathlib
import re
from enum import Enum

from lxml import etree

from src.PlcProject import TwinCATPlcProject, Programm, FunctionBlock, Function, Interface, PlcProject


def TwinCatProjectParser(path_to_project: pathlib.Path) -> PlcProject:
    prj = TwinCATPlcProject(path_to_project)
    prj.name = path_to_project.stem
    prj.path = str(path_to_project)

    for file in path_to_project.rglob(f'**/*'):
        if file.name.endswith('TcPOU'):
            decl = __get_pou_declaration(file)
            match __get_pou_type(decl):
                case ElementType.PROGRAM:
                    prj.add_pou(Programm(name=file.stem, path=file.absolute(), declaration=decl, implementation=''))
                case ElementType.FUNCTIONBLOCK:
                    prj.add_pou(FunctionBlock(name=file.stem, path=file.absolute(), declaration=decl,
                                              implementation=''))
                case ElementType.FUNCTION:
                    prj.add_pou(Function(name=file.stem, path=file.absolute(), declaration=decl, implementation=''))
                case _:
                    raise ValueError(f'this should never happen')

        elif file.name.endswith('TcDUT'):
            prj.duts[file.name] = file
        elif file.name.endswith('TcGVL'):
            prj.gvls[file.name] = file
        elif file.name.endswith('TcIO'):
            decl = __get_interface_declaration(file)
            match __get_pou_type(decl):
                case ElementType.INTERFACE:
                    prj.add_pou(Interface(name=file.stem, path=file.absolute(), declaration=decl))
                case other:
                    raise ValueError(f'this should never happen')

        elif file.name.endswith('plcproj'):
            prj.plc_project_file =file

        else:
            if file.is_file():
                prj.artefacts[file.name] = file

    return prj


class ElementType(Enum):
    PROGRAM = "program"
    FUNCTIONBLOCK = "functionblock"
    FUNCTION = "function"
    INTERFACE = "interface"


def __get_pou_type(declaration: str) -> ElementType:
    declaration = __delete_pragmas(__remove_all_comments(declaration)).strip()

    if declaration.upper().startswith('PROGRAM'):
        return ElementType(ElementType.PROGRAM)
    elif declaration.upper().startswith('FUNCTION_BLOCK'):
        return ElementType(ElementType.FUNCTIONBLOCK)
    elif declaration.upper().startswith('FUNCTION'):
        return ElementType(ElementType.FUNCTION)
    elif declaration.upper().startswith('INTERFACE'):
        return ElementType(ElementType.INTERFACE)
    else:
        raise KeyError(f'Unable to find Pou-type in \n {declaration}')


def __get_pou_declaration(softdevice_path: pathlib.Path):
    """
    This function will return the declaration of a softdevice as string.

    :param softdevice_path: absolute path to the softdevice
    :return: softdevice declaration as string
    """
    root = etree.parse(softdevice_path)
    dec_xml = root.findall('.//POU/Declaration')
    if len(dec_xml) == 1:
        return dec_xml[0].text
    else:
        return None


def __get_interface_declaration(interface_path: pathlib.Path):
    root = etree.parse(interface_path)
    dec_xml = root.findall('.//Itf/Declaration')
    if len(dec_xml) == 1:
        return dec_xml[0].text
    else:
        return None


def __delete_block_comments(in_str):
    """
    Function to delete block commands and returns the give string without the comments.
    PLC block line comment starts with "(*" and ends with "*)".
    :param in_str: Block of text which is to have the block comments removed
    :return in_str: The given block text with all comments removed.
    """

    def prepare_string(in_str):
        new_lines = []
        for line in in_str.split('\n'):
            if '//' in line:
                pos = line.find('//')
                line = '%s%s' % (line[:pos], line[pos:].replace('(*', '$1$').replace('*)', '$2$'))

            new_lines.append(line)

        return '\n'.join(new_lines).strip()

    def delete_single_block_comment(in_str):
        temp = in_str.split('*)')[0].split('(*')[-1]
        return in_str.replace('(*%s*)' % temp, '')

    in_str = prepare_string(in_str)

    i = 0
    while '(*' in in_str and '*)' in in_str:
        in_str = delete_single_block_comment(in_str)
        i += 1
        if i > 50000:
            raise ValueError('Number of block comments in input string to high')

    in_str = in_str.replace('$1$', '(*').replace('$2$', '*)')

    return '\n%s\n' % in_str


def __delete_inline_comments(in_str):
    """
    Function to delete inline comments for a given block of text.
    :param in_str: Block of text  contianing inline comments
    :return: Block of text with inline comments removed.
    """
    new_lines = []
    for line in in_str.split('\n'):
        new_lines.append('%s' % line.split('//')[0])

    return '\n'.join(new_lines)


def __delete_pragmas(input_string):
    """

    :param in_str:
    :return:
    """
    if input_string is None:
        return
    # The patter {.*?} means any text starting with { and ending with }, non-greedy
    pattern = r'\{.*?\}'
    output_string = re.sub(pattern, '', input_string)
    return output_string


def __remove_inline_comments(s):
    if s is None:
        return
    lines = s.split('\n')
    cleaned_lines = []
    for line in lines:
        # Find the start of a potential inline comment
        idx = line.find('//')
        if idx >= 0:
            # Keep only the part of the line before the comment
            line = line[:idx].rstrip()
        if line:  # Exclude empty lines after removing comments
            cleaned_lines.append(line)
    # Join the lines into a single string
    return '\n'.join(cleaned_lines)


def __remove_block_comments(s):
    if s is None:
        return
    block_start = '(*'
    block_end = '*)'
    ans = ''
    i = 0
    nested_level = 0

    while i < len(s):
        # Check if the string at the current position starts with block_start
        if s[i: i + len(block_start)] == block_start:
            nested_level += 1
            i += len(block_start)
        # Check if the string at the current position starts with block_end
        elif s[i: i + len(block_end)] == block_end:
            if nested_level == 0:
                ans += block_end
                i += len(block_end)
            else:
                nested_level -= 1
                i += len(block_end)
        # If we are not in a block comment, we add the current character to the output string
        elif nested_level == 0:
            ans += s[i]
            i += 1
        # If we are in a block comment, ignore the character
        else:
            i += 1
    return ans


def __remove_all_comments(input_string):
    input_string = __remove_block_comments(input_string)
    input_string = __remove_inline_comments(input_string)
    return input_string
