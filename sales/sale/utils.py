import uuid
from customers.models import Customer
from profiles.models import Profile


def generate_code() :
    code = str(uuid.uuid4()).replace('-', '')[:12]
    return code


def get_salesman_from_id(id):
    salesman = Profile.objects.get(id=id)
    return salesman


def get_customer_from_id(id):
    customer = Customer.objects.get(id=id)
    return customer