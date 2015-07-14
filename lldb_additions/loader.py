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
import json
import class_dump


lldb_additions_class_dump_dir = "ClassDumps"
lldb_additions_lldb_commands_dir = "lldb_commands"

lldb_script_extensions = [".py"]
lldb_scripts_paths = ["scripts"]
lldb_commands_paths = ["commands",
                       # "commands/debug"
                       ]
lldb_summaries_paths = ["summaries"]
lldb_summaries_load_order = ["SummaryBase",

                             "NSObject",
                             "NSOperation",
                             "NSURLResponse",
                             "NSURLSessionTask",
                             "NSURLSessionDataTask",
                             "NSCFLocalSessionTask",
                             "NSCFLocalDataTask",
                             "NSCFBackgroundSessionTask",
                             "NSCFBackgroundDataTask",

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
                             "UINavigationController",
                             "UIBarItem",
                             "UIColor",
                             "UIEvent",
                             "UIInternalEvent",

                             "SKRequestInternal",
                             "SKRequest",
                             "SKPaymentInternal",
                             "SKPaymentQueueInternal",
                             "SKPaymentTransactionInternal",
                             "SKProductInternal",
                             "SKProductsRequestInternal",
                             "SKProductsResponseInternal",

                             "AFURLConnectionOperation",
                             "AFHTTPRequestOperation",
                             "AFHTTPRequestOperationManager",
                             "AFURLSessionManager",
                             "AFHTTPSessionManager",
                             "AFHTTPRequestSerializer",
                             "AFJSONRequestSerializer",
                             "AFPropertyListRequestSerializer",
                             "AFHTTPResponseSerializer",
                             "AFJSONResponseSerializer",
                             "AFPropertyListResponseSerializer",
                             "AFXMLParserResponseSerializer",
                             "AFXMLDocumentResponseSerializer",
                             "AFImageResponseSerializer",
                             "AFCompoundResponseSerializer",
                             "AFSecurityPolicy",
                             "AFNetworkActivityIndicatorManager",
                             "AFNetworkReachabilityManager",
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


def scripts_in_directory(path, subdirectories=True):
    """
    Finds all Python scripts in given directory.
    Returns file name and full path to file.

    :param str path: Path to directory with scripts.
    :param bool subdirectories: True if subdirectories should also be searched.
    :return: List of founded scripts.
    :rtype: list[(str, str)]
    """
    scripts = list()

    # Search for scripts inf subdirectories.
    if subdirectories:
        # Go through all folders.
        for root, dirs, files in os.walk(path):
            # Got through all files in folder.
            for f in files:
                # Work only files with correct suffix.
                file_name, file_extension = os.path.splitext(f)
                # Add only files with correct suffix.
                if lldb_script_extensions.count(file_extension) != 0:
                    full_file_path = os.path.join(root, f)
                    scripts.append((file_name, full_file_path))
    # Search for scripts only in given directory.
    else:
        for f in os.listdir(path):
            # Work only files with correct suffix.
            file_name, file_extension = os.path.splitext(f)
            # Add only files with correct suffix.
            if lldb_script_extensions.count(file_extension) != 0:
                full_file_path = os.path.join(path, f)
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
    relative_path = os.path.relpath(script_dir_path, __package_dir_path)
    file_name, _ = os.path.splitext(os.path.basename(script_path))

    # Create module path.
    module_paths = [__package_name]
    module_paths.extend(split_path(relative_path))
    module_paths.append(file_name)
    module_path = ".".join(module_paths)

    # Load module to LLDB.
    if file_name != "__init__":
        # Load module to LLDB.
        debugger.HandleCommand("script import {}".format(module_path))

    # Load module.
    module = imp.load_source(module_path, script_path)

    # Execute init method.
    if hasattr(module, "lldb_init"):
        # Initialize module.
        module.lldb_init(debugger, internal_dict)


def load_lldb_commands_directory(directory, debugger, internal_dict):
    """
    Reads all files from the directory and executes them as LLDB commands.

    :param str directory: Path to directory.
    :param lldb.SBDebugger debugger: LLDB debugger.
    :param dict internal_dict: Internal LLDB dictionary.
    """
    # Go through all folders.
    for root, dirs, files in os.walk(directory):
        # Got through all files in folder.
        for f in files:
            file_path = os.path.join(root, f)
            debugger.HandleCommand("command source -s true {}".format(file_path))


def load_all(debugger, internal_dict):
    """
    Loads all scripts from Commands, Scripts and Summaries directories.

    :param lldb.SBDebugger debugger: LLDB debugger
    :param dict internal_dict: Internal LLDB dictionary.
    """
    log = logging.getLogger(__name__)

    # Load scripts.
    scripts = list()
    for directory in lldb_scripts_paths:
        directory_path = os.path.join(__package_dir_path, directory)
        scripts.extend(scripts_in_directory(directory_path))
    load_scripts(scripts, debugger, internal_dict)

    # Load summaries.
    scripts = list()
    for directory in lldb_summaries_paths:
        directory_path = os.path.join(__package_dir_path, directory)
        scripts.extend(scripts_in_directory(directory_path))
    load_scripts(scripts, debugger, internal_dict, lldb_summaries_load_order)

    # Load commands.
    scripts = list()
    for directory in lldb_commands_paths:
        directory_path = os.path.join(__package_dir_path, directory)
        scripts.extend(scripts_in_directory(directory_path, subdirectories=False))
    load_scripts(scripts, debugger, internal_dict)

    # Load lldb commands.
    load_lldb_commands_directory(os.path.join(__package_dir_path, lldb_additions_lldb_commands_dir), debugger, internal_dict)

    log.debug("Scripts loaded.")


def EMPTY():
    pass


def get_package_name():
    """
    Returns package name -> "lldb_additions"

    :return: Package name.
    :rtype: str
    """
    return __name__.split(u".")[0]


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


__package_name = get_package_name()
__package_dir_path = get_package_dir_path()
__user_config_file_path = u"~/.lldb/lldb_additions.json"
__default_config_file_name = u"config.json"
__package_config_file_name = u"config.json"
__module_files_extensions = [".py"]


def __get_default_configuration():
    """
    Reads default configuration and returns it.

    :return: Default configuration.
    :rtype: dict
    """
    log = logging.getLogger(__name__)

    # Looks for default configuration.
    default_config_path = os.path.join(__package_dir_path, __default_config_file_name)
    if os.path.exists(default_config_path):
        # Loads JSON configuration.
        with open(default_config_path) as default_config_file:
            default_config = json.load(default_config_file)

        return default_config
    else:
        log.critical(u"Cannot find default config file \"{}\".".format(default_config_path))
        return dict()


def __get_user_configuration():
    """
    Reads user configuration and returns it.

    :return: User configuration.
    :rtype: dict
    """
    log = logging.getLogger(__name__)

    # Looks for user JSON configuration file.
    config_path = os.path.expanduser(__user_config_file_path)
    if os.path.exists(config_path):
        # Loads JSON configuration.
        with open(config_path) as config_file:
            config = json.load(config_file)

        return config
    else:
        # Missing JSON config.
        log.info(u"Missing user configuration \"{}\".".format(config_path))
        return dict()


def __get_builtin_package_path(package_name):
    """
    Returns builtin package path.

    :param str package_name: Package path.
    :return: Builtin package path.
    :rtype: str
    """
    return os.path.join(__package_dir_path, package_name)


def __get_builtin_package_config_file_path(package_name):
    """
    Returns builtin package config file path.

    :param str package_name: Package name.
    :return: Builtin package config file path.
    :rtype: str
    """
    return os.path.join(__get_builtin_package_path(package_name), __package_config_file_name)


def __get_custom_package_config_file_path(package_name):
    """
    Returns custom package config file path.

    :param str package_name: Package name.
    :return: Custom package config file path.
    :rtype: str
    """
    return os.path.join(os.path.expanduser(package_name), __package_config_file_name)


def __get_modules_at_path(path):
    """
    Finds all Python modules in given directory.
    Returns module names.

    :param str path: Directory path.
    :return: Python modules in given directory.
    :rtype: list[str]
    """
    modules = list()

    # Search for scripts only in given directory.
    for f in os.listdir(path):
        # Work only files with correct suffix.
        module_name, module_extension = os.path.splitext(f)
        # Skip __init__ file.
        if module_name == "__init__":
            continue
        # Add only files with correct suffix.
        elif __module_files_extensions.count(module_extension) != 0:
            modules.append(module_name)
    return modules


def __load_user_configuration(debugger, user_configuration):
    """
    Loads user configuration from `configuration`. If parameters or configuration are missing
    then loads default configuration.

    :param lldb.SBDebugger debugger: LLDB debugger.
    :param dict user_configuration: User configuration.
    """
    # log = logging.getLogger(__name__)

    # Get default configuration.
    default_config = __get_default_configuration()

    # Loaded packages.
    loaded_packages = list()

    # Load builtin packages.
    builtin_packages = None
    if u"builtin_packages" in user_configuration:
        builtin_packages = user_configuration[u"builtin_packages"]

    if builtin_packages is None:
        builtin_packages = default_config[u"builtin_packages"]

    """:type: list[str]"""
    if builtin_packages is not None:
        for module_name in builtin_packages:
            __load_builtin_package(debugger, module_name, loaded_packages)


def __load_package(debugger, package_name, loaded_packages):
    """
    Loads packages, builtin or custom.

    :param lldb.SBDebugger debugger: LLDB debugger.
    :param str package_name: Package name.
    :param list[str] loaded_packages: Loaded packages.
    """
    # Skip loading if packages was already loaded.
    if package_name in loaded_packages:
        return

    # Checks if builtin package with given name exists.
    builtin_package_config_path = __get_builtin_package_config_file_path(package_name)
    if os.path.exists(builtin_package_config_path):
        __load_builtin_package(debugger, package_name, loaded_packages)
    else:
        # Check if custom module exists.
        custom_package_config_file_path = __get_custom_package_config_file_path(package_name)
        if os.path.exists(custom_package_config_file_path):
            __load_custom_package(debugger, package_name, loaded_packages)


def __load_builtin_package(debugger, package_name, loaded_packages):
    """
    Loads builtin package.

    :param lldb.SBDebugger debugger: LLDB debugger.
    :param str package_name: Package name.
    :param list[str] loaded_packages: Loaded packages.
    """
    log = logging.getLogger(__name__)

    # Skip loading if package was already loaded.
    if package_name in loaded_packages:
        return
    loaded_packages.append(package_name)

    package_path = __get_builtin_package_path(package_name)

    # Check package config file.
    package_config_path = __get_builtin_package_config_file_path(package_name)
    if not os.path.exists(package_config_path):
        log.critical(u"Missing package config file \"{}\".".format(package_config_path))
        return

    # Read config file.
    try:
        with open(package_config_path) as package_config_file:
            package_config = json.load(package_config_file)
    except ValueError:
        log.critical(u"Cannot read package config file \"{}\".".format(package_config_path))
        return

    class_dumps = package_config[u"class_dumps"] if u"class_dumps" in package_config else None
    lldb_init = package_config[u"lldb_init"] if u"lldb_init" in package_config else None
    dependencies = package_config[u"dependencies"] if u"dependencies" in package_config else None
    modules = package_config[u"modules"] if u"modules" in package_config else None
    load_all_modules = package_config[u"load_all_modules"] if u"load_all_modules" in package_config else None

    # Load dependencies.
    if dependencies is not None:
        for dependency in dependencies:
            __load_builtin_package(debugger, dependency, loaded_packages)

    log.debug(u"Loading builtin package \"{}\".".format(package_name))

    # Load modules in order.
    all_package_modules = __get_modules_at_path(package_path)
    if modules is not None:
        for module_name in modules:
            # Load module.
            __load_builtin_module(debugger, package_name, module_name)
            all_package_modules.remove(module_name)

    # Load other modules.
    if load_all_modules is True:
        for module_name in all_package_modules:
            # Load module.
            __load_builtin_module(debugger, package_name, module_name)

    # Load LLDB init.
    if lldb_init is not None:
        # Convert string to list of strings.
        if isinstance(lldb_init, str) or isinstance(lldb_init, unicode):
            lldb_init = [lldb_init]
        for li in lldb_init:
            lldb_init_path = os.path.join(package_path, li)
            if os.path.exists(lldb_init_path):
                log.debug(u"Loading lldb init \"{}\".".format(lldb_init_path))
                debugger.HandleCommand("command source -s true {}".format(lldb_init_path))
            else:
                log.critical(u"Cannot find lldb init file \"{}\".".format(lldb_init_path))

    # Register class dump module.
    if class_dumps is not None:
        class_dumps_path = os.path.join(package_path, class_dumps)
        if os.path.exists(class_dumps_path):
            log.debug(u"Registering class dump module \"{}\".".format(class_dumps_path))
            get_shared_lazy_class_dump_manager().register_module(package_name, class_dumps_path)
        else:
            log.critical(u"Cannot find class dump folder \"{}\".".format(class_dumps_path))


def __load_builtin_module(debugger, package_name, module_name):
    """
    Loads module into LLDB Python interpreter.

    :param lldb.SBDebugger debugger: LLDB debugger.
    :param str package_name: Package name.
    :param str module_name: Module name.
    """
    log = logging.getLogger(__name__)
    module_path = u".".join([__package_name, package_name, module_name])
    log.debug(u"Importing module \"{}\".".format(module_path))
    debugger.HandleCommand("script import {}".format(module_path))


def __load_custom_package(debugger, package_name, loaded_packages):
    # Skip loading if package was already loaded.
    if package_name in loaded_packages:
        return
    pass


def get_shared_lazy_class_dump_manager():
    """
    Get shared lazy class dump manager.

    :return: Shared lazy class dump manager.
    :rtype: ClassDump.LazyClassDumpManager.
    """
    if not hasattr(get_shared_lazy_class_dump_manager, "lazy_class_dump_manager"):
        logger = logging.getLogger(__name__)
        logger.debug(u"Creating shared class dump manager.")
        get_shared_lazy_class_dump_manager.lazy_class_dump_manager = class_dump.LazyClassDumpManager()
    return get_shared_lazy_class_dump_manager.lazy_class_dump_manager


def load(debugger, internal_dict):
    """
    Looks for user configuration at "~/.lldb/lldb_additions.json" and loads it
    using `load_configuration` method.

    :param lldb.SBDebugger debugger: LLDB debugger.
    :param internal_dict: Internal LLDB dictionary.
    """
    log = logging.getLogger(__name__)

    # Get user configuration.
    user_config = __get_user_configuration()
    # Load configuration.
    __load_user_configuration(debugger, user_config)

    log.debug(u"Loaded.")
