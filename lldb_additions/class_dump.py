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


logger.configure_loggers()
class_dumps_folder_name = "class_dumps"
module_map_file_name = "module_map.json"


class LazyClassDumpManager(object):
    """
    Lazy loads class data into memory.

    :param str dir_path: Path to directory where class dumps are stored.
    :param list[Architecture] architectures: List of architectures.
    :param dict[str, str] class_map: Maps class name to path to file.
    """
    def __init__(self, dir_path):
        """
        :param str dir_path: Path to directory where class dumps are stored.
        """
        super(LazyClassDumpManager, self).__init__()
        log = logging.getLogger(__name__)
        log.debug("LazyClassDumpManager: created.")
        self.dir_path = dir_path        # Path from where classes are read.
        self.architectures = list()     # List of architectures.
        self.class_map = None           # Maps class name to path to file.
        self._read_class_map()

    def _read_class_map(self):
        """
        Reads class.map file into memory (self.class_map).
        """
        log = logging.getLogger(__name__)
        log.debug("LazyClassDumpManager: reading class_map.")
        class_map_file_path = os.path.join(self.dir_path, class_map_file_name)
        if not os.path.exists(class_map_file_path):
            log.error("LazyClassDumpManager: Cannot find class.map file.")
            raise StandardError()

        with open(class_map_file_path, "r") as class_map_file:
            class_map = dict()
            """:type: dict[str, str]"""
            # Reads whole file and split it on new line.
            class_map_file_str = class_map_file.read()
            class_map_list = class_map_file_str.split("\n")
            for class_data in class_map_list:
                # Split each line.
                class_data_parts = class_data.split(":")
                class_name = class_data_parts[0]
                class_file_path = class_data_parts[1]
                # Saves data to class_map variable.
                class_map[class_name] = class_file_path
            self.class_map = class_map

    def read_file(self, f):
        """
        Reads JSON data from file object.

        :param f: File to read.
        :return: Dictionary representing JSON data.
        :rtype: dict[str, dict]
        """
        j = json.load(f)
        return j

    def read_file_path(self, file_path):
        """
        Reads JSON data from file at given file path.

        :param file_path:
        :return: Dictionary representing JSON data.
        :rtype: dict[str, dict]
        """
        with open(file_path, "r") as f:
            return self.read_file(f)

    def get_architecture(self, name):
        """
        Returns Architecture object with given name.

        :param str name: Architecture name.
        :return: Architecture object with given name.
        :rtype: Architecture | None
        """
        for a in self.architectures:
            if a.name == name:
                return a
        return None

    def get_architecture_or_create(self, name):
        """
        Returns Architecture object with given name or create it if was not in the list.

        :param str name: Architecture name.
        :return: Architecture object with given name.
        :rtype: Architecture
        """
        for a in self.architectures:
            if a.name == name:
                return a
        # Create new architecture.
        architecture = Architecture(name)
        self.architectures.append(architecture)
        return architecture

    def get_class_or_load(self, architecture_name, class_name):
        """
        Returns Class object for given architecture or load class JSON file.
        :param str architecture_name: Architecture name.
        :param str class_name: Class name.
        :return: Class object.
        :rtype: Class
        """
        log = logging.getLogger(__name__)
        architecture = self.get_architecture_or_create(architecture_name)

        # Get class.
        cl = architecture.get_class(class_name)
        if cl is None:
            # Reads JSON from file.
            log.info("LazyClassDumpManager: get_class_or_load: reading \"{}\".".format(self.class_map[class_name]))
            file_path = os.path.join(self.dir_path, self.class_map[class_name])
            if not os.path.exists(file_path):
                log.error("LazyClassDumpManager: get_class_or_load: missing \"{}\".".format(self.class_map[class_name]))
                return None
            j = self.read_file_path(file_path)

            # Empty json data or missing architecture in JSON.
            if j is None or architecture_name not in j:
                log.error("LazyClassDumpManager: get_class_or_load: missing data in \"{}\".".format(self.class_map[class_name]))
                return None

            # Get class json for given architecture.
            class_json = j[architecture_name]

            # Add class to architecture.
            cl = architecture.read_json(class_json)
        return cl

    def get_ivar(self, architecture_name, class_name, ivar_name):
        """
        Returns Ivar object based on architecture name, class name and ivar name.

        Supported architectures: armv7, armv7s, arm64, i386, x86_64.

        :param str architecture_name: Architecture name.
        :param str class_name: Class name.
        :param str ivar_name: Ivar name.
        :return: Ivar object based on architecture name, class name and ivar name.
        :rtype: Ivar | None
        """
        log = logging.getLogger(__name__)
        # Checks parameters.
        if architecture_name is None or class_name is None or ivar_name is None:
            log.error("LazyClassDumpManager: get_ivar: invalid parameters.")
            return None

        # Check if class exists in class.map.
        if class_name not in self.class_map:
            log.error("LazyClassDumpManager: get_ivar: no class \"{}\" in class_map.".format(class_name))
            return None

        # Get class.
        cl = self.get_class_or_load(architecture_name, class_name)

        # Get ivar.
        ivar = cl.get_ivar(ivar_name)
        # If ivar doesn't exists then look for it in super class.
        if ivar is None and cl.super_class_name is not None:
            return self.get_ivar(architecture_name, cl.super_class_name, ivar_name)

        if ivar is None:
            log.error("LazyClassDumpManager: get_ivar: no ivar \"{}\" for class \"{}\".".format(ivar_name, class_name))
        return ivar


