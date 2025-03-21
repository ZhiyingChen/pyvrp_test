class Customer:
    def __init__(
            self,
            cust_id: str,
            is_depot: bool,
            x_cord: int,
            y_cord: int,
            demand: int,
            ready_time: int,
            due_date: int,
            service_time: int
    ):
        self.cust_id = cust_id
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.demand = demand
        self.ready_time = ready_time
        self.due_date = due_date
        self.service_time = service_time
        self.is_depot = is_depot

    def __str__(self):
        return f"Customer {self.cust_id} at ({self.x_cord}, {self.y_cord})"
