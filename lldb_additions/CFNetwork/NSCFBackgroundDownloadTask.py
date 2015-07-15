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

from .. import helpers
from ..common import SummaryBase
import NSCFBackgroundSessionTask


class NSCFBackgroundDownloadTaskSyntheticProvider(NSCFBackgroundSessionTask.NSCFBackgroundSessionTaskSyntheticProvider):
    """
    Class representing __NSCFBackgroundDownloadTask.
    """
    def __init__(self, value_obj, internal_dict):
        super(NSCFBackgroundDownloadTaskSyntheticProvider, self).__init__(value_obj, internal_dict)
        self.module_name = "CFNetwork"
        self.type_name = "__NSCFBackgroundDownloadTask"

        self.register_child_value("finished", ivar_name="_finished",
                                  primitive_value_function=SummaryBase.get_bool_value,
                                  summary_function=self.get_finished_summary)

    @staticmethod
    def get_finished_summary(value):
        if value:
            return "finished"
        return None


def summary_provider(value_obj, internal_dict):
    return helpers.generic_summary_provider(value_obj, internal_dict, NSCFBackgroundDownloadTaskSyntheticProvider)
