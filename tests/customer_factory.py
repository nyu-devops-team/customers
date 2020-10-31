"""
Test Factory to make fake objects for testing
"""
import factory
from factory.fuzzy import FuzzyChoice
from service.models import Customer


class CustomerFactory(factory.Factory):
    """ Creates fake pets that you don't have to feed """

    class Meta:
        model = Customer

    id = factory.Sequence(lambda n: n)
    first_name = FuzzyChoice(choices=["LeBron", "Kobe", "Steve"])
    last_name = FuzzyChoice(choices=["James", "Bryant", "Nash"])
    email = FuzzyChoice(
        choices=["lbj23@gmail.com", "kb24@gmail.com", "sn10@hotmail.com"]
    )
    address = FuzzyChoice(choices=["23 lbj avenue", "24 kobedrive", "10 steve avenue"])
    active = FuzzyChoice(choices=[1, 0, 1])
    # category = FuzzyChoice(choices=["dog", "cat", "bird", "fish"])
    # available = FuzzyChoice(choices=[True, False])


if __name__ == "__main__":
    for _ in range(10):
        customer = CustomerFactory()
        print(customer.serialize())
