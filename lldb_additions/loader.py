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
import logger
import imp
import json
import class_dump
import type_cache
import helpers


class Loader(object):
    """
    Scripts loader.

    :param lldb.SBDebugger debugger: LLDB debugger.
    :param dict internal_dict: Internal LLDB dictionary.
    """
    __package_name = helpers.get_root_package_name(__name__)
    __package_dir_path = helpers.get_package_dir_path(__name__, __file__)
    __user_config_file_path = u"~/.lldb/lldb_additions.json"
    __default_config_file_name = u"config.json"
    __package_config_file_name = u"config.json"
    __module_files_extensions = [".py"]

    def __init__(self, debugger, internal_dict):
        """
        :param lldb.SBDebugger debugger: LLDB debugger.
        :param dict internal_dict: Internal LLDB dictionary.
        """
        super(Loader, self).__init__()
        self.debugger = debugger
        self.internal_dict = internal_dict

    @classmethod
    def __get_default_configuration(cls):
        """
        Reads default configuration and returns it.

        :return: Default configuration.
        :rtype: dict
        """
        log = logging.getLogger(__name__)

        # Looks for default configuration.
        default_config_path = os.path.join(cls.__package_dir_path, cls.__default_config_file_name)
        if os.path.exists(default_config_path):
            # Loads JSON configuration.
            with open(default_config_path) as default_config_file:
                default_config = json.load(default_config_file)

            return default_config
        else:
            log.critical(u"Cannot find default config file \"{}\".".format(default_config_path))
            return dict()

    @classmethod
    def __get_user_configuration(cls):
        """
        Reads user configuration and returns it.

        :return: User configuration.
        :rtype: dict
        """
        log = logging.getLogger(__name__)

        # Looks for user JSON configuration file.
        config_path = os.path.expanduser(cls.__user_config_file_path)
        if os.path.exists(config_path):
            # Loads JSON configuration.
            with open(config_path) as config_file:
                config = json.load(config_file)

            return config
        else:
            # Missing JSON config.
            log.info(u"Missing user configuration \"{}\".".format(config_path))
            return dict()

    @classmethod
    def __get_builtin_package_path(cls, package_name):
        """
        Returns builtin package path.

        :param str package_name: Package path.
        :return: Builtin package path.
        :rtype: str
        """
        return os.path.join(cls.__package_dir_path, package_name)

    @classmethod
    def __get_builtin_package_config_file_path(cls, package_name):
        """
        Returns builtin package config file path.

        :param str package_name: Package name.
        :return: Builtin package config file path.
        :rtype: str
        """
        return os.path.join(cls.__get_builtin_package_path(package_name), cls.__package_config_file_name)

    @classmethod
    def __get_custom_package_config_file_path(cls, package_name):
        """
        Returns custom package config file path.

        :param str package_name: Package name.
        :return: Custom package config file path.
        :rtype: str
        """
        return os.path.join(os.path.expanduser(package_name), cls.__package_config_file_name)

    @classmethod
    def __get_modules_at_path(cls, path):
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
            elif cls.__module_files_extensions.count(module_extension) != 0:
                modules.append(module_name)
        return modules

    def __load_user_configuration(self, user_configuration):
        """
        Loads user configuration from `configuration`. If parameters or configuration are missing
        then loads default configuration.

        :param dict user_configuration: User configuration.
        """
        # log = logging.getLogger(__name__)

        # Get default configuration.
        default_config = self.__get_default_configuration()

        # Reload builtin scripts.
        reload_modules = False
        if u"reload" in user_configuration:
            reload_modules = bool(user_configuration[u"reload"])
        if reload_modules:
            self.__reload_internal_scripts()

        # Clean log file.
        clean_log_file = False
        if u"clean_logs" in user_configuration:
            clean_log_file = bool(user_configuration[u"clean_logs"])
        if clean_log_file:
            logger.get_shared_logger_configurator().clean_log_file()

        # Configure logger.
        configure_loggers = False
        if u"logging" in user_configuration:
            configure_loggers = bool(user_configuration[u"logging"])
        if configure_loggers:
            logger.get_shared_logger_configurator().configure_loggers()
        else:
            logger.get_shared_logger_configurator().disable_loggers()

        # Cleans shared type cache.
        type_cache.clean_type_cache()

        # Loaded packages.
        loaded_packages = list()

        # Load builtin packages.
        builtin_packages = None
        if u"builtin_packages" in user_configuration:
            builtin_packages = user_configuration[u"builtin_packages"]
            """:type: list[str]"""

        if builtin_packages is None:
            builtin_packages = default_config[u"builtin_packages"]
            """:type: list[str]"""

        if builtin_packages is not None:
            for module_name in builtin_packages:
                self.__load_builtin_package(module_name, loaded_packages, reload_modules)

        # Load additional builtin packages (only from user config).
        if u"additional_builtin_packages" in user_configuration:
            additional_builtin_packages = user_configuration[u"additional_builtin_packages"]
            """:type: list[str]"""
            for module_name in additional_builtin_packages:
                self.__load_builtin_package(module_name, loaded_packages, reload_modules)

    def __reload_internal_scripts(self):
        """
        Reloads builtin scripts, like class_dump, helpers, loader, logger and type_cache.
        """
        scripts = [u"loader", u"class_dump", u"helpers", u"logger", u"type_cache"]
        for script in scripts:
            script_file_path = os.path.join(self.__package_dir_path, script) + u".py"
            script_module_path = u".".join([self.__package_name, script])
            imp.load_source(script_module_path, script_file_path)

    def __load_package(self, package_name, loaded_packages, reload_modules):
        """
        Loads packages, builtin or custom.

        :param str package_name: Package name.
        :param list[str] loaded_packages: Loaded packages.
        :param bool reload_modules: True if modules should be reloaded.
        """
        # Skip loading if packages was already loaded.
        if package_name in loaded_packages:
            return

        # Checks if builtin package with given name exists.
        builtin_package_config_path = self.__get_builtin_package_config_file_path(package_name)
        if os.path.exists(builtin_package_config_path):
            self.__load_builtin_package(package_name, loaded_packages, reload_modules)
        else:
            # Check if custom module exists.
            custom_package_config_file_path = self.__get_custom_package_config_file_path(package_name)
            if os.path.exists(custom_package_config_file_path):
                self.__load_custom_package(package_name, loaded_packages, reload_modules)

    def __load_builtin_package(self, package_name, loaded_packages, reload_modules):
        """
        Loads builtin package.

        :param str package_name: Package name.
        :param list[str] loaded_packages: Loaded packages.
        :param bool reload_modules: True if modules should be reloaded.
        """
        log = logging.getLogger(__name__)

        # Skip loading if package was already loaded.
        if package_name in loaded_packages:
            return
        loaded_packages.append(package_name)

        package_path = self.__get_builtin_package_path(package_name)

        # Check package config file.
        package_config_path = self.__get_builtin_package_config_file_path(package_name)
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
                self.__load_builtin_package(dependency, loaded_packages, reload_modules)

        log.debug(u"Loading builtin package \"{}\".".format(package_name))

        # Load modules in order.
        all_package_modules = self.__get_modules_at_path(package_path)
        if modules is not None:
            for module_name in modules:
                # Load module.
                self.__load_builtin_module(package_name, module_name, reload_modules)
                all_package_modules.remove(module_name)

        # Load other modules.
        if load_all_modules is True:
            for module_name in all_package_modules:
                # Load module.
                self.__load_builtin_module(package_name, module_name, reload_modules)

        # Load LLDB init.
        if lldb_init is not None:
            # Convert string to list of strings.
            if isinstance(lldb_init, str) or isinstance(lldb_init, unicode):
                lldb_init = [lldb_init]
            for li in lldb_init:
                lldb_init_path = os.path.join(package_path, li)
                if os.path.exists(lldb_init_path):
                    log.debug(u"Loading lldb init \"{}\".".format(lldb_init_path))
                    self.debugger.HandleCommand("command source -s true {}".format(lldb_init_path))
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

    def __load_builtin_module(self, package_name, module_name, reload_modules):
        """
        Loads module into LLDB Python interpreter.

        :param str package_name: Package name.
        :param str module_name: Module name.
        :param bool reload_modules: True if modules should be reloaded.
        """
        log = logging.getLogger(__name__)
        # Load module at path.
        module_path = u".".join([self.__package_name, package_name, module_name])
        if reload_modules is False:
            log.debug(u"Importing module \"{}\".".format(module_path))
        self.debugger.HandleCommand("script import {}".format(module_path))

        # (Re)Load module.
        if reload_modules:
            module_file_path = os.path.join(self.__package_dir_path, package_name, module_name) + u".py"
            if os.path.exists(module_file_path):
                log.debug(u"Loading module \"{}\" at path \"{}\".".format(module_path, module_file_path))
                module = imp.load_source(module_path, module_file_path)

                # Execute init method.
                # if hasattr(module, "lldb_init"):
                #     # Initialize module.
                #     module.lldb_init(debugger, internal_dict)
            else:
                log.critical(u"Cannot find module at path \"{}\".".format(module_file_path))

    def __load_custom_package(self, package_name, loaded_packages, reload_modules):
        # Skip loading if package was already loaded.
        if package_name in loaded_packages:
            return
        pass

    def load(self):
        """
        Looks for user configuration at "~/.lldb/lldb_additions.json" and loads it
        using `load_configuration` method.
        """
        log = logging.getLogger(__name__)

        # Get user configuration.
        user_config = self.__get_user_configuration()

        # Load configuration.
        self.__load_user_configuration(user_config)

        log.debug(u"Loaded.")


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
