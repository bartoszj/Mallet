#! /usr/bin/env python
# -*- coding: utf-8 -*-

# The MIT License (MIT)
#
# Copyright (c) 2015 Bartosz Janda
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


NSJSONReadingMutableContainers = 0
NSJSONReadingMutableLeaves = 1
NSJSONReadingAllowFragments = 2

NSJSONWritingPrettyPrinted = 1


def get_json_reading_options_text(value):
    """
    Returns NSJSONSerialization reading option.
    :param int value: NSJSONReadingOptions
    :return: NSJSONSerialization reading option as text.
    :rtype: str
    """
    v = list()
    if value & NSJSONReadingMutableContainers:
        v.append("MutableContainers")
    elif value & NSJSONReadingMutableLeaves:
        v.append("MutableLeaves")
    elif value & NSJSONReadingAllowFragments:
        v.append("AllowFragments")

    return ", ".join(v)


def get_json_writing_options_text(value):
    """
    Returns NSJSONWritingOptions reading option.
    :param int value: NSJSONWritingOptions
    :return: NSJSONWritingOptions reading option as text.
    :rtype: str
    """
    v = list()
    if value & NSJSONWritingPrettyPrinted:
        v.append("PrettyPrinted")
    return ", ".join(v)
