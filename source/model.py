from pyvrp import Model
from pyvrp.stop import MultipleCriteria, NoImprovement, MaxRuntime
import numpy as np
from .input_data import InputData


class VRPModel:
    def __init__(
            self,
            input_data: InputData
    ):
        self.input_data = input_data
        self.m = Model()
        self._init_depot()
        self._init_customers()
        self._init_vehicles()
        self._init_edges()
        self.data = self.m.data()
        self.zone = self.input_data.data_path.split("/")[-1]
        self.res = None

    def _init_depot(self):
        self.depot_dict = {
            customer.cust_id:
            self.m.add_depot(
                x=customer.x_cord,
                y=customer.y_cord,
                name=customer.cust_id
            )
            for _, customer in self.input_data.customer_dict.items()
            if customer.is_depot
        }

    def _init_customers(self):
        self.customer_dict = {
            customer.cust_id:
            self.m.add_client(
                x=customer.x_cord,
                y=customer.y_cord,
                name=customer.cust_id,
                tw_early=customer.ready_time,
                tw_late=customer.due_date,
                delivery=[customer.demand, 1],
                service_duration=customer.service_time
            )
            for _, customer in self.input_data.customer_dict.items()
            if not customer.is_depot
        }

    def _init_vehicles(self):
        self.vehicle_type = self.m.add_vehicle_type(
            capacity=[self.input_data.vehicle_type.capacity, len(self.m.locations)],
            num_available=self.input_data.vehicle_type.number,
        )

    def _init_edges(self):
        for frm in self.m.locations:
            for to in self.m.locations:
                frm_node = self.input_data.customer_dict[frm.name]
                to_node = self.input_data.customer_dict[to.name]
                distance = np.sqrt(
                    (frm_node.x_cord - to_node.x_cord) ** 2
                    + (frm_node.y_cord - to_node.y_cord) ** 2
                )

                self.m.add_edge(
                    frm,
                    to,
                    distance=distance,
                    duration=to_node.service_time if frm.name != to.name else 0,
                )


    def solve(self, stop):

        self.res = self.m.solve(stop=stop, display=True)