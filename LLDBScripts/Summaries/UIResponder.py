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
import NSObject


class UIResponder_SynthProvider(NSObject.NSObject_SynthProvider):
    # UIResponder:
    # Offset / size (+ alignment)                                           32bit:                  64bit:

    def __init__(self, value_obj, sys_params, internal_dict):
        # self.as_super = super(UIResponder_SynthProvider, self)
        # self.as_super.__init__()
        super(UIResponder_SynthProvider, self).__init__(value_obj, sys_params, internal_dict)
        
    def update(self):
        super(UIResponder_SynthProvider, self).update()
        
    def adjust_for_architecture(self):
        super(UIResponder_SynthProvider, self).adjust_for_architecture()
