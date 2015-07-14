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
from ..Foundation import NSOperationQueue
from ..CFNetwork import NSURLSession
from .. import SummaryBase
import AFSecurityPolicy
import AFNetworkReachabilityManager


class AFURLSessionManagerSyntheticProvider(NSObject.NSObjectSyntheticProvider):
    """
    Class representing AFURLSessionManager.
    """
    def __init__(self, value_obj, internal_dict):
        super(AFURLSessionManagerSyntheticProvider, self).__init__(value_obj, internal_dict)

        self.register_child_value("session", ivar_name="_session",
                                  provider_class=NSURLSession.NSURLSessionSyntheticProvider,
                                  summary_function=self.get_session_summary)
        self.register_child_value("operation_queue", ivar_name="_operationQueue",
                                  provider_class=NSOperationQueue.NSOperationQueueSyntheticProvider,
                                  summary_function=self.get_operation_queue_summary)
        self.register_child_value("mutable_task_delegates_keyed_by_task_identifier", ivar_name="_mutableTaskDelegatesKeyedByTaskIdentifier",
                                  primitive_value_function=SummaryBase.get_count_value,
                                  summary_function=self.get_mutable_task_delegates_keyed_by_task_identifier_summary)
        self.register_child_value("response_serializer", ivar_name="_responseSerializer",
                                  provider_class=AFSecurityPolicy.AFSecurityPolicySyntheticProvider,
                                  summary_function=self.get_response_serializer_summary)
        self.register_child_value("security_policy", ivar_name="_securityPolicy",
                                  provider_class=AFSecurityPolicy.AFSecurityPolicySyntheticProvider,
                                  summary_function=self.get_security_policy_summary)
        self.register_child_value("reachability_manager", ivar_name="_reachabilityManager",
                                  provider_class=AFNetworkReachabilityManager.AFNetworkReachabilityManagerSyntheticProvider,
                                  summary_function=self.get_reachability_manager_summary)
        self.register_child_value("attempts_to_recreate_upload_tasks_for_background_sessions", ivar_name="_attemptsToRecreateUploadTasksForBackgroundSessions",
                                  primitive_value_function=SummaryBase.get_bool_value,
                                  summary_function=self.get_attempts_to_recreate_upload_tasks_for_background_sessions_summary)

    @staticmethod
    def get_session_summary(provider):
        """
        :param NSURLSession.NSURLSessionSyntheticProvider provider: NSURLSession provider.
        """
        return provider.summary()

    @staticmethod
    def get_operation_queue_summary(provider):
        """
        :param NSOperationQueue.NSOperationQueueSyntheticProvider provider: NSOperationQueue provider.
        """
        private = provider.private_provider
        """:type: NSOperationQueueInternal.NSOperationQueueInternalSyntheticProvider"""
        if private is None:
            return None

        summary = SummaryBase.join_summaries(private.suspended_summary,
                                             private.get_operations_count_summary(),
                                             private.executing_operations_count_summary,
                                             private.max_operations_count_summary)
        return summary

    @staticmethod
    def get_mutable_task_delegates_keyed_by_task_identifier_summary(value):
        return "tasks={}".format(value)

    @staticmethod
    def get_response_serializer_summary(provider):
        """
        :param AFSecurityPolicy.AFSecurityPolicySyntheticProvider provider: AFSecurityPolicy provider.
        """
        return provider.summary()

    @staticmethod
    def get_security_policy_summary(provider):
        """
        :param AFSecurityPolicy.AFSecurityPolicySyntheticProvider provider: AFSecurityPolicy provider.
        """
        return provider.summary()

    @staticmethod
    def get_reachability_manager_summary(provider):
        """
        :param AFNetworkReachabilityManager.AFNetworkReachabilityManagerSyntheticProvider provider: AFNetworkReachabilityManager provider.
        """
        return provider.summary()

    @staticmethod
    def get_attempts_to_recreate_upload_tasks_for_background_sessions_summary(value):
        if value:
            return "attemptsToRecreateUploadTasksForBackgroundSessions"
        return None

    def summaries_parts(self):
        return [self.session_summary, self.mutable_task_delegates_keyed_by_task_identifier_summary]


def summary_provider(value_obj, internal_dict):
    return helpers.generic_summary_provider(value_obj, internal_dict, AFURLSessionManagerSyntheticProvider)
