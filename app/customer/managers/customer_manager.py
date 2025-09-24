from customer.models import Customer
from customer.managers.otp_manager import OTPManager


class CustomerManager:
    def __init__(self):
        pass

    @classmethod
    def update(cls, customer_id: str, **kwargs):
        customer = Customer.objects.filter(id=customer_id).first()
        if customer:
            if kwargs.get('name'):
                customer.name = kwargs.get('name')
            if kwargs.get('gender'):
                customer.gender = kwargs.get('gender').upper()
            
            customer.save()
        return customer
    
    @classmethod
    def create(cls, phone_number: str, name: str = None, gender: str = None):
        customer = Customer.objects.filter(phone_number=phone_number).first()
        if not customer:
            customer = Customer()
            customer.phone_number = phone_number
            if name:
                customer.name = name
            if gender:
                customer.gender = gender
            customer.save()
        return customer

    @classmethod
    def send_otp(cls, phone_number: str, name: str = None, gender: str = None):
        existing_customer = Customer.objects.filter(phone_number=phone_number).first()
        if existing_customer and (name or gender):
            customer = cls.update(existing_customer.id, name=name, gender=gender)
        else:
            customer = cls.create(phone_number, name=name, gender=gender)

        otp_manager = OTPManager()
        otp_manager.send_otp(phone_number)

        return customer
    
    @classmethod
    def get_customer_using_phone_number(cls, phone_number: str):
        return Customer.objects.filter(phone_number=phone_number).first()
    
    @classmethod
    def get_single_customer_data(cls, customer: Customer):
        customer_data = {
            "customerId": str(customer.id),
            "name": customer.name,
            "email": customer.email if customer.email else "",
            "lastName": customer.last_name if customer.last_name else "",
            "address": customer.address if customer.address else "",
            "phoneNumber": customer.phone_number if customer.phone_number else "",
            "gender": customer.gender if customer.gender else "",
        }
        return customer_data
        







