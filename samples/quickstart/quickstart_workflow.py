#
# Copyright 2022 The AI Flow Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
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
import time

from ai_flow.model.action import TaskAction
from ai_flow.notification.notification_client import AIFlowNotificationClient
from ai_flow.operators.bash import BashOperator
from ai_flow.operators.python import PythonOperator

from ai_flow.model.workflow import Workflow

EVENT_KEY = "key"


def func():
    time.sleep(5)
    notification_client = AIFlowNotificationClient("localhost:50052")
    notification_client.send_event(key=EVENT_KEY,
                                   value='This is a custom message.')


with Workflow(name='quickstart_workflow') as w1:
    task1 = BashOperator(name='task1', bash_command='echo I am the 1st task.')
    task2 = BashOperator(name='task2', bash_command='echo I am the 2nd task.')
    task3 = PythonOperator(name='task3', python_callable=func)
    task4 = BashOperator(name='task4', bash_command='echo I am the 4th task.')

    task3.start_after([task1, task2])

    task4.action_on_event_received(action=TaskAction.START, event_key=EVENT_KEY)
