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
import logging

from google.protobuf.json_format import Parse
from ai_flow.common.exception.exceptions import AIFlowException
from ai_flow.rpc.client.util.proto_to_meta import ProtoToMeta
from ai_flow.rpc.protobuf.message_pb2 import SUCCESS, NamespaceProto, RESOURCE_DOES_NOT_EXIST, INTERNAL_ERROR, \
    WorkflowProto, WorkflowSnapshotProto
from ai_flow.rpc.protobuf.metadata_service_pb2 import NamespaceListProto, WorkflowSnapshotListProto
from ai_flow.rpc.protobuf.scheduler_service_pb2 import WorkflowListProto

logger = logging.getLogger(__name__)


def unwrap_bool_response(response):
    if response.return_code == str(SUCCESS):
        return True
    elif response.return_code == str(INTERNAL_ERROR):
        logger.warning(response.error_msg)
        return False
    else:
        raise AIFlowException(response.error_msg)


def unwrap_string_response(response):
    if response.return_code == str(SUCCESS):
        return response.data
    else:
        raise AIFlowException(response.error_msg)


def unwrap_namespace_response(response):
    if response.return_code == str(SUCCESS):
        return ProtoToMeta.proto_to_namespace_meta(Parse(response.data, NamespaceProto()))
    elif response.return_code == str(RESOURCE_DOES_NOT_EXIST):
        return None
    else:
        raise AIFlowException(response.error_msg)


def unwrap_namespace_list_response(response):
    if response.return_code == str(SUCCESS):
        namespace_list_proto = Parse(response.data, NamespaceListProto())
        return ProtoToMeta.proto_to_namespace_meta_list(namespace_list_proto.namespaces)
    elif response.return_code == str(RESOURCE_DOES_NOT_EXIST):
        return None
    else:
        raise AIFlowException(response.error_msg)


def unwrap_workflow_response(response):
    if response.return_code == str(SUCCESS):
        return ProtoToMeta.proto_to_workflow_meta(Parse(response.data, WorkflowProto()))
    elif response.return_code == str(RESOURCE_DOES_NOT_EXIST):
        return None
    else:
        raise AIFlowException(response.error_msg)


def unwrap_workflow_list_response(response):
    if response.return_code == str(SUCCESS):
        workflow_list_proto = Parse(response.data, WorkflowListProto())
        return ProtoToMeta.proto_to_workflow_meta_list(workflow_list_proto.workflows)
    elif response.return_code == str(RESOURCE_DOES_NOT_EXIST):
        return None
    else:
        raise AIFlowException(response.error_msg)


def unwrap_workflow_snapshot_response(response):
    if response.return_code == str(SUCCESS):
        return ProtoToMeta.proto_to_workflow_snapshot_meta(Parse(response.data, WorkflowSnapshotProto()))
    elif response.return_code == str(RESOURCE_DOES_NOT_EXIST):
        return None
    else:
        raise AIFlowException(response.error_msg)


def unwrap_workflow_snapshot_list_response(response):
    if response.return_code == str(SUCCESS):
        snapshot_list_proto = Parse(response.data, WorkflowSnapshotListProto())
        return ProtoToMeta.proto_to_workflow_snapshot_meta_list(snapshot_list_proto.workflow_snapshots)
    elif response.return_code == str(RESOURCE_DOES_NOT_EXIST):
        return None
    else:
        raise AIFlowException(response.error_msg)

