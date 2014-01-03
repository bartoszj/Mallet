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

import os

lldb_commands_paths = ["~/Library/LLDBScripts/Commands"]
lldb_summaries_paths = ["~/Library/LLDBScripts/Summaries"]
lldb_script_endings = [".py"]
lldb_summaries_load_order = ["objc_runtime",
                             "summary_helpers",
                             "NSObject",
                             "UIResponder",
                             "UIView",
                             "UIControl",
                             "UIPickerView",

                             "SKRequest"]


def scripts_in_directory(path):
    endings = tuple(lldb_script_endings)
    scripts = []

    # Go through all folders
    for root, dirs, files in os.walk(os.path.expanduser(path)):
        # Got through all files in folder
        for f in files:
            # Add only files with correct suffix
            if f.endswith(endings):
                file_name = os.path.splitext(f)[0]
                full_file_path = os.path.join(root, f)
                scripts.append((file_name, full_file_path))
                # print f
                # print file_name
                # print full_file_path
    return scripts


def load_scripts(scripts, debugger, order_list=[]):
    scripts.sort()

    # Load scripts from ordered list.
    for ordered_script in order_list:
        indexes = [i for i, v in enumerate(scripts) if v[0] == ordered_script]
        if len(indexes) > 0:
            index = indexes[0]
            script_name, script_path = scripts[index]
            load_script(script_path, debugger)
            del scripts[index]

    # Load other scripts
    for script_name, script_path in scripts:
        load_script(script_path, debugger)


def load_script(script_path, debugger):
    command = "command script import \"{}\"".format(script_path)
    debugger.HandleCommand(command)
    # print script_path
    # print command


def __lldb_init_module(debugger, dict):
    scripts = []
    for directory in lldb_commands_paths:
        scripts.extend(scripts_in_directory(directory))
    load_scripts(scripts, debugger)

    scripts = []
    for directory in lldb_summaries_paths:
        scripts.extend(scripts_in_directory(directory))
    load_scripts(scripts, debugger, lldb_summaries_load_order)
