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

import json
import os
import logging
import logger


class_dumps_folder_name = "class_dumps"
module_map_file_name = "module_map.json"


class LazyClassDumpManager(object):
    """
    Lazy loads class data into memory.

    :param dict[str, Module] modules: Maps module name to module.
    """
    def __init__(self):
        super(LazyClassDumpManager, self).__init__()
        log = logging.getLogger(__name__)
        log.debug("LazyClassDumpManager: created.")
        self.modules = dict()

    def register_module(self, module_name, module_path):
        """
        Adds module directory with `module_map.json` file.

        :param str module_name: Module name.
        :param str module_path: Path to module directory.
        """
        log = logging.getLogger(__name__)
        module_path = os.path.normpath(module_path)
        # Check if directory exists.
        if not os.path.exists(module_path):
            log.error("LazyClassDumpManager: Cannot find module \"{}\" directory \"{}\".".format(module_name, module_path))
            return

        # Loads module.
        module = Module(module_name, module_path)
        self.modules[module_name] = module

    def get_module(self, name):
        """
        Returns Module object with given name.

        :param str name: Module name.
        :return: Module object with given name.
        :rtype: Module | None
        """
        if name in self.modules:
            return self.modules[name]
        return None

    def get_class(self, module_name, architecture_name, class_name):
        """
        Returns Class object based on module name, architecture name and class name.

        Supported architectures: armv7, armv7s, arm64, i386, x86_64.

        :param str module_name: Module name.
        :param str architecture_name: Architecture name.
        :param str class_name: Class name.
        :return: Class object based on module name, architecture name and class name.
        :rtype: Class | None
        """
        # Try to finds Module.
        module = self.get_module(module_name)
        if not module:
            return None

        # Get Class.
        c = module.get_class_or_load(architecture_name, class_name)
        return c

    def get_ivar(self, module_name, architecture_name, class_name, ivar_name):
        """
        Returns Ivar object based on module name, architecture name, class name and ivar name.

        :param str module_name: Module name.
        :param str architecture_name: Architecture name.
        :param str class_name: Class name.
        :param str ivar_name: Ivar name.
        :return: Ivar object based on module name, architecture name, class name and ivar name.
        :rtype: Ivar | None
        """
        # Get Class.
        c = self.get_class(module_name, architecture_name, class_name)
        if not c:
            return None

        # Get Ivar.
        i = c.get_ivar(ivar_name)
        return i


class ClassDumpManager(object):
    """
    Represent list of modules. It loads all data at once.

    :param dict[str, Module] modules: Map of module name to Module object.
    """
    def __init__(self):
        super(ClassDumpManager, self).__init__()
        self.modules = dict()

    def get_module(self, name):
        """
        Returns Module object with given name.

        :param str name: Module name.
        :return: Module object with given name.
        :rtype: Module | None
        """
        if name in self.modules:
            return self.modules[name]
        return None

    def read_directory_path(self, dir_path):
        """
        Reads all module directories from directory.

        :param str dir_path: Path to directory.
        """
        # Go through all files in input directory and read it.
        for module_name in os.listdir(dir_path):
            module_path = os.path.join(dir_path, module_name)
            if os.path.isdir(module_path):
                # Get Module.
                module = self.get_module(module_name)
                if not module:
                    module = Module(module_name)
                    self.modules[module_name] = module
                #  Read Module JSON files.
                module.read_directory_path(module_path)

    def save_to_folder(self, folder_path):
        """
        Saves all classes from all modules as JSON files to given folder path.

        :param str folder_path: Path to output folder.
        """
        folder_path = os.path.normpath(folder_path)

        # Create output directory if needed.
        if len(self.modules) != 0:
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

        # Save every Module.
        for module_name, module in self.modules.iteritems():
            module_path = os.path.join(folder_path, module.name, class_dumps_folder_name)
            module.save_to_folder(module_path)


