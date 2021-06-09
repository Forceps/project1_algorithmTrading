import torch
from AI.pymon import PyMon
import torch.multiprocessing as mp


def train_one_net(network_g, device, actor_name: str):
    db_from = "selected_by_code" + actor_name[-1]
    network_local = PyMon(network_global=network_g, name=actor_name, device=device, target_database_name=db_from)
    network_local.simulationInit(startDate=20190515)

    while network_local.mySituation[1] < network_local.today:
        network_local.simulation_at_one_point(learning=True)


if __name__ == "__main__":
    actors = ["학생1", "학생2", "학생3"]
    device = torch.device("cpu")

    network_global = PyMon(device=device)
    network_global.network.share_memory()

    mp.set_start_method("spawn")
    print("MP start method:", mp.get_start_method())

    processes = []
    for name in actors:
        p = mp.Process(target=train_one_net, args=(network_global.network, device, name,))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()

