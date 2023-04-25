from apis.raider_io_api import RaiderIoApi


class RaiderIoService:

    @staticmethod
    def get_raider_io_history(name, realm, region):
        val = RaiderIoApi.get_all_io_history(name, realm, region)
        print(val)
