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
import class_dump
import type_cache
import helpers
import yaml
import sys


class Loader(object):
    """
    Scripts loader.

    :param lldb.SBDebugger debugger: LLDB debugger.
    :param dict internal_dict: Internal LLDB dictionary.
    :param bool reload_builtin: Reload builtin modules.
    :param bool reload_custom: Reload custom / user modules.
    :param list[str] loaded_builtin_packages: List of loaded builtin packages.
    :param list[str] loaded_builtin_packages_lldb_init: List of loaded builtin packages lldb init.
    :param list[str] loaded_custom_packages: List of loaded custom packages.
    :param list[str] loaded_custom_packages_lldb_init: List of loaded custom packages lldb init.
    :param str __PACKAGE_NAME: Package name.
    :param str __PACKAGE_DIR_PATH: Path to directory.
    :param str __USER_CONFIG_FILE_PATH: User configuration file path.
    :param str __DEFAULT_CONFIG_FILE_NAME: Default (package) configuration file name.
    :param str __PACKAGE_CONFIG_FILE_NAME: Package configuration file name.
    :param str __MODULE_FILES_EXTENSIONS: Supported module extensions.
    """
    __PACKAGE_NAME = helpers.get_first_package_name(__name__)
    __PACKAGE_DIR_PATH = helpers.get_package_dir_path(__name__, __file__)
    __USER_CONFIG_FILE_PATH = u"~/.lldb/mallet.yml"
    __DEFAULT_CONFIG_FILE_NAME = u"config.yml"
    __PACKAGE_CONFIG_FILE_NAME = u"config.yml"
    __MODULE_FILES_EXTENSIONS = [".py"]
    __MODULE_INIT_METHOD = "lldb_init"

    def __init__(self):
        super(Loader, self).__init__()
        self.debugger = None
        self.internal_dict = None

        self.reload_builtin = False
        self.reload_custom = True
        self.loaded_builtin_packages = list()
        self.loaded_builtin_packages_lldb_init = list()
        self.loaded_custom_packages = list()
        self.loaded_custom_packages_lldb_init = list()

    @classmethod
    def __get_default_configuration(cls):
        """
        Reads default configuration and returns it.

        :return: Default configuration.
        :rtype: dict
        """
        log = logging.getLogger(__name__)

        # Looks for default configuration.
        default_config_path = os.path.join(cls.__PACKAGE_DIR_PATH, cls.__DEFAULT_CONFIG_FILE_NAME)
        if os.path.exists(default_config_path):
            # Loads YAML configuration.
            try:
                with open(default_config_path) as default_config_file:
                    default_config = yaml.load(default_config_file)
                return default_config
            except ValueError:
                # Cannot open YAML file.
                if len(log.handlers) == 0:
                    print(u"Cannot open default config file \"{}\".".format(default_config_path))
                else:
                    log.critical(u"Cannot open default config file \"{}\".".format(default_config_path))
                return dict()
        else:
            # Missing YAML config.
            if len(log.handlers) == 0:
                print(u"Cannot find default config file \"{}\".".format(default_config_path))
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

        # Looks for user YAML configuration file.
        config_path = os.path.expanduser(cls.__USER_CONFIG_FILE_PATH)
        if os.path.exists(config_path):
            # Loads YAML configuration.
            try:
                with open(config_path) as config_file:
                    config = yaml.load(config_file)
                return config
            except ValueError:
                # Cannot open user YAML.
                if len(log.handlers) == 0:
                    print(u"Cannot open user configuration \"{}\".".format(config_path))
                else:
                    log.warning(u"Cannot open user configuration \"{}\".".format(config_path))
                return dict()
        else:
            # Missing YAML config.
            if len(log.handlers) == 0:
                print(u"Missing user configuration \"{}\".".format(config_path))
            else:
                log.warning(u"Missing user configuration \"{}\".".format(config_path))
            return dict()

    @classmethod
    def __get_builtin_package_path(cls, package_name):
        """
        Returns builtin package path.

        :param str package_name: Package name.
        :return: Builtin package path.
        :rtype: str
        """
        return os.path.join(cls.__PACKAGE_DIR_PATH, package_name)

    @classmethod
    def __get_builtin_package_config_file_path(cls, package_name):
        """
        Returns builtin package config file path.

        :param str package_name: Package name.
        :return: Builtin package config file path.
        :rtype: str
        """
        return os.path.join(cls.__get_builtin_package_path(package_name), cls.__PACKAGE_CONFIG_FILE_NAME)

    @classmethod
    def __get_custom_package_path(cls, package_name):
        """
        Returns custom package path.

        :param str package_name: Package name.
        :return: Custom package path.
        :rtype: str
        """
        return os.path.expanduser(package_name)

    @classmethod
    def __get_custom_package_config_file_path(cls, package_name):
        """
        Returns custom package config file path.

        :param str package_name: Package name.
        :return: Custom package config file path.
        :rtype: str
        """
        return os.path.join(cls.__get_custom_package_path(package_name), cls.__PACKAGE_CONFIG_FILE_NAME)

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
            # Add only files with correct suffix.
            if cls.__MODULE_FILES_EXTENSIONS.count(module_extension) != 0:
                modules.append(module_name)
        return modules

    def load(self, debugger, internal_dict):
        """
        Looks for user configuration at "~/.lldb/mallet.yml" If parameters or configuration are missing
        then loads default configuration.
        """
        self.debugger = debugger
        self.internal_dict = internal_dict
        log = logging.getLogger(__name__)

        # Get default configuration.
        default_config = self.__get_default_configuration()

        # Get user configuration.
        user_configuration = self.__get_user_configuration()

        # Reload builtin / custom.
        self.reload_builtin = False
        self.reload_custom = True
        if u"reload_builtin" in user_configuration:
            self.reload_builtin = bool(user_configuration[u"reload_builtin"])
        if u"reload" in user_configuration:
            self.reload_custom = bool(user_configuration[u"reload"])
        # Force custom package reload if builtin packages are reloaded.
        if self.reload_builtin:
            self.reload_custom = True

        # Clean loaded packages list.
        self.loaded_builtin_packages = list()
        self.loaded_custom_packages = list()

        # Reload builtin scripts and cleans builtin loaded packages.
        if self.reload_builtin:
            self.loaded_builtin_packages_lldb_init = list()
            self.__reload_internal_scripts()

        # Clean custom / user packages.
        if self.reload_custom:
            self.loaded_custom_packages_lldb_init = list()

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

        # Load builtin packages.
        builtin_packages = None
        if u"builtin_packages" in user_configuration and isinstance(user_configuration[u"builtin_packages"], list):
            builtin_packages = user_configuration[u"builtin_packages"]
            """:type: list[str]"""

        if builtin_packages is None:
            builtin_packages = default_config[u"builtin_packages"]
            """:type: list[str]"""

        if builtin_packages is not None:
            for package_name in builtin_packages:
                self.__load_package(package_name)

        # Load user or builtin packages (only from user config).
        if u"packages" in user_configuration and isinstance(user_configuration[u"packages"], list):
            additional_builtin_packages = user_configuration[u"packages"]
            """:type: list[str]"""
            for package_name in additional_builtin_packages:
                self.__load_package(package_name)

        log.debug(u"Loaded.")

    def __reload_internal_scripts(self):
        """
        Reloads builtin scripts, like class_dump, helpers, loader, logger and type_cache.
        """
        scripts = [u"loader", u"class_dump", u"helpers", u"logger", u"type_cache"]
        for script in scripts:
            script_file_path = os.path.join(self.__PACKAGE_DIR_PATH, script) + u".py"
            script_module_path = u".".join([self.__PACKAGE_NAME, script])
            imp.load_source(script_module_path, script_file_path)

    def __load_package(self, package):
        """
        Loads packages, builtin or custom.

        :param str package: Package name.
        """
        log = logging.getLogger(__name__)

        # Skip loading if packages was already loaded.
        if package in self.loaded_builtin_packages or package in self.loaded_custom_packages:
            return

        # Checks if builtin package with given name exists.
        builtin = True
        package_path = self.__get_builtin_package_path(package)
        package_config_path = self.__get_builtin_package_config_file_path(package)
        if not os.path.exists(package_config_path):
            # Check if custom module with given name exists and has config file.
            builtin = False
            package_path = self.__get_custom_package_path(package)
            package_config_path = self.__get_custom_package_config_file_path(package)
            if not os.path.exists(package_config_path):
                # Both builtin and custom packages don't have config file.
                return

        # Check config file path.
        assert package_path, u"Empty package path."
        assert package_config_path, u"Empty package config file path."

        # Append loaded packages.
        if builtin:
            self.loaded_builtin_packages.append(package)
        else:
            self.loaded_custom_packages.append(package)

        # Read config file.
        try:
            with open(package_config_path) as package_config_file:
                package_config = yaml.load(package_config_file)
        except ValueError:
            log.warning(u"Cannot read package config file \"{}\".".format(package_config_path))
            return

        # Read configuration.
        class_dumps = package_config[u"class_dumps"] if u"class_dumps" in package_config else None
        lldb_init = package_config[u"lldb_init"] if u"lldb_init" in package_config else None
        dependencies = package_config[u"dependencies"] if u"dependencies" in package_config else None
        modules = package_config[u"modules"] if u"modules" in package_config else None
        load_all_modules = package_config[u"load_all_modules"] if u"load_all_modules" in package_config else None

        # Get package name from package path.
        package_name = os.path.basename(package)

        # Get full package name.
        if builtin:
            full_package_name = u".".join([self.__PACKAGE_NAME, package_name])
        else:
            full_package_name = package_name

        # Load dependencies.
        if dependencies is not None:
            for dependency in dependencies:
                self.__load_package(dependency)

        log.info(u"Loading {} package \"{}\".".format(u"builtin" if builtin else u"custom", package))

        # Load modules in order.
        all_package_modules = self.__get_modules_at_path(package_path)
        if modules is not None:
            for module_name in modules:
                # Load module.
                self.__load_module(full_package_name, package_path, module_name)
                all_package_modules.remove(module_name)

        # Load other modules.
        if load_all_modules is True:
            for module_name in all_package_modules:
                # Load module.
                self.__load_module(full_package_name, package_path, module_name)

        # Load LLDB init.
        self.__load_lldb_init(package_path, lldb_init)

        # Register class dump module.
        if class_dumps is not None:
            class_dumps_path = os.path.join(package_path, class_dumps)
            if os.path.exists(class_dumps_path):
                log.debug(u"Registering class dump module \"{}\".".format(class_dumps_path))
                get_shared_lazy_class_dump_manager().register_module(package, class_dumps_path)
            else:
                log.warning(u"Cannot find class dump folder \"{}\".".format(class_dumps_path))

    def __load_module(self, full_package_name, package_path, module_name):
        """
        Loads module into LLDB Python interpreter.
        It is wrapper to `__load_module_*` methods.

        :param str full_package_name: Full package name.
        :param str package_path: Package path.
        :param str module_name: Module name.
        """
        # self.__load_module_1(full_package_name, package_path, module_name)
        self.__load_module_2(full_package_name, package_path, module_name)
        # self.__load_module_3(full_package_name, package_path, module_name)

    def __load_module_1(self, full_package_name, package_path, module_name):
        """
        Loads module into LLDB Python interpreter.
        This implementation is using `imp.load_source`.

        :param str full_package_name: Full package name.
        :param str package_path: Package path.
        :param str module_name: Module name.
        """
        log = logging.getLogger(__name__)
        # Load module at path.
        full_module_name = u".".join([full_package_name, module_name])
        self.debugger.HandleCommand("script import {}".format(full_module_name))

        # (Re)Load module.
        module_file_path = os.path.join(package_path, module_name) + u".py"
        if os.path.exists(module_file_path):
            log.debug(u"Loading module \"{}\" at path \"{}\".".format(full_module_name, module_file_path))
            module = imp.load_source(full_module_name, module_file_path)

            # Execute init method.
            if hasattr(module, self.__MODULE_INIT_METHOD):
                # Initialize module.
                init_method = getattr(module, self.__MODULE_INIT_METHOD)
                init_method(self.debugger, self.internal_dict)
        else:
            log.warning(u"Cannot find module at path \"{}\".".format(module_file_path))

    def __load_module_2(self, full_package_name, package_path, module_name):
        """
        Loads module into LLDB Python interpreter.
        This implementation is using `imp.find_module` and `imp.load_module`.

        :param str full_package_name: Full package name.
        :param str package_path: Package path.
        :param str module_name: Module name.
        :return: Loaded module.
        :rtype: module | None
        """
        log = logging.getLogger(__name__)

        # Root package.
        root_package_name = helpers.get_root_package_name(full_package_name)

        # Don't load __init__ module directly, just load package.
        if module_name == "__init__":
            last_package_name = helpers.get_last_package_name(full_package_name)
            root_package_path = os.path.dirname(package_path)

            return self.__load_module_2(root_package_name, root_package_path, last_package_name)

        # Try to load root package. Which is required to load sub module.
        # Package already loaded.
        if full_package_name in sys.modules:
            package = sys.modules[full_package_name]
        # There is no root package to load.
        elif root_package_name is None or len(root_package_name) == 0:
            package = None
        # Load root package.
        else:
            last_package_name = helpers.get_last_package_name(full_package_name)
            root_package_path = os.path.dirname(package_path)

            package = self.__load_module_2(root_package_name, root_package_path, last_package_name)

        # Load module.
        m = None
        """:type: module"""
        fp = None
        """:type: file"""
        try:
            # Find and load module.
            full_module_name = u".".join([full_package_name, module_name])
            fp, pathname, description = imp.find_module(module_name, [package_path])
            log.debug(u"Loading module \"{}\" at path \"{}\".".format(full_module_name, pathname))
            m = imp.load_module(full_module_name, fp, pathname, description)

            # Add module to package if exists.
            if package:
                setattr(package, module_name, m)

            # Execute mallet init method.
            if hasattr(m, self.__MODULE_INIT_METHOD):
                # Initialize module.
                init_method = getattr(m, self.__MODULE_INIT_METHOD)
                init_method(self.debugger, self.internal_dict)

        except ImportError:
            log.warning(u"Cannot find module \"{}\" at path \"{}\".".format(module_name, package_path))
        finally:
            # Closing file.
            if fp:
                fp.close()

        return m

    def __load_module_3(self, full_package_name, package_path, module_name):
        """
        Loads module into LLDB Python interpreter.
        This implementation is using standard `import` statement, no reloading.
        Is working only with built in modules or modules installed by pip.

        :param str full_package_name: Full package name.
        :param str package_path: Package path.
        :param str module_name: Module name.
        """
        log = logging.getLogger(__name__)

        # Load module at path.
        full_module_name = u".".join([full_package_name, module_name])
        log.debug(u"Loading module \"{}\".".format(full_module_name))
        self.debugger.HandleCommand("script import {}".format(full_module_name))

        if full_module_name in sys.modules:
            module = sys.modules[full_module_name]

            # Execute init method.
            if hasattr(module, self.__MODULE_INIT_METHOD):
                # Initialize module.
                init_method = getattr(module, self.__MODULE_INIT_METHOD)
                init_method(self.debugger, self.internal_dict)

    def __load_lldb_init(self, package_path, lldb_init):
        """
        Loads lldb init files.

        :param str package_path: Package path.
        :param str | list[str] lldb_init: lldb init files.
        :return:
        """
        log = logging.getLogger(__name__)

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
                    log.warning(u"Cannot find lldb init file \"{}\".".format(lldb_init_path))


__shared_lazy_class_dump_manager = None
""":type: class_dump.LazyClassDumpManager"""
__shared_loader = None
""":type: Loader"""


def get_shared_lazy_class_dump_manager():
    """
    Get shared lazy class dump manager.

    :return: Shared lazy class dump manager.
    :rtype: ClassDump.LazyClassDumpManager.
    """
    global __shared_lazy_class_dump_manager
    if __shared_lazy_class_dump_manager is None:
        __shared_lazy_class_dump_manager = class_dump.LazyClassDumpManager()
        log = logging.getLogger(__name__)
        log.debug(u"Creating shared class dump manager.")
    return __shared_lazy_class_dump_manager


def get_shared_loader():
    """
    Get shared Loader.

    :return: Shared loader.
    :rtype: Loader.
    """
    global __shared_loader
    if __shared_loader is None:
        __shared_loader = Loader()
        log = logging.getLogger(__name__)
        log.debug(u"Creating shared Loader.")
    return __shared_loader
