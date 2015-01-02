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
import imp

try:
    import LLDBLogger
except ImportError:
    imp.load_source("LLDBLogger", "LLDBScripts/Scripts/ClassDump.py")
    import LLDBLogger

class_map_file_name = "class.map"


class LazyArchitecturesList(object):
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
        super(LazyArchitecturesList, self).__init__()
        logger = logging.getLogger(__name__)
        logger.debug("LazyArchitecturesList: created.")
        self.dir_path = dir_path        # Path from where classes are read.
        self.architectures = list()     # List of architectures.
        self.class_map = None           # Maps class name to path to file.
        self._read_class_map()

    def _read_class_map(self):
        """
        Reads class.map file into memory (self.class_map).
        """
        logger = logging.getLogger(__name__)
        logger.debug("LazyArchitecturesList: reading class_map.")
        class_map_file_path = os.path.join(self.dir_path, class_map_file_name)
        if not os.path.exists(class_map_file_path):
            logger.error("LazyArchitecturesList: Cannot find class.map file.")
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
        logger = logging.getLogger(__name__)
        # Checks parameters.
        if architecture_name is None or class_name is None or ivar_name is None:
            logger.error("LazyArchitecturesList: get_ivar: invalid parameters.")
            return None

        # Check if class exists in class.map.
        if class_name not in self.class_map:
            logger.error("LazyArchitecturesList: get_ivar: no class \"{}\" in class_map.".format(class_name))
            return None

        # Get architecture.
        architecture = self.get_architecture(architecture_name)
        if architecture is None:
            # Create new architecture.
            architecture = Architecture(architecture_name)
            self.architectures.append(architecture)

        # Get class.
        cl = architecture.get_class(class_name)
        if cl is None:
            # Reads JSON from file.
            logger.info("LazyArchitecturesList: get_ivar: reading \"{}\".".format(self.class_map[class_name]))
            file_path = os.path.join(self.dir_path, self.class_map[class_name])
            if not os.path.exists(file_path):
                logger.error("LazyArchitecturesList: get_ivar: missing \"{}\".".format(self.class_map[class_name]))
                return None
            j = self.read_file_path(file_path)

            # Empty json data or missing architecture in JSON.
            if j is None or architecture_name not in j:
                logger.error("LazyArchitecturesList: get_ivar: missing data in \"{}\".".format(self.class_map[class_name]))
                return None

            # Get class json for given architecture.
            class_json = j[architecture_name]

            # Add class to architecture.
            cl = architecture.add_json(class_json)

        # Get ivar.
        ivar = cl.get_ivar(ivar_name)
        # If ivar doesn't exists then look for it in super class.
        if ivar is None and cl.super_class_name is not None:
            return self.get_ivar(architecture_name, cl.super_class_name, ivar_name)

        if ivar is None:
            logger.error("LazyArchitecturesList: get_ivar: no ivar \"{}\" for class \"{}\".".format(ivar_name, class_name))
        return ivar


