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

import SummaryBase
import NSObject
import Helpers


class NSURLComponentsSyntheticProvider(NSObject.NSObjectSyntheticProvider):
    """
    Class representing NSURLComponents.
    """
    def __init__(self, value_obj, internal_dict):
        super(NSURLComponentsSyntheticProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "__NSConcreteURLComponents"

        self.register_child_value("url_string", ivar_name="_urlString",
                                  primitive_value_function=SummaryBase.get_stripped_summary_value,
                                  summary_function=self.get_url_string_summary)
        self.register_child_value("scheme_component", ivar_name="_schemeComponent",
                                  primitive_value_function=SummaryBase.get_stripped_summary_value,
                                  summary_function=self.get_scheme_component_summary)
        self.register_child_value("user_component", ivar_name="_userComponent",
                                  primitive_value_function=SummaryBase.get_stripped_summary_value,
                                  summary_function=self.get_user_component_summary)
        self.register_child_value("password_component", ivar_name="_passwordComponent",
                                  primitive_value_function=SummaryBase.get_stripped_summary_value,
                                  summary_function=self.get_password_component_summary)
        self.register_child_value("host_component", ivar_name="_hostComponent",
                                  primitive_value_function=SummaryBase.get_stripped_summary_value,
                                  summary_function=self.get_host_component_summary)
        self.register_child_value("port_component", ivar_name="_portComponent",
                                  primitive_value_function=SummaryBase.get_description_value,
                                  summary_function=self.get_port_component_summary)
        self.register_child_value("path_component", ivar_name="_pathComponent",
                                  primitive_value_function=SummaryBase.get_stripped_summary_value,
                                  summary_function=self.get_path_component_summary)
        self.register_child_value("query_component", ivar_name="_queryComponent",
                                  primitive_value_function=SummaryBase.get_stripped_summary_value,
                                  summary_function=self.get_query_component_summary)
        self.register_child_value("fragment_component", ivar_name="_fragmentComponent",
                                  primitive_value_function=SummaryBase.get_stripped_summary_value,
                                  summary_function=self.get_fragment_component_summary)

    @staticmethod
    def get_url_string_summary(value):
        return "url=\"{}\"".format(value)

    @staticmethod
    def get_scheme_component_summary(value):
        return "scheme=\"{}\"".format(value)

    @staticmethod
    def get_user_component_summary(value):
        return "user=\"{}\"".format(value)

    @staticmethod
    def get_password_component_summary(value):
        return "password=\"{}\"".format(value)

    @staticmethod
    def get_host_component_summary(value):
        return "host=\"{}\"".format(value)

    @staticmethod
    def get_port_component_summary(value):
        return "port={}".format(value)

    @staticmethod
    def get_path_component_summary(value):
        return "path=\"{}\"".format(value)

    @staticmethod
    def get_query_component_summary(value):
        return "query=\"{}\"".format(value)

    @staticmethod
    def get_fragment_component_summary(value):
        return "fragment=\"{}\"".format(value)

    def summary(self):
        summary = SummaryBase.join_summaries(self.url_string_summary, self.scheme_component_summary,
                                             self.user_component_summary, self.password_component_summary,
                                             self.host_component_summary, self.port_component_summary,
                                             self.path_component_summary, self.query_component_summary,
                                             self.fragment_component_summary)
        return summary


def summary_provider(value_obj, internal_dict):
    return Helpers.generic_summary_provider(value_obj, internal_dict, NSURLComponentsSyntheticProvider)


def __lldb_init_module(debugger, dictionary):
    debugger.HandleCommand("type summary add -F NSURLComponents.summary_provider \
                            --category Foundation \
                            NSURLComponents __NSConcreteURLComponents")
    debugger.HandleCommand("type category enable Foundation")