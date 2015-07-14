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

NSASCIIStringEncoding = 1
NSNEXTSTEPStringEncoding = 2
NSJapaneseEUCStringEncoding = 3
NSUTF8StringEncoding = 4
NSISOLatin1StringEncoding = 5
NSSymbolStringEncoding = 6
NSNonLossyASCIIStringEncoding = 7
NSShiftJISStringEncoding = 8
NSISOLatin2StringEncoding = 9
NSUnicodeStringEncoding = 10
NSWindowsCP1251StringEncoding = 11
NSWindowsCP1252StringEncoding = 12
NSWindowsCP1253StringEncoding = 13
NSWindowsCP1254StringEncoding = 14
NSWindowsCP1250StringEncoding = 15
NSISO2022JPStringEncoding = 21
NSMacOSRomanStringEncoding = 30

NSUTF16StringEncoding = NSUnicodeStringEncoding

NSUTF16BigEndianStringEncoding = 0x90000100
NSUTF16LittleEndianStringEncoding = 0x94000100

NSUTF32StringEncoding = 0x8c000100
NSUTF32BigEndianStringEncoding = 0x98000100
NSUTF32LittleEndianStringEncoding = 0x9c000100


def get_string_encoding_text(value):
    if value == NSASCIIStringEncoding:
        return "ASCII"
    elif value == NSNEXTSTEPStringEncoding:
        return "NEXTSTEP"
    elif value == NSJapaneseEUCStringEncoding:
        return "JapaneseEUC"
    elif value == NSUTF8StringEncoding:
        return "UTF8"
    elif value == NSISOLatin1StringEncoding:
        return "ISOLatin1"
    elif value == NSSymbolStringEncoding:
        return "Symbol"
    elif value == NSNonLossyASCIIStringEncoding:
        return "NonLossyASCII"
    elif value == NSShiftJISStringEncoding:
        return "ShiftJIS"
    elif value == NSISOLatin2StringEncoding:
        return "ISOLatin2"
    elif value == NSUnicodeStringEncoding:
        return "UTF16"
    elif value == NSWindowsCP1251StringEncoding:
        return "WindowsCP1251"
    elif value == NSWindowsCP1252StringEncoding:
        return "WindowsCP1252"
    elif value == NSWindowsCP1253StringEncoding:
        return "WindowsCP1253"
    elif value == NSWindowsCP1254StringEncoding:
        return "WindowsCP1254"
    elif value == NSWindowsCP1250StringEncoding:
        return "WindowsCP1250"
    elif value == NSISO2022JPStringEncoding:
        return "ISO2022JP"
    elif value == NSMacOSRomanStringEncoding:
        return "MacOSRoman"
    elif value == NSUTF16BigEndianStringEncoding:
        return "UTF16BigEndian"
    elif value == NSUTF16LittleEndianStringEncoding:
        return "UTF16LittleEndian"
    elif value == NSUTF32StringEncoding:
        return "UTF32"
    elif value == NSUTF32BigEndianStringEncoding:
        return "UTF32BigEndian"
    elif value == NSUTF32LittleEndianStringEncoding:
        return "UTF32LittleEndian"
    return "Unknown"
