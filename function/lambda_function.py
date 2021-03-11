from bson import json_util
from pymongo import MongoClient, monitoring


class CommandLogger(monitoring.CommandListener):
    def __init__(self):
        self.lsids = set()

    def started(self, event):
        if 'lsid' in event.command:
            lsid_hex = event.command.get('lsid')['id'].as_uuid().hex
            # TODO: Modify MongoClient so it has a private API for reliably
            # tracking all server sessions.
            self._update_sessions(lsid_hex)
            print(f"{event.command_name} started with lsid {lsid_hex}")
        else:
            print(f"{event.command_name} started with no lsid")

    def succeeded(self, event):
        print(f"{event.command_name} succeeded")

    def failed(self, event):
        print(f"{event.command_name} failed")

    def _update_sessions(self, lsid_hex):
        self.lsids.add(lsid_hex)
        # Extensions and lambda functions share the same /tmp.
        with open('/tmp/lsids.txt', 'w') as f:
            f.write('\n'.join(self.lsids))


monitoring.register(CommandLogger())

client = MongoClient(
    "mongodb+srv://lambdauser:lambdauser@cluster0.t9dg0.mongodb.net/admin")


def lambda_handler(event, lambda_context):
    return json_util.dumps(client.db.command('isMaster'))
