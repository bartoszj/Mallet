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
import imp


try:
    import LLDBLogger
except ImportError:
    pass


class_map_file_name = "class.map"


class LazyArchitecturesList(object):
    """
    Lazy loads class data into memory.
    """
    def __init__(self, dir_path):
        super(LazyArchitecturesList, self).__init__()
        LLDBLogger.get_logger().debug("LazyArchitecturesList: created.")
        self.dir_path = dir_path        # Path from where classes are read.
        self.architectures = list()     # List of architectures.
        self.class_map = None           # Maps class name to path to file.
        self._read_class_map()

    def _read_class_map(self):
        """
        Reads class.map file into memory (self.class_map).
        """
        LLDBLogger.get_logger().debug("LazyArchitecturesList: reading class map.")
        class_map_file_path = os.path.join(self.dir_path, class_map_file_name)
        if not os.path.exists(class_map_file_path):
            LLDBLogger.get_logger().error("LazyArchitecturesList: Cannot find class.map file.")
            raise StandardError()

        with open(class_map_file_path, "r") as class_map_file:
            class_map = dict()
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
        """
        j = json.load(f)
        return j

    def read_file_path(self, file_path):
        """
        Reads JSON data from file at given file path.
        """
        with open(file_path, "r") as f:
            return self.read_file(f)

    def get_architecture(self, name):
        """
        Returns Architecture object based on name.
        """
        for a in self.architectures:
            if a.name == name:
                return a
        return None

    def get_ivar(self, architecture_name, class_name, ivar_name):
        """
        Returns Ivar object based on architecture name, class name and ivar name.

        Supported architectures: armv7, armv7s, arm64, i386, x86_64.
        """
        # Checks parameters.
        if architecture_name is None or class_name is None or ivar_name is None:
            LLDBLogger.get_logger().error("LazyArchitecturesList: get_ivar: invalid parameters.")
            return None

        # Check if class exists in class.map.
        if class_name not in self.class_map:
            LLDBLogger.get_logger().error("LazyArchitecturesList: get_ivar: no class {} in class_map.".format(class_name))
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
            LLDBLogger.get_logger().info("LazyArchitecturesList: get_ivar: reading \"{}\".".format(self.class_map[class_name]))
            file_path = os.path.join(self.dir_path, self.class_map[class_name])
            j = self.read_file_path(file_path)

            # Empty json data or missing architecture in JSON.
            if j is None or architecture_name not in j:
                LLDBLogger.get_logger().error("LazyArchitecturesList: get_ivar: missing data in \"{}\".".format(self.class_map[class_name]))
                return

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
            LLDBLogger.get_logger().error("LazyArchitecturesList: get_ivar: no ivar \"{}\" for class \"{}\".".format(ivar_name, class_name))
        return ivar


class ArchitecturesList(object):
    """
    Represent list of architectures. It loads all data at once.
    """
    def __init__(self):
        super(ArchitecturesList, self).__init__()
        self.architectures = list()

    def get_architecture(self, name):
        """
        Finds Architecture object with given name.
        """
        for a in self.architectures:
            if a.name == name:
                return a
        return None

    def all_class_names(self):
        """
        Returns a list of all classe names from all architectures.
        """
        s = set()
        for a in self.architectures:
            s = s.union(set(a.all_class_names()))
        return list(s)

    def read_json(self, j, framework):
        """
        Reads a JSON content.
        """
        for archName in j:
            architecture = self.get_architecture(archName)
            if not architecture:
                architecture = Architecture(archName)
                self.architectures.append(architecture)
            architecture.add_json(j[archName], framework)

    def read_file(self, f, framework):
        """
        Reads a file object.
        """
        j = json.load(f)
        self.read_json(j, framework)

    def read_file_path(self, fp, framework):
        """
        Reads a file at given path.
        """
        with open(fp, "r") as f:
            self.read_file(f, framework)

    def read_directory_path(self, dir_path):
        """
        Reads all files from directory.
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
        """
        classes = self.all_class_names()
        class_map = list()
        for class_name in classes:
            # Get class data.
            class_data = dict()
            framework_name = None
            file_name = None
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
        """
        # Current directory path.
        current_dir = os.path.abspath(__file__)
        current_dir, _ = os.path.split(current_dir)

        # Finds offsets.json file.
        if not os.path.exists(offsets_file_path):
            print "Offset file doesn't exists."
            exit()

        # Read offsets.json file.
        with open(offsets_file_path, "r") as offsets_file:
            offsets = json.load(offsets_file)

            # Go through all architectures and fix offsets.
            for architecture in self.architectures:
                if architecture.name not in offsets:
                    print "No architecture {} in offsets.".format(architecture.name)
                    continue
                architecture.fix_ivars_offset(offsets[architecture.name])


