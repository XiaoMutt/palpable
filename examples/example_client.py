from examples.config import *
from src.palpable.units.client import Client


class ExampleClient(Client):
    def __init__(self):
        super(ExampleClient, self).__init__(
            address=SERVER_ADDRESS,
            family=SERVER_FAMILY,
            authkey=SECRET
        )
