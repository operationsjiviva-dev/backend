class CartDoesNotExist(Exception):
    def __init__(self):
        message = "Some issue with your cart, Please refresh the page"
        super().__init__(message)


class CartIsEmpty(Exception):
    def __init__(self):
        message = "Cart is empty"
        super().__init__(message)


class CartDeliveryAdrressNotSet(Exception):
    def __init__(self):
        message = "Delivery address not set"
        super().__init__(message)


class PaymentPreferenceNotSet(Exception):
    def __init__(self):
        message = "Payment preference not set"
        super().__init__(message)


class OrderDoesNotExist(Exception):
    def __init__(self):
        message = "Order does not exist"
        super().__init__(message)

