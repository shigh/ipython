"""Tests for tokenutil"""
# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.

import nose.tools as nt

from IPython.utils.tokenutil import token_at_cursor, line_at_cursor

def expect_token(expected, cell, cursor_pos):
    token = token_at_cursor(cell, cursor_pos)
    offset = 0
    for line in cell.splitlines():
        if offset + len(line) >= cursor_pos:
            break
        else:
            offset += len(line)
    column = cursor_pos - offset
    line_with_cursor = '%s|%s' % (line[:column], line[column:])
    line
    nt.assert_equal(token, expected,
        "Expected %r, got %r in: %r (pos %i)" % (
        expected, token, line_with_cursor, cursor_pos)
    )

def test_simple(): 
    cell = "foo"
    for i in range(len(cell)):
        expect_token("foo", cell, i)

def test_function():
    cell = "foo(a=5, b='10')"
    expected = 'foo'
    # up to `foo(|a=`
    for i in range(cell.find('a=') + 1):
        expect_token("foo", cell, i)
    # find foo after `=`
    for i in [cell.find('=') + 1, cell.rfind('=') + 1]:
        expect_token("foo", cell, i)
    # in between `5,|` and `|b=`
    for i in range(cell.find(','), cell.find('b=')):
        expect_token("foo", cell, i)

def test_multiline():
    cell = '\n'.join([
        'a = 5',
        'b = hello("string", there)'
    ])
    expected = 'hello'
    start = cell.index(expected) + 1
    for i in range(start, start + len(expected)):
        expect_token(expected, cell, i)
    expected = 'there'
    start = cell.index(expected) + 1
    for i in range(start, start + len(expected)):
        expect_token(expected, cell, i)

def test_attrs():
    cell = "foo(a=obj.attr.subattr)"
    expected = 'obj'
    idx = cell.find('obj') + 1
    for i in range(idx, idx + 3):
        expect_token(expected, cell, i)
    idx = cell.find('.attr') + 2
    expected = 'obj.attr'
    for i in range(idx, idx + 4):
        expect_token(expected, cell, i)
    idx = cell.find('.subattr') + 2
    expected = 'obj.attr.subattr'
    for i in range(idx, len(cell)):
        expect_token(expected, cell, i)

def test_line_at_cursor():
    cell = ""
    (line, offset) = line_at_cursor(cell, cursor_pos=11)
    assert line == "", ("Expected '', got %r" % line)
    assert offset == 0, ("Expected '', got %r" % line)