class ArchitecturesList(object):
    """
    Represent list of architectures. It loads all data at once.

    :param list[Architecture] architectures: List of architectures.
    """
    def __init__(self):
        super(ArchitecturesList, self).__init__()
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

    def read_json(self, json_data, framework):
        """
        Reads a JSON data.

        :param dict[str, dict] json_data: Dictionary representation of JSON data of protocol.
        :param str framework: Framework name.
        """
        for archName in json_data:
            architecture = self.get_architecture(archName)
            # Create architecture.
            if not architecture:
                architecture = Architecture(archName)
                self.architectures.append(architecture)
            architecture.add_json(json_data[archName], framework)

    def read_file(self, f, framework):
        """
        Reads a file object.

        :param f: File to read.
        :param str framework: Framework name.
        """
        json_data = json.load(f)
        """:type: dict[str, dict]"""
        self.read_json(json_data, framework)

    def read_file_path(self, file_path, framework):
        """
        Reads a file at given path.

        :param str file_path: File path.
        :param str framework: Framework name.
        """
        with open(file_path, "r") as f:
            self.read_file(f, framework)

    def read_directory_path(self, dir_path):
        """
        Reads all files from directory.

        :param str dir_path: Path to directory.
        """
        # Go through all files in input directory and read it.
        for root, dirs, files in os.walk(dir_path):
            for f in files:
                # Check if it is a JSON file.
                if not f.endswith(".json"):
                    continue

                # Framework.
                framework_name = root.replace(dir_path, "").strip("/")

                # File path.
                fi_path = os.path.join(root, f)
                self.read_file_path(fi_path, framework_name)

    def save_to_folder(self, folder_path):
        """
        Saves all classes as JSON files to given folder path.

        :param str folder_path: Path to output folder.
        """
        classes = self.all_class_names()
        class_map = list()
        """:type: list[str]"""
        for class_name in classes:
            # Get class data.
            class_data = dict()
            """:type: dict[str, dict]"""
            framework_name = None
            file_name = None
            # Get class data from all architectures.
            for architecture in self.architectures:
                c = architecture.get_class(class_name)
                framework_name = c.framework_name
                file_name = c.file_name()
                class_data[architecture.name] = c.json_data()

            # Data for class map.
            class_map.append("{}:{}/{}".format(class_name, framework_name, file_name))

            # Output directory path.
            output_dir_path = os.path.join(folder_path, framework_name)
            # Create output directory if needed.
            if not os.path.exists(output_dir_path):
                os.makedirs(output_dir_path)

            # Output file path.
            output_file_path = os.path.join(output_dir_path, file_name)
            # Saving.
            with open(output_file_path, "w") as output_file:
                json.dump(class_data, output_file, sort_keys=True, indent=2, separators=(",", ":"))
                print "Saving {}".format(class_name)

        # Class map file.
        class_map_file_path = os.path.join(folder_path, class_map_file_name)
        class_map_str = "\n".join(class_map)
        with open(class_map_file_path, "w") as class_map_file:
            class_map_file.write(class_map_str)

    def fix_ivars_offset(self, offsets_file_path):
        """
        Fixes ivars offset using offset information from file.

        :param str offsets_file_path: Path to offsets.json file.
        """
        # Current directory path.
        current_dir = os.path.abspath(__file__)
        current_dir, _ = os.path.split(current_dir)

        # offsets.json file doesn't exists.
        if not os.path.exists(offsets_file_path):
            print "Offset file doesn't exists."
            exit(1)

        # Read offsets.json file.
        with open(offsets_file_path, "r") as offsets_file:
            offsets = json.load(offsets_file)
            """:type: dict[str, list]"""

            # Go through all architectures and fix offsets.
            for architecture in self.architectures:
                if architecture.name not in offsets:
                    print "No architecture {} in offsets.".format(architecture.name)
                    continue
                architecture.fix_ivars_offset(offsets[architecture.name])


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

    def add_json(self, json_data, framework=None):
        """
        Reads JSON content of class and adds it to the list of classes

        :param dict[str, str | object] json_data: Dictionary representation of JSON data of class.
        :param str framework: Name of framework (optional).
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
            c.framework_name = framework
            self.classes.append(c)
            self._classes_map = None
            return c
        return None

    def class_inheritance(self, cl):
        """
        Returns class hierarchy as list.

        :param Class cl: Class.
        :return: Class hierarchy as list.
        :rtype: list[str]
        """
        ci = [cl.class_name, cl.super_class_name]

        super_class_name = cl.super_class_name
        while super_class_name:
            super_cl = self.get_class(super_class_name)
            if super_cl:
                # Adds super class name to the end of the list.
                ci.append(super_cl.super_class_name)
                super_class_name = super_cl.super_class_name
            else:
                super_class_name = None

        return ci

    def class_offset_for_class(self, cl, offsets_list):
        """
        Returns ClassOffset object for given Class object from list of offsets.

        :param Class cl: Class.
        :param OffsetsList offsets_list: Offsets list.
        :return: ClassOffset object for given Class object from list of offsets.
        :rtype: ClassOffset | None
        """
        class_inheritance = self.class_inheritance(cl)
        for class_name in class_inheritance:
            # Looks for ClassOffset from class list.
            if offsets_list.has_class_offset(class_name):
                return offsets_list.get_class_offset(class_name)
            # Looks for ClassOffset from super class list.
            if offsets_list.has_super_class_offset(class_name):
                return offsets_list.get_super_class_offset(class_name)
        return None

    def fix_ivars_offset(self, offsets):
        """
        Adds offset to ivars using content from JSON.

        :param list[dict[str, str | int]] offsets: Dictionary representation of JSON data of list of class offsets.
        """
        offsets_list = OffsetsList(offsets)
        for cl in self.classes:
            class_offset = self.class_offset_for_class(cl, offsets_list)
            if class_offset:
                cl.fix_ivars_offset(class_offset)


class Protocol(object):
    """
    Represents protocol.

    :param str framework_name: Framework name.
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
        self.framework_name = None
        self.protocol_name = None
        self.protocols = list()
        self.properties = list()
        self.class_methods = list()
        self.instance_methods = list()
        self.optional_class_methods = list()
        self.optional_instance_methods = list()
        self.type = "protocol"
        self.read_json(json_data)

    def file_name(self):
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

    def file_name(self):
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

    def fix_ivars_offset(self, offset):
        """
        Fix (add) ivar offsets based on offsets.json.

        :param ClassOffset offset: Offsets for current class.
        """
        for ivar in self.ivars:
            ivar.offset += offset.offset


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


