#! /usr/bin/env python
# -*- coding: utf-8 -*-

# The MIT License (MIT)
#
# Copyright (c) 2013 Bartosz Janda
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

import lldb

# NSStringEncoding
NSASCIIStringEncoding = 1                        # 0..127 only
NSNEXTSTEPStringEncoding = 2
NSJapaneseEUCStringEncoding = 3
NSUTF8StringEncoding = 4
NSISOLatin1StringEncoding = 5
NSSymbolStringEncoding = 6
NSNonLossyASCIIStringEncoding = 7
NSShiftJISStringEncoding = 8                     # kCFStringEncodingDOSJapanese
NSISOLatin2StringEncoding = 9
NSUnicodeStringEncoding = 10
NSWindowsCP1251StringEncoding = 11               # Cyrillic; same as AdobeStandardCyrillic
NSWindowsCP1252StringEncoding = 12               # WinLatin1
NSWindowsCP1253StringEncoding = 13               # Greek
NSWindowsCP1254StringEncoding = 14               # Turkish
NSWindowsCP1250StringEncoding = 15               # WinLatin2
NSISO2022JPStringEncoding = 21                   # ISO 2022 Japanese encoding for e-mail
NSMacOSRomanStringEncoding = 30

NSUTF16StringEncoding = NSUnicodeStringEncoding  # An alias for NSUnicodeStringEncoding

NSUTF16BigEndianStringEncoding = 0x90000100      # NSUTF16StringEncoding encoding with explicit endianness specified
NSUTF16LittleEndianStringEncoding = 0x94000100   # NSUTF16StringEncoding encoding with explicit endianness specified

NSUTF32StringEncoding = 0x8c000100
NSUTF32BigEndianStringEncoding = 0x98000100      # NSUTF32StringEncoding encoding with explicit endianness specified
NSUTF32LittleEndianStringEncoding = 0x9c000100   # NSUTF32StringEncoding encoding with explicit endianness specified


# Converting NSData to NSString
# NSString UTF8
def print_nsdata_as_nsstring_utf8_command(debugger, command, result, internal_dict):
    print_nsdata_as_nsstring_command(debugger, command, result, internal_dict, NSUTF8StringEncoding)


# NSString UTF16
def print_nsdata_as_nsstring_utf16_command(debugger, command, result, internal_dict):
    print_nsdata_as_nsstring_command(debugger, command, result, internal_dict, NSUTF16StringEncoding)


# NSString UTF16 Little Endian
def print_nsdata_as_nsstring_utf16l_command(debugger, command, result, internal_dict):
    print_nsdata_as_nsstring_command(debugger, command, result, internal_dict, NSUTF16LittleEndianStringEncoding)


# NSString UTF16 Big Endian
def print_nsdata_as_nsstring_utf16b_command(debugger, command, result, internal_dict):
    print_nsdata_as_nsstring_command(debugger, command, result, internal_dict, NSUTF16BigEndianStringEncoding)


# NSString UTF32
def print_nsdata_as_nsstring_utf32_command(debugger, command, result, internal_dict):
    print_nsdata_as_nsstring_command(debugger, command, result, internal_dict, NSUTF32StringEncoding)


# NSString UTF32 Little Endian
def print_nsdata_as_nsstring_utf32l_command(debugger, command, result, internal_dict):
    print_nsdata_as_nsstring_command(debugger, command, result, internal_dict, NSUTF32LittleEndianStringEncoding)


# NSString UTF32 Big Endian
def print_nsdata_as_nsstring_utf32b_command(debugger, command, result, internal_dict):
    print_nsdata_as_nsstring_command(debugger, command, result, internal_dict, NSUTF32BigEndianStringEncoding)


def print_nsdata_as_nsstring_command(debugger, command, result, internal_dict, string_type=NSUTF8StringEncoding):
    """
    Overview:

    A command to print NSData object as NSString.

    Example:

    pds data
    pds8 data
    pds16 data
    pds16l data
    pds16b data
    pds32 data
    pds32l data
    pds32b data
    """
    target = debugger.GetSelectedTarget()
    process = target.GetProcess()
    thread = process.GetSelectedThread()
    frame = thread.GetSelectedFrame()

    if not target.IsValid() or not process.IsValid():
        result.SetError("Unable to get target/process")
        return

    options = lldb.SBExpressionOptions()
    options.SetIgnoreBreakpoints()

    print_command = "(NSString *)[[NSString alloc] initWithData:((NSData *)({0!s})) encoding:{1}]"\
        .format(command, string_type)
    if frame.IsValid():
        data = frame.EvaluateExpression(print_command, options)
        data_description = data.GetObjectDescription()

        print >> result, data_description
    else:
        result.SetError("Invalid frame.")


# def lldb_init(debugger, internal_dict):
#     debugger.HandleCommand("command script add -f {}.print_nsdata_as_nsstring_utf8_command pds".format(__name__))
#     debugger.HandleCommand("command script add -f {}.print_nsdata_as_nsstring_utf8_command pds8".format(__name__))
#     debugger.HandleCommand("command script add -f {}.print_nsdata_as_nsstring_utf16_command pds16".format(__name__))
#     debugger.HandleCommand("command script add -f {}.print_nsdata_as_nsstring_utf16l_command pds16l".format(__name__))
#     debugger.HandleCommand("command script add -f {}.print_nsdata_as_nsstring_utf16b_command pds16b".format(__name__))
#     debugger.HandleCommand("command script add -f {}.print_nsdata_as_nsstring_utf32_command pds32".format(__name__))
#     debugger.HandleCommand("command script add -f {}.print_nsdata_as_nsstring_utf32l_command pds32l".format(__name__))
#     debugger.HandleCommand("command script add -f {}.print_nsdata_as_nsstring_utf32b_command pds32b".format(__name__))
