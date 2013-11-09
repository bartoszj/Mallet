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

import lldb


def SKProduct_SummaryProvider(valobj, dict):
    stream = lldb.SBStream()
    valobj.GetExpressionPath(stream)

    # productIdentifier
    #product_identifier = valobj.CreateValueFromExpression("productIdentifier",
    #                                                      "(NSString *)[" + stream.GetData() +
    #                                                      " productIdentifier]")
    #product_identifier_value = product_identifier.GetObjectDescription()
    #product_identifier_summary = product_identifier_value

    # localizedTitle
    localized_title = valobj.CreateValueFromExpression("localizedTitle",
                                                       "(NSString *)[" + stream.GetData() +
                                                       " localizedTitle]")
    localized_title_value = localized_title.GetObjectDescription()
    localized_title_summary = "@\"{}\"".format(localized_title_value)

    # localizedDescription
    #localized_description = valobj.CreateValueFromExpression("localizedDescription",
    #                                                         "(NSString *)[" + stream.GetData() +
    #                                                         " localizedDescription]")
    #localized_description_value = localized_description.GetObjectDescription()
    #localized_description_summary = localized_description_value

    # price
    #price = valobj.CreateValueFromExpression("price",
    #                                         "(NSDecimalNumber *)[" + stream.GetData() +
    #                                         " price]")
    #price_value = price.GetObjectDescription()
    #price_summary = price_value

    # priceLocale
    #price_locale = valobj.CreateValueFromExpression("priceLocale",
    #                                                "(NSLocale *)[" + stream.GetData() +
    #                                                " priceLocale]")
    #price_locale_value = price_locale.GetObjectDescription()
    #price_locale_summary = price_locale_value

    # downloadable
    downloadable = valobj.CreateValueFromExpression("downloadable",
                                                    "(BOOL)[" + stream.GetData() +
                                                    " downloadable]")
    downloadable_value = downloadable.GetValueAsUnsigned()
    downloadable_summary = "downloadable = {}".format("YES" if downloadable_value == 1 else "NO")

    # downloadContentVersion
    download_content_version = valobj.CreateValueFromExpression("downloadContentVersion",
                                                                "(NSString *)[" + stream.GetData() +
                                                                " downloadContentVersion]")
    download_content_version_value = download_content_version.GetObjectDescription()
    download_content_version_summary = "version = @\"{}\"".format(download_content_version_value)

    # Summaries
    summaries = [localized_title_summary]
    if downloadable_value != 0:
        summaries.append(downloadable_summary)
        summaries.append(download_content_version_summary)

    summary = ", ".join(summaries)
    return summary


def __lldb_init_module(debugger, dict):
    debugger.HandleCommand("type summary add -F SKProduct.SKProduct_SummaryProvider \
                            --category StoreKit \
                            SKProduct")
    debugger.HandleCommand("type category enable StoreKit")
