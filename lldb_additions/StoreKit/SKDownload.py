#! /usr/bin/env python
# -*- coding: utf-8 -*-

# The MIT License (MIT)
#
# Copyright (c) 2013 Bartosz Janda
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
from ..Foundation import NSObject

SKDownloadStateWaiting = 0
SKDownloadStateActive = 1
SKDownloadStatePaused = 2
SKDownloadStateFinished = 3
SKDownloadStateFailed = 4
SKDownloadStateCancelled = 5


class SKDownloadSyntheticProvider(NSObject.NSObjectSyntheticProvider):
    """
    Class representing SKDownload.
    """
    def __init__(self, value_obj, internal_dict):
        super(SKDownloadSyntheticProvider, self).__init__(value_obj, internal_dict)
        self.module_name = "StoreKit"
        self.type_name = "SKDownload"

        self.register_child_value("content_identifier", ivar_name="_contentIdentifier",
                                  primitive_value_function=SummaryBase.get_summary_value,
                                  summary_function=self.get_content_identifier_summary)
        self.register_child_value("content_length", ivar_name="_contentLength",
                                  primitive_value_function=SummaryBase.get_signed_value,
                                  summary_function=self.get_content_length_summary)
        self.register_child_value("content_url", ivar_name="_contentURL",
                                  primitive_value_function=SummaryBase.get_summary_value,
                                  summary_function=self.get_content_url_summary)
        self.register_child_value("download_id", ivar_name="_downloadID",
                                  primitive_value_function=SummaryBase.get_summary_value,
                                  summary_function=self.get_download_id_summary)
        self.register_child_value("download_state", ivar_name="_downloadState",
                                  primitive_value_function=SummaryBase.get_signed_value,
                                  summary_function=self.get_download_state_summary)
        self.register_child_value("progress", ivar_name="_progress",
                                  primitive_value_function=SummaryBase.get_float_value,
                                  summary_function=self.get_progress_summary)
        self.register_child_value("time_remaining", ivar_name="_timeRemaining",
                                  primitive_value_function=SummaryBase.get_float_value,
                                  summary_function=self.get_time_remaining_summary)
        self.register_child_value("version", ivar_name="_version",
                                  primitive_value_function=SummaryBase.get_summary_value,
                                  summary_function=self.get_version_summary)

    @staticmethod
    def get_content_identifier_summary(value):
        return "{}".format(value)

    @staticmethod
    def get_content_length_summary(value):
        return "length={}".format(value)

    @staticmethod
    def get_content_url_summary(value):
        return "url={}".format(value)

    @staticmethod
    def get_download_id_summary(value):
        return "downloadID={}".format(value)

    @staticmethod
    def get_download_state_summary(value):
        name = "Unknown"
        if value == SKDownloadStateWaiting:
            name = "Waiting"
        elif value == SKDownloadStateActive:
            name = "Active"
        elif value == SKDownloadStatePaused:
            name = "Paused"
        elif value == SKDownloadStateFinished:
            name = "Finished"
        elif value == SKDownloadStateFailed:
            name = "Failed"
        elif value == SKDownloadStateCancelled:
            name = "Cancelled"

        return "state={}".format(name)

    @staticmethod
    def get_progress_summary(value):
        return "progress={}".format(SummaryBase.formatted_float(value))

    @staticmethod
    def get_time_remaining_summary(value):
        return "timeRemaining={}".format(SummaryBase.formatted_float(value))

    @staticmethod
    def get_version_summary(value):
        return "version={}".format(value)

    def summaries_parts(self):
        return [self.content_identifier_summary, self.content_length_summary]


def summary_provider(value_obj, internal_dict):
    return helpers.generic_summary_provider(value_obj, internal_dict, SKDownloadSyntheticProvider)
