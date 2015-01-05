#! /usr/bin/env python
# -*- coding: utf-8 -*-

# The MIT License (MIT)
#
# Copyright (c) 2014 Bartosz Janda
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
import os
import logging
import LLDBLogger

LLDBLogger.configure_loggers()

lldb_scripts_dir = "~/Library/LLDBScripts/"
lldb_class_dump_dir = "ClassDumps"
lldb_commands_paths = ["Commands"]
lldb_scripts_paths = ["Scripts"]
lldb_scripts_load_order = ["Helpers",
                           "LLDBLogger",
                           "SaveParam"]
lldb_script_extensions = [".py"]

lldb_summaries_paths = ["Summaries"]
lldb_summaries_load_order = ["SummaryBase",

                             "NSObject",

                             "CADoublePoint",
                             "CADoubleSize",
                             "CADoubleRect",
                             "CALayerInternalLayer",
                             "CALayerIvars",
                             "CALayer",

                             "UIResponder",
                             "UIView",
                             "UIControl",
                             "UIPickerView",

                             "SKRequestInternal",
                             "SKRequest",
                             "SKPaymentInternal",
                             "SKPaymentQueueInternal",
                             "SKPaymentTransactionInternal",
                             "SKProductInternal",
                             "SKProductsRequestInternal",
                             "SKProductsResponseInternal"
                             ]


def scripts_in_directory(path):
    """
    Finds all Python scripts in given directory.

    :param str path: Path to directory with scripts.
    :return: List of founded scripts.
    :rtype: list[(str, str)]
    """
    extensions = tuple(lldb_script_extensions)
    scripts = []

    # Go through all folders
    for root, dirs, files in os.walk(os.path.expanduser(path)):
        # Got through all files in folder
        for f in files:
            # Add only files with correct suffix
            if f.endswith(extensions):
                file_name = os.path.splitext(f)[0]
                full_file_path = os.path.join(root, f)
                scripts.append((file_name, full_file_path))
                # print f
                # print file_name
                # print full_file_path
    return scripts


def load_scripts(scripts, debugger, order_list=[]):
    """
    Loads scripts to the debugger. It uses order_list to load scripts in correct order if needed.

    :param list[(str, str)] scripts: List of scripts to load.
    :param lldb.SBDebugger debugger: LLDB debugger.
    :param list[str] order_list: List of ordered scripts that have to be loaded in order.
    """
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
    """
    Loads script at script_path to debugger.

    :param str script_path: Path to script.
    :param lldb.SBDebugger debugger: LLDB debugger.
    """
    command = "command script import \"{}\"".format(script_path)
    debugger.HandleCommand(command)
    # print script_path
    # print command


def load_lldb_scripts(debugger):
    """
    Loads all scripts from Commands, Scripts and Summaries directories.

    :param lldb.SBDebugger debugger: LLDB debugger.
    """
    # Load commands.
    scripts = []
    for directory in lldb_commands_paths:
        full_path = os.path.join(lldb_scripts_dir, directory)
        scripts.extend(scripts_in_directory(full_path))
    load_scripts(scripts, debugger)

    # Load scripts.
    scripts = []
    for directory in lldb_scripts_paths:
        full_path = os.path.join(lldb_scripts_dir, directory)
        scripts.extend(scripts_in_directory(full_path))
    load_scripts(scripts, debugger, lldb_scripts_load_order)

    # Load summaries.
    scripts = []
    for directory in lldb_summaries_paths:
        full_path = os.path.join(lldb_scripts_dir, directory)
        scripts.extend(scripts_in_directory(full_path))
    load_scripts(scripts, debugger, lldb_summaries_load_order)

    logger = logging.getLogger(__name__)
    logger.debug("Scripts loaded.")
