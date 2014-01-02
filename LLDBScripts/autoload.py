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

lldb_auto_load_paths = ["~/Library/LLDBScripts/Commands",
                        "~/Library/LLDBScripts/Summaries"]
lldb_script_endings = [".py"]
lldb_script_order = ["objc_runtime",
                     "summary_helpers",
                     "NSObject",
                     "UIResponder",
                     "UIView",
                     "UIControl"]


def load_script(script_path, debugger):
    command = "command script import \"{}\"".format(script_path)
    debugger.HandleCommand(command)


def __lldb_init_module(debugger, dict):
    # Go through all files
    to_load = set()
    endings = tuple(lldb_script_endings)

    # Go through all lldb auto load paths
    for path in lldb_auto_load_paths:
        # Got through all folders in auto load paths
        for root, dirs, files in os.walk(os.path.expanduser(path)):
            # Got through all files
            for f in files:
                # Add only files with correct suffix
                if f.endswith(endings):
                    full_file_path = os.path.join(root, f)
                    # to_load.add(full_file_path)
                    to_load.add((f, full_file_path))
                    # print f
                    # print full_file_path

    # Load all scripts
    to_load = list(to_load)
    to_load.sort()

    # First load Summaries from order list
    for order_summary in lldb_script_order:
        indexes = [i for i, v in enumerate(to_load) if v[0].startswith(order_summary)]
        if len(indexes) > 0:
            index = indexes[0]
            script_name, script_path = to_load[index]
            load_script(script_path, debugger)
            del to_load[index]

    # Load other scripts
    for script_name, script_path in to_load:
        load_script(script_path, debugger)
        # print script_path
        # print command