class Module(object):
    """
    Represents one module. Contains list of architectures.

    :param str name: Module name.
    :param str dir_path: Path to module directory.
    :param dict[str, str] module_file_map: Module map. Maps class name to class file path.
    :param dict[str, Architecture] architectures: Maps architecture name to Architecture object.
    """
    def __init__(self, name, dir_path=None):
        """
        :param str name: Module name.
        """
        super(Module, self).__init__()
        self.name = name
        self.dir_path = dir_path
        self.module_file_map = None
        self.architectures = dict()
        if dir_path:
            self._read_module_map()

    def get_architecture(self, name):
        """
        Finds Architecture object with given name.

        :param str name: Architecture name.
        :return: Architecture object with given name.
        :rtype: Architecture | None
        """
        if name in self.architectures:
            return self.architectures[name]
        return None

    def all_class_names(self):
        """
        Returns a list of all class names from all architectures.

        :return: A list of all class names from all architectures.
        :rtype: list[str]
        """
        s = set()
        for name, architecture in self.architectures.iteritems():
            s = s.union(set(architecture.all_class_names()))
        return list(s)

    def read_directory_path(self, dir_path):
        """
        Reads all files from directory.

        :param str dir_path: Path to directory.
        """
        # Go through all files in input directory and read it.
        for root, dirs, files in os.walk(dir_path):
            for file_name in files:
                # Check if it is a JSON file.
                if not file_name.endswith(".json"):
                    continue

                # File path.
                file_path = os.path.join(root, file_name)
                self.read_file_path(file_path)

    def read_file_path(self, file_path):
        """
        Reads a file at given path.

        :param str file_path: File path.
        """
        with open(file_path, "r") as f:
            self.read_file(f)

    def read_file(self, f):
        """
        Reads a file object.

        :param f: File to read.
        """
        json_data = json.load(f)
        """:type: dict[str, dict]"""
        self.read_json(json_data)

    def read_json(self, json_data):
        """
        Reads a JSON data.

        :param dict[str, dict] json_data: Dictionary representation of JSON data of protocol.
        """
        for architecture_name in json_data:
            architecture = self.get_architecture(architecture_name)
            # Create architecture.
            if not architecture:
                architecture = Architecture(architecture_name)
                self.architectures[architecture_name] = architecture
            architecture.read_json(json_data[architecture_name])

    def save_to_folder(self, folder_path):
        """
        Saves all classes from all architectures as JSON files to given folder path.

        :param str folder_path: Path to output folder.
        """
        # Create output directory if needed.
        if len(self.all_class_names()) != 0:
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

        # Module map.
        module_map = dict()

        # Get every class.
        classes = self.all_class_names()
        for class_name in classes:
            class_data = dict()
            class_file_name = None
            # Get class data from all architectures.
            for name, architecture in self.architectures.iteritems():
                c = architecture.get_class(class_name)
                class_data[architecture.name] = c.json_data()
                class_file_name = c.get_file_name()

            # Module map info.
            module_map[class_name] = class_file_name

            # Save class data to file.
            class_file_path = os.path.join(folder_path, class_file_name)
            with open(class_file_path, "w") as f:
                json.dump(class_data, f, sort_keys=True, indent=2, separators=(",", ":"))
                print("Saving {}.{}.".format(self.name, class_name))

        # Save module map.
        module_map_file_path = os.path.join(folder_path, module_map_file_name)
        with open(module_map_file_path, "w") as f:
            json.dump(module_map, f, sort_keys=True, indent=2, separators=(",", ":"))

    def _read_module_map(self):
        """
        Reads module map file.
        """
        log = logging.getLogger(__name__)
        # Check if module map exists.
        module_map_file_path = os.path.join(self.dir_path, module_map_file_name)
        if not os.path.exists(module_map_file_path):
            log.error("Module: _read_module_map: Cannot find module map \"{}\" at \"{}\".".format(self.name, module_map_file_path))
            raise StandardError()

        # Reads module map into memory.
        with open(module_map_file_path, "r") as f:
            self.module_file_map = json.load(f)

    def get_class_or_load(self, architecture_name, class_name):
        """
        Get Class object for given architecture and class name. Loads data if needed.

        :param str | unicode architecture_name: Architecture name.
        :param str | unicode class_name: Class name.
        :return: Class object for given architecture and class name.
        :rtype: Class | None
        """
        log = logging.getLogger(__name__)
        # Load architecture.
        a = self.get_architecture(architecture_name)
        if not a:
            a = Architecture(architecture_name)
            self.architectures[architecture_name] = a

        # Load class.
        c = a.get_class(class_name)
        if c:
            return c

        # Read class when not yet exists.
        if class_name in self.module_file_map:
            # Get path to class json.
            class_path = self.module_file_map[class_name]
            class_path = os.path.join(self.dir_path, class_path)
            # File doesn't exists.
            if not os.path.exists(class_path):
                log.error("Module: get_class_or_load: Cannot find file: \"{}\".".format(class_path))
                return None

            # Open file.
            with open(class_path, "r") as f:
                json_data = json.load(f)

                # File is empty.
                if not json_data:
                    log.error("Module: get_class_or_load: Cannot open file \"{}\".".format(class_path))
                    return None

                # File doesn't contains architecture information.
                if architecture_name not in json_data:
                    log.error("Module: get_class_or_load: Cannot find architecture in \"{}\".".format(class_path))
                    return None

                # Read JSON data.
                class_data = json_data[architecture_name]
                # Create class object.
                c = a.read_json(class_data)
        return c

    def __str__(self):
        return "<{}: {}>".format(self.__class__.__name__, self.name)


