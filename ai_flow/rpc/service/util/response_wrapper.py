#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
from enum import Enum
from functools import wraps
from typing import List

from google.protobuf.json_format import MessageToJson

from ai_flow.common.exception.exceptions import AIFlowException
from ai_flow.common.result import BaseResult, RetCode
from ai_flow.rpc.protobuf.message_pb2 import Response, SUCCESS, ReturnCode, RESOURCE_DOES_NOT_EXIST, NamespaceProto, \
    INTERNAL_ERROR, WorkflowProto, WorkflowSnapshotProto
from ai_flow.rpc.protobuf.metadata_service_pb2 import NamespaceListProto, WorkflowSnapshotListProto
from ai_flow.rpc.protobuf.scheduler_service_pb2 import WorkflowListProto


def catch_exception(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AIFlowException as e:
            return Response(return_code=str(e.error_code), error_msg=e.error_msg)

    return wrapper


def wrap_data_response(data):
    if data is not None:
        return Response(return_code=str(SUCCESS), error_msg=None,
                        data=MessageToJson(data, preserving_proto_field_name=True))
    else:
        return Response(return_code=str(RESOURCE_DOES_NOT_EXIST),
                        error_msg=ReturnCode.Name(RESOURCE_DOES_NOT_EXIST).lower(),
                        data=None)


def wrap_result_response(result: BaseResult):
    if result.status == RetCode.OK:
        return Response(return_code=str(SUCCESS), error_msg=None, data=result.message)
    else:
        return Response(return_code=str(INTERNAL_ERROR), error_msg=result.message,
                        data=None)


def wrap_namespace_list_response(namespace_list: List[NamespaceProto]):
    if namespace_list is None or len(namespace_list) == 0:
        return Response(return_code=str(RESOURCE_DOES_NOT_EXIST),
                        error_msg=ReturnCode.Name(RESOURCE_DOES_NOT_EXIST).lower(),
                        data=None)
    else:
        list_proto = NamespaceListProto(namespaces=namespace_list)
        return Response(return_code=str(SUCCESS),
                        error_msg=None,
                        data=MessageToJson(list_proto, preserving_proto_field_name=True))


def wrap_workflow_list_response(workflow_list: List[WorkflowProto]):
    if workflow_list is None or len(workflow_list) == 0:
        return Response(return_code=str(RESOURCE_DOES_NOT_EXIST),
                        error_msg=ReturnCode.Name(RESOURCE_DOES_NOT_EXIST).lower(),
                        data=None)
    else:
        list_proto = WorkflowListProto(workflows=workflow_list)
        return Response(return_code=str(SUCCESS),
                        error_msg=None,
                        data=MessageToJson(list_proto, preserving_proto_field_name=True))


def wrap_workflow_snapshot_list_response(workflow_snapshot_list: List[WorkflowSnapshotProto]):
    if workflow_snapshot_list is None or len(workflow_snapshot_list) == 0:
        return Response(return_code=str(RESOURCE_DOES_NOT_EXIST),
                        error_msg=ReturnCode.Name(RESOURCE_DOES_NOT_EXIST).lower(),
                        data=None)
    else:
        list_proto = WorkflowSnapshotListProto(workflow_snapshots=workflow_snapshot_list)
        return Response(return_code=str(SUCCESS),
                        error_msg=None,
                        data=MessageToJson(list_proto, preserving_proto_field_name=True))




