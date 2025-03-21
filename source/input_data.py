from typing import List
import numpy as np

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
                cust_id=parts[0],
                x_cord=int(parts[1]),
                y_cord=int(parts[2]),
                demand=int(parts[3]),
                ready_time=int(parts[4]),
                due_date=int(parts[5]),
                service_time=int(parts[6]),
                is_depot=False if int(parts[0]) > 0 else True
            )
            customers[customer.cust_id] = customer
        self.customer_dict = customers

    def calculate_distance(
            self,
            route_sol_lt: List[List[str]]
    ):
        cost = 0
        for route in route_sol_lt:
            # depot  到第一个点
            depot = self.customer_dict["0"]
            cust_id_1 = route[0]
            cust_1 = self.customer_dict[cust_id_1]
            cost += np.sqrt(
                (depot.x_cord - cust_1.x_cord) ** 2 +
                (depot.y_cord - cust_1.y_cord) ** 2
            )

            # 最后一个点回到depot
            cust_id_2 = route[-1]
            cust_2 = self.customer_dict[cust_id_2]
            cost += np.sqrt(
                (cust_2.x_cord - depot.x_cord) ** 2 +
                (cust_2.y_cord - depot.y_cord) ** 2
            )

            # 中间
            for i in range(len(route) - 1):
                cust_id_1 = route[i]
                cust_id_2 = route[i + 1]
                cust_1 = self.customer_dict[cust_id_1]
                cust_2 = self.customer_dict[cust_id_2]
                dist = np.sqrt(
                    (cust_1.x_cord - cust_2.x_cord) ** 2 +
                    (cust_1.y_cord - cust_2.y_cord) ** 2
                )
                cost += dist

        return cost