class OffsetsList(object):
    """
    Represents offsets values for all classes (for one architecture) in offsets.json file.

    :param list[ClassOffset] list: List of offsets.
    :param dict[str, ClassOffset] _classes_map: Map of classes and its offset.
    :param dict[str, ClassOffset] _super_classes_map: Map of super classes and its offset.
    """
    def __init__(self, json_data):
        """
        :param list[dict[str, str | int]] json_data: Dictionary representation of JSON data of list of class offsets.
        """
        super(OffsetsList, self).__init__()
        self.list = None
        self._classes_map = dict()
        self._super_classes_map = dict()
        self._read_json(json_data)
        self._get_class_map()

    def _read_json(self, json_data):
        """
        Reads JSON data and creates ClassOffset objects.

        :param list[dict[str, str | int]] json_data: Dictionary representation of JSON data of list of class offsets.
        """
        l = list()
        """:type: list[ClassOffset]"""
        for cl in json_data:
            o = ClassOffset(cl)
            l.append(o)
        self.list = l

    def _get_class_map(self):
        """
        Create class map and super class map.
        """
        if self._classes_map is None:
            cm = dict()
            """:type: dict[str, ClassOffset]"""
            scm = dict()
            """:type: dict[str, ClassOffset]"""
            for c in self.list:
                if c.class_name is not None:
                    cm[c.class_name] = c
                if c.super_class_name is not None:
                    scm[c.super_class_name] = c
            self._classes_map = cm
            self._super_classes_map = scm

    def has_class_offset(self, class_name):
        """
        Checks if object has offset for given class name.

        :param str class_name: Class name.
        :return: True if offset for given class exists.
        :rtype: bool
        """
        if class_name in self._classes_map:
            return True
        return False

    def has_super_class_offset(self, super_class_name):
        """
        Checks if object has offset for given super class name.

        :param str super_class_name: Super class name.
        :return: True if offset for given super class exists.
        :rtype: bool
        """
        if super_class_name in self._super_classes_map:
            return True
        return False

    def get_class_offset(self, class_name):
        """
        Returns class offset for given class name.

        :param str class_name: Class name.
        :return: Offset for given class.
        :rtype: ClassOffset | None
        """
        if class_name in self._classes_map:
            return self._classes_map[class_name]
        return None

    def get_super_class_offset(self, super_class_name):
        """
        Returns class offset for given super class name.

        :param str super_class_name: Super class name.
        :return: Offset for given super class.
        :rtype: ClassOffset | None
        """
        if super_class_name in self._super_classes_map:
            return self._super_classes_map[super_class_name]
        return None


class ClassOffset(object):
    """
    Represent class offset from offsets.json file.

    :param str class_name: Class name.
    :param str super_class_name: Super class name.
    :param int offset: Offset.
    """
    def __init__(self, json_data):
        """
        :param dict[str, str | int] json_data: Dictionary representation of JSON data of class offset.
        """
        super(ClassOffset, self).__init__()
        self.class_name = None
        self.super_class_name = None
        self.offset = None
        self._read_json(json_data)

    def _read_json(self, json_data):
        """
        Reads JSON data and stores data in local parameters.

        :param dict[str, str | int] json_data: Dictionary representation of JSON data.
        """
        if "class" in json_data:
            self.class_name = json_data["class"]
        if "super_class" in json_data:
            self.super_class_name = json_data["super_class"]
        self.offset = json_data["offset"]


if __name__ == "__main__":
    pass
