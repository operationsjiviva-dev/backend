class CartPaymentPreference:
    CASH = 'CASH'
    ONLINE = 'ONLINE'

    @classmethod
    def values(cls):
        return [cls.CASH, cls.ONLINE]


class CartStatus:
    OPEN = 'OPEN'
    CLOSED = 'CLOSED'
    DISCARDED = 'DISCARDED'

    @classmethod
    def values(cls):
        return [cls.OPEN, cls.CLOSED]