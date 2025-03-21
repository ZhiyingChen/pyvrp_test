import os
import pandas as pd
from pyvrp import Model, read
from pyvrp.stop import MaxRuntime, NoImprovement, MultipleCriteria
from source.input_data import InputData
from source.model import VRPModel

# 配置参数

TIME_LIMITS = [60, 300]  # 1,5,10,30 分钟（单位：秒）


if __name__ == "__main__":
    input_path = './nvida_instance/C1_10_7.TXT'

    input_data = InputData(input_path)
    vrp_model = VRPModel(input_data)
    vrp_model.solve()
