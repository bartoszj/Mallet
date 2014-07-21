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


class ArchitecturesList(object):
    def __init__(self):
        super(ArchitecturesList, self).__init__()
        self.architectures = list()

    def architecture(self, name):
        for a in self.architectures:
            if a.name == name:
                return a
        return None

    def all_class_names(self):
        s = set()
        for a in self.architectures:
            s = s.union(set(a.all_class_names()))
        return list(s)

    def read_json(self, j):
        for archName in j:
            architecture = self.architecture(archName)
            if not architecture:
                architecture = Architecture(archName)
                self.architectures.append(architecture)
            architecture.add_json(j[archName])

    def read_file(self, f):
        j = json.load(f)
        self.read_json(j)

    def read_file_path(self, fp):
        with open(fp, "r") as f:
            self.read_file(f)

    def save_to_folder(self, folder_path):
        classes = self.all_class_names()
        for class_name in classes:
            class_data = list()
            for architecture in self.architectures:
                c = architecture.get_class(class_name)
                class_data.append(architecture.json_data_for_object(c))
            print class_data
        print folder_path


class Architecture(object):
    def __init__(self, name):
        super(Architecture, self).__init__()
        self.name = name
        self.protocols = list()
        self.classes = list()
        self.categories = list()

        self._classes_map = None

    def _get_class_map(self):
        # Create class map.
        if self._classes_map is None:
            m = dict()
            for c in self.classes:
                m[c.class_name] = c
            if len(m) > 0:
                self._classes_map = m
        return self._classes_map

    def all_class_names(self):
        self._get_class_map()
        return self._get_class_map().keys()

    def get_class(self, name):
        self._get_class_map()

        if name in self._classes_map:
            return self._classes_map[name]
        return None

    def add_json(self, j):
        if j is None:
            return

        if not "type" in j:
            return

        t = j["type"]
        if t == "class":
            c = Class(j)
            self.classes.append(c)
            self._classes_map = None

    def json_data_for_object(self, o):
        if o is None:
            return None

        oj = o.json_data()

        j = dict()
        j[self.name] = oj

        return j


class Protocol(object):
    def __init__(self, j=None):
        super(Protocol, self).__init__()
        self.protocol_name = None
        self.protocols = None
        self.properties = None
        self.class_methods = None
        self.instance_methods = None
        self.optional_class_methods = None
        self.optional_instance_methods = None
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
        if self.protocols:
            j["protocols"] = self.protocols
        j["type"] = self.type
        return j


class Class(Protocol):
    def __init__(self, j=None):
        super(Class, self).__init__()
        self.class_name = None
        self.super_class_name = None
        self.ivars = None
        self.protocols = None
        self.class_methods = None
        self.type = "class"
        self.read_json(j)

    def file_name(self):
        return "{}.json".format(self.class_name)

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
            if len(ivars) > 0:
                self.ivars = ivars

    def json_data(self):
        j = super(Class, self).json_data()
        if self.class_name:
            j["className"] = self.class_name
        if self.super_class_name:
            j["superClassName"] = self.super_class_name
        if self.ivars:
            ivars_j = list()
            for ivar in self.ivars:
                ivar_j = ivar.json_data()
                ivars_j.append(ivar_j)
            if len(ivars_j) > 0:
                j["ivars"] = ivars_j
        j["type"] = self.type
        return j


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

if __name__ == "__main__":
    pass
