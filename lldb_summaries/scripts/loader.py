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
import imp
import logger

logger.configure_loggers()


def get_package_name():
    """
    Returns package name -> "lldb_summaries"

    :return: Package name.
    :rtype: str
    """
    return __name__.split(".")[0]


def get_package_dir_path():
    """
    Returns absolute package path.

    :return: Absolute package path.
    :rtype: str
    """
    # Get number of submodules.
    modules = __name__.split(".")
    modules_count = len(modules)
    step_count = modules_count - 1
    if step_count < 0:
        step_count = 0

    # Got up to main package folder.
    path = os.path.realpath(__file__)
    for _ in range(step_count):
        path = os.path.dirname(path)

    return path


lldb_summaries_package_name = get_package_name()
lldb_summaries_package_dir_path = get_package_dir_path()

lldb_script_extensions = [".py"]
lldb_commands_paths = ["commands"]
lldb_summaries_paths = ["summaries"]
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
                             "UIViewController",

                             "SKRequestInternal",
                             "SKRequest",
                             "SKPaymentInternal",
                             "SKPaymentQueueInternal",
                             "SKPaymentTransactionInternal",
                             "SKProductInternal",
                             "SKProductsRequestInternal",
                             "SKProductsResponseInternal"
                             ]


def split_path(path):
    """
    Split directory path into list.

    :param str path:
    :return: directory path split into list.
    :rtype: list[str]
    """
    folders = []
    while path != "":
        path, last = os.path.split(path)
        if last != "":
            folders.append(last)
    folders.reverse()
    return folders


def scripts_in_directory(path):
    """
    Finds all Python scripts in given directory.

    :param str path: Path to directory with scripts.
    :return: List of founded scripts.
    :rtype: list[(str, str)]
    """
    scripts = list()

    # Go through all folders.
    for root, dirs, files in os.walk(os.path.expanduser(path)):
        # Got through all files in folder.
        for f in files:
            # Work only files with correct suffix.
            file_name, file_extension = os.path.splitext(f)
            # Add only files with correct suffix.
            if lldb_script_extensions.count(file_extension) != 0:
                full_file_path = os.path.join(root, f)
                scripts.append((file_name, full_file_path))
    return scripts


def load_scripts(scripts, debugger, internal_dict, order_list=[]):
    """
    Loads scripts to the debugger. It uses order_list to load scripts in correct order if needed.

    :param list[(str, str)] scripts: List of scripts to load.
    :param lldb.SBDebugger debugger: LLDB debugger.
    :param dict internal_dict: Internal LLDB dictionary.
    :param list[str] order_list: List of ordered scripts that have to be loaded in order.
    """
    scripts.sort()

    # Load scripts from ordered list.
    for ordered_script in order_list:
        # Find script index.
        indexes = [i for i, v in enumerate(scripts) if v[0] == ordered_script]
        if len(indexes) > 0:
            index = indexes[0]
            script_name, script_path = scripts[index]
            load_script(script_path, debugger, internal_dict)
            del scripts[index]

    # Load other scripts
    for script_name, script_path in scripts:
        load_script(script_path, debugger, internal_dict)


def load_script(script_path, debugger, internal_dict):
    """
    Loads script at script_path to debugger.

    :param str script_path: Path to script.
    :param lldb.SBDebugger debugger: LLDB debugger.
    :param dict internal_dict: Internal LLDB dictionary.
    """
    # Helpers.
    log = logging.getLogger(__name__)
    script_dir_path = os.path.dirname(script_path)
    relative_path = os.path.relpath(script_dir_path, lldb_summaries_package_dir_path)
    file_name, _ = os.path.splitext(os.path.basename(script_path))

    # Create module path.
    module_paths = [lldb_summaries_package_name]
    module_paths.extend(split_path(relative_path))
    module_paths.append(file_name)
    module_path = ".".join(module_paths)

    # Load module to LLDB.
    if file_name != "__init__":
        # Load module to LLDB.
        debugger.HandleCommand("command script import {}".format(module_path))

    # Load module.
    module = imp.load_source(module_path, script_path)

    # Execute init method.
    if hasattr(module, "lldbinit"):
        # Initialize module.
        log.debug("Loading script: {}".format(file_name))
        module.lldbinit(debugger, internal_dict, module_path)


def load_all(debugger, internal_dict):
    """
    Loads all scripts from Commands, Scripts and Summaries directories.

    :param lldb.SBDebugger debugger: LLDB debugger
    :param dict internal_dict: Internal LLDB dictionary.
    """
    log = logging.getLogger(__name__)

    # Load commands.
    scripts = list()
    for directory in lldb_commands_paths:
        directory_path = os.path.join(lldb_summaries_package_dir_path, directory)
        scripts.extend(scripts_in_directory(directory_path))
    load_scripts(scripts, debugger, internal_dict)

    # Load summaries.
    # for directory in lldb_summaries_paths:
    #     load_scripts_in_directory(directory, lldb_summaries_load_order, debugger, internal_dict)

    log.debug("Scripts loaded.")