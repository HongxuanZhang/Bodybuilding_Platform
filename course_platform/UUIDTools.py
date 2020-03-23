import uuid


class UUIDTools(object):
    """uuid function tools"""

    @staticmethod
    def uuid1_hex():
        return uuid.uuid1().hex
