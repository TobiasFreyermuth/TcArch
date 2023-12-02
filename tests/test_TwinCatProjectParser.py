from src.PlcProjectParser.TwinCatProjectParser import (TwinCatProjectParser, __remove_block_comments,
                                                       __remove_inline_comments, __remove_all_comments)


def test_deleting_block_comments():
    block_comment = '(* Block Comment 1*)'
    code = 'INTERFACE A'
    st_src = f'{block_comment}{code}'
    assert __remove_block_comments(st_src) == code

    st_src = f'{code}{block_comment}'
    assert __remove_block_comments(st_src) == code

    st_src = f'{block_comment}{code}{block_comment}'
    assert __remove_block_comments(st_src) == code

    st_src = f'{code}{block_comment}{code}'
    assert __remove_block_comments(st_src) == f'{code}{code}'

    st_src = f'{code}{block_comment}{code}{block_comment}'
    assert __remove_block_comments(st_src) == f'{code}{code}'


def test_deleting_nested_block_comments():
    block_comment = '(* Block Comment outer (* Block Comment inner*)*)'
    code = 'INTERFACE A'
    st_src = f'{block_comment}{code}'
    assert __remove_block_comments(st_src) == code

    st_src = f'{code}{block_comment}'
    assert __remove_block_comments(st_src) == code

    st_src = f'{block_comment}{code}{block_comment}'
    assert __remove_block_comments(st_src) == code

    st_src = f'{code}{block_comment}{code}'
    assert __remove_block_comments(st_src) == f'{code}{code}'

    st_src = f'{code}{block_comment}{code}{block_comment}'
    assert __remove_block_comments(st_src) == f'{code}{code}'


def test_deleting_inline_comments():
    inline_comment = '//Block Comment 1\n'
    code = 'INTERFACE A'
    st_src = f'{inline_comment}{code}'
    assert __remove_inline_comments(st_src) == code

    st_src = f'{code}{inline_comment}'
    assert __remove_inline_comments(st_src) == code

    st_src = f'{inline_comment}{code}{inline_comment}'
    assert __remove_inline_comments(st_src) == code

    st_src = f'{code}{inline_comment}{code}'
    assert __remove_inline_comments(st_src) == f'{code}\n{code}'

    st_src = f'{code}{inline_comment}\n{code}{inline_comment}'
    assert __remove_inline_comments(st_src) == f'{code}\n{code}'


def test_removing_inline_comments_multiline():
    inline_comment = '//Block Comment 1\n'
    code = 'INTERFACE A'
    st_src = """
    test: bool; // test comment
    // comment
    """

    st_src_without_comments = """
    test: bool; 
    
    """
#    st_src = f'{inline_comment}{code}'
    assert __remove_inline_comments(st_src).strip() == st_src_without_comments.strip()


def test_removing_all_comments():
    st_src = """
    test: bool; // test comment
    // comment
    (*
    test multiline block comment
    *)
    Test_1 : bool:=True;
    """

    st_src_without_comments = """
    test: bool;
    
    Test_1 : bool:=True;
    """
    assert __remove_all_comments(st_src).strip() == st_src_without_comments.strip()



