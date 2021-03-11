import atexit

from bson import json_util
from pymongo import MongoClient, monitoring


class CommandLogger(monitoring.CommandListener):

    def started(self, event):
        print(f"{event.command_name} started with lsid {event.command.get('lsid')}")

    def succeeded(self, event):
        print(f"{event.command_name} succeeded")

    def failed(self, event):
        print(f"{event.command_name} failed")


monitoring.register(CommandLogger())

client = MongoClient("mongodb+srv://lambdauser:lambdauser@cluster0.t9dg0.mongodb.net/admin")
atexit.register(client.close)

def lambda_handler(event, lambda_context):
    return json_util.dumps(client.db.command('isMaster'))
