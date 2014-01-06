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

import lldb

Architecture_unknown = 0
Architecture_armv7 = 1
Architecture_armv7s = 1
Architecture_arm64 = 2
Architecture_i386 = 3
Architecture_x86_64 = 4


class SummaryBase_SynthProvider(object):
    # SummaryBase:

    def __init__(self, value_obj, sys_params, internal_dict):
        # self.as_super = super(SummaryBase_SynthProvider, self)
        # self.as_super.__init__()
        super(SummaryBase_SynthProvider, self).__init__()

        self.value_obj = value_obj
        self.sys_params = sys_params
        self.internal_dict = internal_dict
        self.architecture = Architecture_unknown
        self.arch_offset = 0
        self.get_architecture()
        self.update()

    def update(self):
        self.adjust_for_architecture()

    def adjust_for_architecture(self):
        pass

    def get_architecture(self):
        triple = self.value_obj.GetTarget().GetTriple()

        self.architecture = Architecture_unknown
        if triple.startswith("i386"):
            self.architecture = Architecture_i386
        elif triple.startswith("x86_64"):
            self.architecture = Architecture_x86_64
        elif triple.startswith("armv7"):
            self.architecture = Architecture_armv7
        elif triple.startswith("armv7s"):
            self.architecture = Architecture_armv7s
        elif triple.startswith("arm64"):
            self.architecture = Architecture_arm64

        return self.architecture

    def summary(self):
        return None
