
class VehicleType:
    def __init__(
            self,
            capacity: int,
            number: int
    ):
        self.capacity = capacity
        self.number = number

    def __str__(self):
        return f"VehicleType(capacity={self.capacity}, number={self.number})"