import os

def convert_to_vrp(
        input_path: str,
        output_path: str
):
    with open(input_path) as f:
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
    num_vehicles = vehicle_data[0]
    capacity = vehicle_data[1]

    # 处理客户信息
    customers = []
    for line in sections["CUSTOMER"][1:]:  # 跳过标题行
        parts = list(filter(None, line.split()))
        if len(parts) < 7:
            continue
        customers.append({
            'id': int(parts[0]) + 1,
            'x': parts[1],
            'y': parts[2],
            'demand': parts[3],
            'ready': parts[4],
            'due': parts[5],
            'service': parts[6]
        })

    # 写入.vrp文件
    with open(output_path, 'w') as f:
        f.write(f"NAME: {input_path.split('/')[-1]}\n")
        f.write("TYPE: VRPTW\n")
        f.write(f"DIMENSION: {len(customers) }\n")
        f.write(f"VEHICLES: {num_vehicles}\n")
        f.write(f"CAPACITY: {capacity}\n")
        f.write(f'EDGE_WEIGHT_TYPE : EUC_2D\n')
        f.write(f"NODE_COORD_SECTION\n")
        for cust in customers:
            f.write(f"{cust['id']} {cust['x']} {cust['y']}\n")

        f.write(f"DEMAND_SECTION\n")
        for cust in customers:
            f.write(f"{cust['id']} {cust['demand']}\n")

        f.write(f"TIME_WINDOW_SECTION\n")
        for cust in customers:
            f.write(f"{cust['id']} {cust['ready']} {cust['due']}\n")

        f.write("SERVICE_TIME_SECTION\n")
        for cust in customers:
            f.write(f"{cust['id']} {cust['service']}\n")

        f.write("DEPOT_SECTION\n1\n-1\n")
        f.write("EOF")


def convert_all_txt_to_vrp(
        working_dir: str,
):
    for file in os.listdir(working_dir):
        if file.endswith(".TXT"):
            input_path = os.path.join(working_dir, file)
            output_path = os.path.join(working_dir, file.replace(".TXT", ".vrp"))
            convert_to_vrp(input_path, output_path)