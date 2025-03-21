from typing import Dict
from source import domain_object as do

class InputData:
    def __init__(
            self,
            data_path
    ):
        self.data_path = data_path
        self._init_vehicles_and_customers()

    def _init_vehicles_and_customers(self):
        with open(self.data_path) as f:
            content = f.read()

        sections = {}
        current_section = None
        for line in content.split('\n'):
            line = line.strip()
            if not line:
                continue
            if line == "VEHICLE":
                current_section = "VEHICLE"
                sections[current_section] = []
            elif line == "CUSTOMER":
                current_section = "CUSTOMER"
                sections[current_section] = []
            elif current_section:
                sections[current_section].append(line)

        # 处理车辆信息
        vehicle_header = sections["VEHICLE"][0].split()
        vehicle_data = sections["VEHICLE"][1].split()
        num_vehicles = int(vehicle_data[0])
        capacity = int(vehicle_data[1])

        self.vehicle_type = do.VehicleType(
            number=num_vehicles,
            capacity=capacity
        )

        # 处理客户信息
        customers = dict()
        for line in sections["CUSTOMER"][1:]:  # 跳过标题行
            parts = list(filter(None, line.split()))
            if len(parts) < 7:
                continue
            customer = do.Customer(
                cust_id=str(int(parts[0]) + 1),
                x_cord=int(parts[1]),
                y_cord=int(parts[2]),
                demand=float(parts[3]),
                ready_time=float(parts[4]),
                due_date=float(parts[5]),
                service_time=float(parts[6]),
                is_depot=False if int(parts[0]) > 0 else True
            )
            customers[customer.cust_id] = customer
        self.customer_dict = customers