class Architecture(object):
    """
    Represent one architecture.
    """
    def __init__(self, name):
        super(Architecture, self).__init__()
        self.name = name            # Architecture name.
        self.protocols = list()     # List of protocols.
        self.classes = list()       # List of classes.
        self.categories = list()    # List of categories.

        self._classes_map = None    # Maps class name to Class object.

    def _get_class_map(self):
        """
        Creates class map. Maps class name to Class object.
        """
        # Create class map.
        if self._classes_map is None:
            m = dict()
            for c in self.classes:
                m[c.class_name] = c
            if len(m) > 0:
                self._classes_map = m
        return self._classes_map

    def all_class_names(self):
        """
        Returns all class names.
        """
        self._get_class_map()
        return self._get_class_map().keys()

    def get_class(self, name):
        """
        Returns class with given name.
        """
        self._get_class_map()
        if self._classes_map is None:
            return None

        if name in self._classes_map:
            return self._classes_map[name]
        return None

    def add_json(self, j, framework=None):
        """
        Reads JSON content for architecture.
        """
        if j is None:
            return

        if not "type" in j:
            return

        t = j["type"]
        if t == "class":
            c = Class(j)
            c.framework_name = framework
            self.classes.append(c)
            self._classes_map = None
            return c

    def class_inheritance(self, cl):
        """
        Returns class hierarchy as list.
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
        Returns ClassOffset object for given Class object.
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
        """
        offsets_list = OffsetsList(offsets)
        for cl in self.classes:
            class_offset = self.class_offset_for_class(cl, offsets_list)
            if class_offset:
                cl.fix_ivars_offset(class_offset)


class Protocol(object):
    def __init__(self, j=None):
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
        self.read_json(j)

    def file_name(self):
        return "{}-Protocol.json".format(self.protocol_name)

    def read_json(self, j):
        if j is None:
            return

        if "protocolName" in j:
            self.protocol_name = j["protocolName"]
        if "protocols" in j:
            self.protocols = j["protocols"]

    def json_data(self):
        j = dict()
        if self.protocol_name:
            j["protocolName"] = self.protocol_name
        if len(self.protocols) > 0:
            j["protocols"] = self.protocols
        j["type"] = self.type
        return j


class Class(Protocol):
    def __init__(self, j=None):
        super(Class, self).__init__()
        self.class_name = None
        self.super_class_name = None
        self.ivars = list()
        self.type = "class"
        self.read_json(j)

    def file_name(self):
        return "{}.json".format(self.class_name)

    def get_ivar(self, ivar_name):
        for ivar in self.ivars:
            if ivar.name == ivar_name:
                return ivar
        return None

    def read_json(self, j):
        if j is None:
            return

        super(Class, self).read_json(j)
        self.protocol_name = None
        if "className" in j:
            self.class_name = j["className"]
        if "superClassName" in j:
            self.super_class_name = j["superClassName"]
        if "ivars" in j:
            ivars_j = j["ivars"]
            ivars = list()
            for ivar_j in ivars_j:
                ivar = Ivar(ivar_j)
                ivars.append(ivar)
            self.ivars = ivars

    def json_data(self):
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
        for ivar in self.ivars:
            ivar.offset += offset.offset


class Ivar(object):
    def __init__(self, j=None):
        super(Ivar, self).__init__()
        self.alignment = None
        self.ivarType = None
        self.name = None
        self.offset = None
        self.size = None
        self.type = "ivar"
        self.read_json(j)

    def read_json(self, j):
        if j is None:
            return

        if "alignment" in j:
            self.alignment = j["alignment"]
        if "ivarType" in j:
            self.ivarType = j["ivarType"]
        if "name" in j:
            self.name = j["name"]
        if "offset" in j:
            self.offset = j["offset"]
        if "size" in j:
            self.size = j["size"]

    def json_data(self):
        j = dict()
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
    def __init__(self, json_data):
        super(OffsetsList, self).__init__()
        self.list = None
        self._classes_map = None
        self._super_classes_map = None
        self._read_json(json_data)

    def _get_class_map(self):
        # Create class map.
        if self._classes_map is None:
            cm = dict()
            scm = dict()
            for c in self.list:
                if c.class_name is not None:
                    cm[c.class_name] = c
                if c.super_class_name is not None:
                    scm[c.super_class_name] = c
            if len(cm) > 0:
                self._classes_map = cm
            if len(scm) > 0:
                self._super_classes_map = scm

    def _read_json(self, json_data):
        l = list()
        for cl in json_data:
            o = ClassOffset(cl)
            l.append(o)

        if len(l) > 0:
            self.list = l

    def has_class_offset(self, class_name):
        self._get_class_map()
        if self._classes_map is None:
            return False

        if class_name in self._classes_map:
            return True
        return False

    def has_super_class_offset(self, super_class_name):
        self._get_class_map()
        if self._super_classes_map is None:
            return False

        if super_class_name in self._super_classes_map:
            return True
        return False

    def get_class_offset(self, class_name):
        self._get_class_map()
        if self._classes_map is None:
            return None

        if class_name in self._classes_map:
            return self._classes_map[class_name]
        return None

    def get_super_class_offset(self, super_class_name):
        self._get_class_map()
        if self._super_classes_map is None:
            return None

        if super_class_name in self._super_classes_map:
            return self._super_classes_map[super_class_name]
        return None


class ClassOffset(object):
    def __init__(self, json_data):
        super(ClassOffset, self).__init__()
        self.class_name = None
        self.super_class_name = None
        self.offset = None
        self._read_json(json_data)

    def _read_json(self, json_data):
        if "class" in json_data:
            self.class_name = json_data["class"]
        if "super_class" in json_data:
            self.super_class_name = json_data["super_class"]
        self.offset = json_data["offset"]


if __name__ == "__main__":
    pass