class Architecture(object):
    """
    Represent one CPU architecture.

    :param str name: Name of architecture.
    :param dict[str, Class] classes: Maps class name to Class object.
    """
    def __init__(self, name):
        """
        :param str name: Name of architecture.
        """
        super(Architecture, self).__init__()
        self.name = name
        self.classes = dict()

    def all_class_names(self):
        """
        Returns all class names.

        :return: All class names.
        :rtype: list[str]
        """
        return self.classes.keys()

    def get_class(self, name):
        """
        Returns class with given name.

        :param str name: Class name.
        :return: Class with given name.
        :rtype: Class | None
        """
        if name in self.classes:
            return self.classes[name]
        return None

    def read_json(self, json_data):
        """
        Reads JSON content of class and adds it to the list of classes

        :param dict[str, str | object] json_data: Dictionary representation of JSON data of class.
        :return: Return parsed class.
        :rtype: Class | None
        """
        if json_data is None:
            return None

        if "type" not in json_data:
            return None

        t = json_data["type"]
        if t == "class":
            c = Class(json_data)
            self.classes[c.class_name] = c
            return c
        return None

    def __str__(self):
        return "<{}: {}, classes:{}>".format(self.__class__.__name__, self.name, len(self.classes))


class Protocol(object):
    """
    Represents protocol.

    :param str protocol_name: Protocol name.
    :param list[str] protocols: List of protocols names.
    :param list properties: List of properties.
    :param list class_methods: List of class methods.
    :param list instance_methods: List of instance methods.
    :param list optional_class_methods: List of optional class methods.
    :param list optional_instance_methods: List of optional instance methods.
    :param str type: Type of object (always "protocol").
    """
    def __init__(self, json_data=None):
        """
        :param dict[str, str | list[str] | object] json_data: Dictionary representation of JSON data of protocol.
        """
        super(Protocol, self).__init__()
        self.protocol_name = None
        self.protocols = list()
        self.properties = list()
        self.class_methods = list()
        self.instance_methods = list()
        self.optional_class_methods = list()
        self.optional_instance_methods = list()
        self.type = "protocol"
        self.read_json(json_data)

    def get_file_name(self):
        """
        Returns JSON file name for given protocol.

        :return: JSON file name for given protocol.
        :rtype: str
        """
        return "{}-Protocol.json".format(self.protocol_name)

    def read_json(self, json_data):
        """
        Reads JSON data and stores data in local parameters.

        :param dict[str, str | list[str] | object] json_data: Dictionary representation of JSON data of protocol.
        """
        if json_data is None:
            return

        if "protocolName" in json_data:
            self.protocol_name = json_data["protocolName"]
        if "protocols" in json_data:
            self.protocols = json_data["protocols"]

    def json_data(self):
        """
        Returns JSON representation of Protocol object as dictionary.

        :return: JSON representation of Protocol object as dictionary.
        :rtype: dict[str, str | list[str] | object]
        """
        j = dict()
        """:type: dict[str, str | list[str] | object]"""
        if self.protocol_name:
            j["protocolName"] = self.protocol_name
        if len(self.protocols) > 0:
            j["protocols"] = self.protocols
        j["type"] = self.type
        return j