class ClassDumpManager(object):
    """
    Represent list of modules. It loads all data at once.

    :param list[Module] modules: List of architectures.
    """
    def __init__(self):
        super(ClassDumpManager, self).__init__()
        self.modules = list()

    def get_module(self, name):
        """
        Finds Module object with given name.

        :param str name: Module name.
        :return: Module object with given name.
        :rtype: Module | None
        """
        for a in self.modules:
            if a.name == name:
                return a
        return None

    # def all_class_names(self):
    #     """
    #     Returns a list of all class names from all architectures.
    #
    #     :return: A list of all class names from all architectures.
    #     :rtype: list[str]
    #     """
    #     s = set()
    #     for a in self.modules:
    #         s = s.union(set(a.all_class_names()))
    #     return list(s)

    def read_directory_path(self, dir_path):
        """
        Reads all module directories from directory.

        :param str dir_path: Path to directory.
        """
        # Go through all files in input directory and read it.
        for module_name in os.listdir(dir_path):
            module_path = os.path.join(dir_path, module_name)
            if os.path.isdir(module_path):
                module = self.get_module(module_name)
                if not module:
                    module = Module(module_name)
                    self.modules.append(module)
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

        for module in self.modules:
            module_path = os.path.join(folder_path, module.name, class_dumps_folder_name)
            module.save_to_folder(module_path)


class Module(object):
    """
    Represents one module. Contains list of architectures.

    :param str name: Module name.
    :param list[Architecture] architectures: List of architectures.
    """
    def __init__(self, name):
        """
        :param str name: Module name.
        """
        super(Module, self).__init__()
        self.name = name
        self.architectures = list()

    def get_architecture(self, name):
        """
        Finds Architecture object with given name.

        :param str name: Architecture name.
        :return: Architecture object with given name.
        :rtype: Architecture | None
        """
        for a in self.architectures:
            if a.name == name:
                return a
        return None

    def all_class_names(self):
        """
        Returns a list of all class names from all architectures.

        :return: A list of all class names from all architectures.
        :rtype: list[str]
        """
        s = set()
        for a in self.architectures:
            s = s.union(set(a.all_class_names()))
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
        for archName in json_data:
            architecture = self.get_architecture(archName)
            # Create architecture.
            if not architecture:
                architecture = Architecture(archName)
                self.architectures.append(architecture)
            architecture.read_json(json_data[archName])

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
            for a in self.architectures:
                c = a.get_class(class_name)
                class_data[a.name] = c.json_data()
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

    def __str__(self):
        return "<{}: {}>".format(self.__class__.__name__, self.name)


class Architecture(object):
    """
    Represent one CPU architecture.

    :param str name: Name of architecture.
    :param list[Protocol] protocols: List of protocols.
    :param list[Class] classes: List of classes.
    :param dict[str, Class] _classes_map: Maps class name to Class object.
    """
    def __init__(self, name):
        """
        :param str name: Name of architecture.
        """
        super(Architecture, self).__init__()
        self.name = name            # Architecture name.
        self.protocols = list()     # List of protocols.
        self.classes = list()       # List of classes.

        self._classes_map = None    # Maps class name to Class object.

    def _get_class_map(self):
        """
        Creates class map. Maps class name to Class object.

        :return: Returns class map.
        :rtype: dict[str, Class]
        """
        # Create class map.
        if self._classes_map is None:
            m = dict()
            """:type: dict[str, Class]"""
            for c in self.classes:
                m[c.class_name] = c
            if len(m) > 0:
                self._classes_map = m
        return self._classes_map

    def all_class_names(self):
        """
        Returns all class names.

        :return: All class names.
        :rtype: list[str]
        """
        self._get_class_map()
        return self._classes_map.keys()

    def get_class(self, name):
        """
        Returns class with given name.

        :param str name: Class name.
        :return: Class with given name.
        :rtype: Class | None
        """
        self._get_class_map()
        if self._classes_map is None:
            return None

        if name in self._classes_map:
            return self._classes_map[name]
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
            self.classes.append(c)
            self._classes_map = None
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
