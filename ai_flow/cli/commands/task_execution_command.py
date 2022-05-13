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
"""task-execution command"""
from typing import List

from ai_flow.model.task_execution import TaskExecution
from ai_flow.model.workflow import Workflow


def run_task_execution(args):
    task_execution = TaskExecution(workflow_execution_id=args.workflow_execution_id,
                                   task_name=args.task_name,
                                   sequence_number=args.seq_num,
                                   execution_type=args.execution_type)
    task_execution.run()
