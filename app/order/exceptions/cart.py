class ProductOutOfStock(Exception):
    def __init__(self):
        message = "Product is out of stock"
        super().__init__(message)

class ProductDoesNotExist(Exception):
    def __init__(self):
        message = "Product does not exist"
        super().__init__(message)

class CartProductQuantityLimitExceeded(Exception):
    def __init__(self):
        message = "You have exceeded the product quantity limit"
        super().__init__(message)

class CartDoesNotExist(Exception):
    def __init__(self):
        message = "Some issue with your cart, Please refresh the page"
        super().__init__(message)

class InvalidPaymentPreference(Exception):
    def __init__(self):
        message = "Invalid payment preference"
        super().__init__(message)

