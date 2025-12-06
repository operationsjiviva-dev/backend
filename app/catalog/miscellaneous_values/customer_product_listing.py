class ProductSortByOptions:
    PRICE_LOW_TO_HIGH = "PRICE_LOW_TO_HIGH"
    PRICE_HIGH_TO_LOW = "PRICE_HIGH_TO_LOW"

    @classmethod
    def values(cls):
        return [cls.PRICE_LOW_TO_HIGH, cls.PRICE_HIGH_TO_LOW]
