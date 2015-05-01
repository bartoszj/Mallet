#! /usr/bin/env python
# -*- coding: utf-8 -*-

# The MIT License (MIT)
#
# Copyright (c) 2015 Bartosz Janda
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

from ...scripts import helpers
from ..Foundation import NSObject
from .. import SummaryBase


class UINibStorageSyntheticProvider(NSObject.NSObjectSyntheticProvider):
    """
    Class representing UINibStorage.
    """
    def __init__(self, value_obj, internal_dict):
        super(UINibStorageSyntheticProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "UINibStorage"

        self.register_child_value("bundle_resource_name", ivar_name="bundleResourceName",
                                  primitive_value_function=SummaryBase.get_summary_value,
                                  summary_function=self.get_bundle_resource_name_summary)
        self.register_child_value("bundle_directory_name", ivar_name="bundleDirectoryName",
                                  primitive_value_function=SummaryBase.get_summary_value,
                                  summary_function=self.get_bundle_directory_name_summary)
        self.register_child_value("identifier_for_strings_file", ivar_name="identifierForStringsFile",
                                  primitive_value_function=SummaryBase.get_summary_value,
                                  summary_function=self.get_identifier_for_strings_file_summary)

    @staticmethod
    def get_bundle_resource_name_summary(value):
        return "resourceName={}".format(value)

    @staticmethod
    def get_bundle_directory_name_summary(value):
        return "dictionaryName={}".format(value)

    @staticmethod
    def get_identifier_for_strings_file_summary(value):
        return "identifierForStringsFile={}".format(value)

    def summaries_parts(self):
        return [self.bundle_resource_name_summary,
                self.bundle_directory_name_summary,
                self.identifier_for_strings_file_summary]


def summary_provider(value_obj, internal_dict):
    return helpers.generic_summary_provider(value_obj, internal_dict, UINibStorageSyntheticProvider)
