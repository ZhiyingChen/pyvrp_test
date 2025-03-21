import os
import pandas as pd
from pyvrp import Model, read
from pyvrp.stop import MaxRuntime, NoImprovement, MultipleCriteria
from source.input_data import InputData
from source.model import VRPModel

# 配置参数

TIME_LIMITS = [60, 300, 600, 1800]  # 1,5,10,30 分钟（单位：秒）


if __name__ == "__main__":
    working_dir = './nvida_instance/'

    results = []
    for file in os.listdir(working_dir):
        if not file.endswith(".TXT"):
            continue
        # 读取实例数据
        input_path = os.path.join(working_dir, file)
        instance_name = file.replace(".TXT", "")
        for time_limit in TIME_LIMITS:
            try:
                # 关键配置：停止条件 = 最大运行时间 + 无改进迭代次数
                stop_conditions = MultipleCriteria([
                    MaxRuntime(time_limit),  # 时间限制（秒）
                    NoImprovement(5000),  # 5000次迭代无改进后停止
                ])

                input_data = InputData(input_path)
                vrp_model = VRPModel(input_data)
                vrp_model.solve(stop=stop_conditions)

                result = vrp_model.res

                vehicles = result.best.num_routes()
                cost = result.cost()
                clients = result.best.num_clients()
                duration = result.best.duration()

            except Exception as e:
                vehicles = cost = clients = duration = "N/A"
                print(f"求解失败: {instance_name} (Time={time_limit}s) - {str(e)}")

            results.append({
                "Instance": instance_name.replace(".vrp", ""),
                "Vehicles": vehicles,
                "Timelimits": f"{time_limit // 60}分钟",
                "Distance": cost,
                "Clients": clients,
                "Duration": duration,
            })

    # 生成 Excel
    df = pd.DataFrame(results)
    df.to_excel("vrptw_test_results.xlsx", index=False)
    print("结果已保存到 vrptw_test_results.xlsx")
