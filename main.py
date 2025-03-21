import os
import pandas as pd
from pyvrp import Model, read
from pyvrp.stop import MaxRuntime, NoImprovement, MultipleCriteria
from source import functions

# 配置参数

TIME_LIMITS = [60, 300, 600, 1800]  # 1,5,10,30 分钟（单位：秒）


if __name__ == "__main__":
    working_dir = './nvida_instance/'

    functions.convert_all_txt_to_vrp(working_dir=working_dir)

    results = []
    for file in os.listdir(working_dir):
        if not file.endswith(".vrp"):
            continue
        instance_name = file
        temp_file = os.path.join(working_dir, file)

        try:
            # 读取实例数据
            instance = read(temp_file)

            # 创建模型
            model = Model.from_data(instance)

            for time_limit in TIME_LIMITS:
                try:
                    # 关键配置：停止条件 = 最大运行时间 + 无改进迭代次数
                    stop_conditions = MultipleCriteria([
                        MaxRuntime(time_limit),  # 时间限制（秒）
                        NoImprovement(5000),  # 5000次迭代无改进后停止
                    ])

                    # 运行求解器
                    result = model.solve(stop=stop_conditions, display=True)
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

        except Exception as e:
            print(f"加载实例 {instance_name} 失败: {str(e)}")
            continue

    # 生成 Excel
    df = pd.DataFrame(results)
    df.to_excel("vrptw_test_results.xlsx", index=False)
    print("结果已保存到 vrptw_test_results.xlsx")