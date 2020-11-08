from seatable_api import SeaTableAPI
from seatable_api.constants import UPDATE_DTABLE, NEW_NOTIFICATION
from seatable_api.utils import convert_row

server_url = 'https://cloud.seatable.cn'
api_token = 'd00ad238bb6050b32aa8b2fa95e5f7b3ca79b1e6'


def on_update_seatable(data, index, *args):
    """ You can overwrite this event
    """
    row = convert_row(metadata, data)
    print(row)


def on_new_notification(data, index, *args):
    """ You can overwrite this event
    """
    print(data)


def connect_socket_io():

    seatable_api = SeaTableAPI(api_token, server_url)
    seatable_api.auth(with_socket_io=True)

    global metadata
    metadata = seatable_api.get_metadata()

    # overwrite events
    seatable_api.socketIO.on(UPDATE_DTABLE, on_update_seatable)
    seatable_api.socketIO.on(NEW_NOTIFICATION, on_new_notification)

    seatable_api.socketIO.wait()  # forever or limit (seconds=10)


if __name__ == '__main__':
    connect_socket_io()
