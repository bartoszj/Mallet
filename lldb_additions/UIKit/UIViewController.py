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

from .. import helpers
from ..common import SummaryBase
import UIResponder


class UIViewControllerSyntheticProvider(UIResponder.UIResponderSyntheticProvider):
    """
    Class representing UIViewController.
    """
    def __init__(self, value_obj, internal_dict):
        super(UIViewControllerSyntheticProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "UIViewController"

        self.register_child_value("title", ivar_name="_title",
                                  primitive_value_function=SummaryBase.get_summary_value,
                                  summary_function=self.get_title_summary)
        self.register_child_value("nib_name", ivar_name="_nibName",
                                  primitive_value_function=SummaryBase.get_summary_value,
                                  summary_function=self.get_nib_name_summary)
        self.register_child_value("child_view_controllers", ivar_name="_childViewControllers",
                                  primitive_value_function=SummaryBase.get_count_value,
                                  summary_function=self.get_child_view_controllers_summary)

    @staticmethod
    def get_title_summary(value):
        return "title={}".format(value)

    @staticmethod
    def get_nib_name_summary(value):
        return "nibName={}".format(value)

    @staticmethod
    def get_child_view_controllers_summary(value):
        return "viewControllers={}".format(value)

    def summaries_parts(self):
        return [self.title_summary]


def summary_provider(value_obj, internal_dict):
    return helpers.generic_summary_provider(value_obj, internal_dict, UIViewControllerSyntheticProvider)