class Class(Protocol):
    """
    Represents class.

    :param str class_name: Name of class.
    :param str super_class_name: Name of super class.
    :param list[Ivar] ivars: List of ivars.
    :param str type: Type of object (always "class").
    """
    def __init__(self, json_data=None):
        """
        :param dict[str, str | list] json_data: Dictionary representation of JSON data of protocol.
        """
        super(Class, self).__init__()
        self.class_name = None
        self.super_class_name = None
        self.ivars = list()
        self.type = "class"
        self.read_json(json_data)

    def get_file_name(self):
        """
        Returns JSON file name for given class.

        :return: JSON file name for given class.
        :rtype: str
        """
        return "{}.json".format(self.class_name)

    def get_ivar(self, ivar_name):
        """
        Returns ivar with given name.

        :return: ivar with given name.
        :rtype: Ivar | None
        """
        for ivar in self.ivars:
            if ivar.name == ivar_name:
                return ivar
        return None

    def read_json(self, json_data):
        """
        Reads JSON data and stores data in local parameters.

        :param dict[str, str | list] json_data: Dictionary representation of JSON data of protocol.
        """
        if json_data is None:
            return

        super(Class, self).read_json(json_data)
        self.protocol_name = None
        if "className" in json_data:
            self.class_name = json_data["className"]
        if "superClassName" in json_data:
            self.super_class_name = json_data["superClassName"]
        if "ivars" in json_data:
            ivars_j = json_data["ivars"]
            ivars = list()
            """:type: list[Ivar]"""
            for ivar_j in ivars_j:
                ivar = Ivar(ivar_j)
                ivars.append(ivar)
            self.ivars = ivars

    def json_data(self):
        """
        Returns JSON representation of Class object as dictionary.

        :return: JSON representation of Class object as dictionary.
        :rtype: dict[str, str | list]
        """
        j = super(Class, self).json_data()
        # Class name.
        if self.class_name:
            j["className"] = self.class_name
        # Super class name.
        if self.super_class_name:
            j["superClassName"] = self.super_class_name
        # ivars.
        ivars_j = list()
        for ivar in self.ivars:
            ivar_j = ivar.json_data()
            ivars_j.append(ivar_j)
        if len(ivars_j) > 0:
            j["ivars"] = ivars_j
        # Type
        j["type"] = self.type
        return j

    def __str__(self):
        return "<{} {}>".format(self.__class__.__name__, self.class_name)


class Ivar(object):
    """
    Represents ivar.

    :param int alignment: ivar alignment.
    :param str ivarType: Type of ivar.
    :param str name: Name of ivar.
    :param int offset: Offset of ivar.
    :param int size: Size of ivar.
    :param str type: Type of object (always "ivar").
    """
    def __init__(self, json_data=None):
        """
        :param dict[str, str | int] json_data: Dictionary representation of JSON data of ivar.
        """
        super(Ivar, self).__init__()
        self.alignment = None
        self.ivarType = None
        self.name = None
        self.offset = None
        self.size = None
        self.type = "ivar"
        self.read_json(json_data)

    def read_json(self, json_data):
        """
        Reads JSON data and stores data in local parameters.

        :param dict[str, str | int] json_data: Dictionary representation of JSON data of ivar.
        """
        if json_data is None:
            return

        if "alignment" in json_data:
            self.alignment = json_data["alignment"]
        if "ivarType" in json_data:
            self.ivarType = json_data["ivarType"]
        if "name" in json_data:
            self.name = json_data["name"]
        if "offset" in json_data:
            self.offset = json_data["offset"]
        if "size" in json_data:
            self.size = json_data["size"]

    def json_data(self):
        """
        Returns JSON representation of Ivar object as dictionary.

        :return: JSON representation of Ivar object as dictionary.
        :rtype: dict[str, str | int]
        """
        j = dict()
        """:type: dict[str, str | int]"""
        if self.alignment:
            j["alignment"] = self.alignment
        if self.ivarType:
            j["ivarType"] = self.ivarType
        if self.name:
            j["name"] = self.name
        if self.offset:
            j["offset"] = self.offset
        if self.size:
            j["size"] = self.size
        j["type"] = self.type
        return j

    def __str__(self):
        return "<{} {}, {}>".format(self.__class__.__name__, self.name, self.offset)
