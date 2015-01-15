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
from .. import SummaryBase
import UIView
import UILabel


class UITableViewCellSyntheticProvider(UIView.UIViewSyntheticProvider):
    """
    Class representing UITableViewCell.
    """
    def __init__(self, value_obj, internal_dict):
        super(UITableViewCellSyntheticProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "UITableViewCell"

        self.register_child_value("reuse_identifier", ivar_name="_reuseIdentifier",
                                  primitive_value_function=SummaryBase.get_summary_value,
                                  summary_function=self.get_reuse_identifier_summary)
        self.register_child_value("text_label", ivar_name="_textLabel",
                                  provider_class=UILabel.UILabelSyntheticProvider,
                                  summary_function=self.get_text_label_summary)
        self.register_child_value("detail_text_label", ivar_name="_detailTextLabel",
                                  provider_class=UILabel.UILabelSyntheticProvider,
                                  summary_function=self.get_detail_text_label)

    @staticmethod
    def get_reuse_identifier_summary(value):
        return "reuseIdentifier={}".format(value)

    @staticmethod
    def get_text_label_summary(provider):
        """
        Text label summary.

        :param UILabel.UILabelSyntheticProvider provider: UILabel provider
        :return: Text label summary.
        :rtype: str
        """
        value = provider.text_value
        if value is not None:
            return "textLabel={}".format(provider.text_value)
        return None

    @staticmethod
    def get_detail_text_label(provider):
        """
        Detail label summary.

        :param UILabel.UILabelSyntheticProvider provider: UILabel provider
        :return: Detail label summary.
        :rtype: str
        """
        value = provider.text_value
        if value is not None:
            return "detailLabel={}".format(provider.text_value)
        return None

    def summary(self):
        summary = SummaryBase.join_summaries(self.text_label_summary,
                                             self.detail_text_label_summary,
                                             self.reuse_identifier_summary,
                                             self.tag_summary)
        return summary


def summary_provider(value_obj, internal_dict):
    return helpers.generic_summary_provider(value_obj, internal_dict, UITableViewCellSyntheticProvider)


def lldb_init(debugger, dictionary):
    debugger.HandleCommand("type summary add -F {}.summary_provider \
                            --category UIKit \
                            UITableViewCell".format(__name__))
    debugger.HandleCommand("type category enable UIKit")
