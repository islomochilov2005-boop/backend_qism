import hashlib

class ClickXizmati:
    @staticmethod
    def imzo_yaratish(text):
        return hashlib.md5(text.encode('utf-8')).hexdigest()