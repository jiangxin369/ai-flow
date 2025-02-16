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
import os
import unittest
import notification_service.settings
from notification_service.storage.alchemy import ClientModel

from sqlalchemy import create_engine

from notification_service.cli import cli_parser
from notification_service.cli.commands import db_command
from notification_service.settings import get_configuration
from notification_service.util import db


class TestCliDb(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = cli_parser.get_parser()
        cls.config_str = """
                    server_port: 50052
                    # uri of database backend for notification server
                    db_uri: sqlite:///ns.db
                    # High availability is disabled by default
                    enable_ha: false
                    # TTL of the heartbeat of a server, i.e., if the server hasn't send heartbeat for the TTL time, it is down.
                    ha_ttl_ms: 10000
                    # Hostname and port the server will advertise to clients when HA enabled. If not set, it will use the local ip and configured port.
                    advertised_uri: 127.0.0.1:50052
                """
        cls.tmp_config_file = os.path.join(os.path.dirname(__file__), 'notification_server.yaml')
        with open(cls.tmp_config_file, 'w') as f:
            f.write(cls.config_str)
        notification_service.settings.NOTIFICATION_HOME = os.path.dirname(__file__)
        cls.config = get_configuration()

    @classmethod
    def tearDownClass(cls) -> None:
        if os.path.exists(cls.tmp_config_file):
            os.remove(cls.tmp_config_file)

    def _remove_db_file(self):
        if os.path.exists('ns.db'):
            os.remove('ns.db')

    def setUp(self) -> None:
        self._remove_db_file()
        db.SQL_ALCHEMY_CONN = self.config.db_uri

    def tearDown(self) -> None:
        self._remove_db_file()
        db.clear_engine_and_session()

    def test_cli_db_init(self):
        db_command.init(self.parser.parse_args(['db', 'init']))
        engine = create_engine(self.config.db_uri)
        self.assertTrue('event_model' in engine.table_names())
        self.assertTrue('member_model' in engine.table_names())
        self.assertTrue('notification_client' in engine.table_names())

    def test_cli_db_reset(self):
        db_command.init(self.parser.parse_args(['db', 'init']))
        db.prepare_db()
        with db.create_session() as session:
            client = ClientModel()
            client.namespace = 'a'
            client.sender = 'a'
            client.create_time = 1
            session.add(client)
            session.commit()
            client_res = session.query(ClientModel).all()
            self.assertEqual(1, len(client_res))
            db_command.reset(self.parser.parse_args(['db', 'reset', '-y']))
            client_res = session.query(ClientModel).all()
            self.assertEqual(0, len(client_res))

    def test_cli_db_upgrade(self):
        db_command.upgrade(self.parser.parse_args(['db', 'upgrade', '--version', '87cb292bcc31']))
        engine = create_engine(self.config.db_uri)
        self.assertTrue('event_model' in engine.table_names())
        self.assertTrue('notification_client' in engine.table_names())
        self.assertFalse('member_model' in engine.table_names())

    def test_cli_db_downgrade(self):
        db_command.init(self.parser.parse_args(['db', 'init']))
        db_command.downgrade(self.parser.parse_args(['db', 'downgrade', '--version', '87cb292bcc31']))
        engine = create_engine(self.config.db_uri)
        self.assertTrue('event_model' in engine.table_names())
        self.assertTrue('notification_client' in engine.table_names())
        self.assertFalse('member_model' in engine.table_names())


if __name__ == '__main__':
    unittest.main()
