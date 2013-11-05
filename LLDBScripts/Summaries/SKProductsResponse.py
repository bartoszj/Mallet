#! /usr/bin/env python
# -*- coding: utf-8 -*-

import lldb


def SKProductsResponse_SummaryProvider(valobj, dict):
    stream = lldb.SBStream()
    valobj.GetExpressionPath(stream)
    num_valid_products_o = valobj.CreateValueFromExpression("valid_count",
                                        "(NSUInteger)[[" + stream.GetData() + " products] count]")
    num_valid_products = num_valid_products_o.GetValueAsUnsigned()
    num_not_valid_products_o = valobj.CreateValueFromExpression("not_valid_count",
                                        "(NSUInteger)[[" + stream.GetData() + " invalidProductIdentifiers] count]")
    num_not_valid_products = num_not_valid_products_o.GetValueAsUnsigned()

    return "@\"Valid: {}, not valid: {}\"".format(num_valid_products, num_not_valid_products)


def __lldb_init_module(debugger, dict):
    debugger.HandleCommand("type summary add -F SKProductsResponse.SKProductsResponse_SummaryProvider SKProductsResponse")
