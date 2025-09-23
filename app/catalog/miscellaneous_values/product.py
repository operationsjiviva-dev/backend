class ProductSizes:
    XS = "XS"
    S = "S"
    M = "M"
    L = "L"
    XL = "XL"
    XXL = "XXL"
    XXXL = "XXXL"

    CHOICES = [
        (XS, "Extra Small"),
        (S, "Small"),
        (M, "Medium"),
        (L, "Large"),
        (XL, "Extra Large"),
        (XXL, "Double Extra Large"),
        (XXXL, "Triple Extra Large"),
    ]
    ALL_SIZES_ORDER = [XS, S, M, L, XL, XXL, XXXL]


class ProductMetaAtrributes:
    COLLECTION = "COLLECTION"
    CATEGORY = "CATEGORY"
    OCCASION = "OCCASION"
    TAG = "TAG"