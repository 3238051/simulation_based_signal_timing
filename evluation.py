# -*- coding: utf-8 -*-

# @Author: KeyangZhang
# @Email: 3238051@qq.com
# @Date: 2020-07-07 17:32:50
# @LastEditTime: 2020-07-24 14:31:43
# @LastEditors: Keyangzhang


# net.getEdge() get edge object
# traci.edge.getLastStepMeanSpeed()
# traci.edge.getLastStepHaltingNumber()

import traci
from sumolib.net import readNet
import xml.etree.ElementTree as ET

def get_edge_id(edge_file):
    tree = ET.parse(edge_file)
    root = tree.getroot()
    edg_ids = [edg.attrib['id'] for edg in root.iter('edge')]
    return edg_ids

cfg_file = "C:/Users/LEGION/Desktop/DRLSignalControl/YunLiangHeArtery_GuanghuaToQididajie/sumo_files/YunLiangHeArtery_GuanghuaToQididajie.sumocfg"
net_file = "C:/Users/LEGION/Desktop/DRLSignalControl/YunLiangHeArtery_GuanghuaToQididajie/sumo_files/YunLiangHeArtery_GuanghuaToQididajie.net.xml"
edg_file = "C:/Users/LEGION/Desktop/DRLSignalControl/YunLiangHeArtery_GuanghuaToQididajie/sumo_files/YunLiangHeArtery_GuanghuaToQididajie.edg.xml"
add_file = "C:/Users/LEGION/Desktop/DRLSignalControl/YunLiangHeArtery_GuanghuaToQididajie/sumo_files/YunLiangHeArtery_GuanghuaToQididajie.add.xml"
rou_file = "C:/Users/LEGION/Desktop/DRLSignalControl/YunLiangHeArtery_GuanghuaToQididajie/sumo_files/YunLiangHeArtery_GuanghuaToQididajie.rou.xml"

traci.start(['sumo', "-c", cfg_file,"-a",add_file,"-r",rou_file,"--start","--quit-on-end"])

simnet = readNet(net_file)

cumul_delay = 0
cumul_halt_num = 0
cumul_halt_num_artery = 0
cumul_veh_speed = 0
cumul_veh_num = 0
step_length = traci.simulation.getDeltaT()
edge_ids = get_edge_id(edg_file)
edge_leninfo = {edge_id:simnet.getEdge(edge_id).getLength() for edge_id in edge_ids}
edge_speedliminfo = {edge_id:simnet.getEdge(edge_id).getSpeed() for edge_id in edge_ids}


while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()

    for edge_id in edge_ids:
        edge_mean_speed = traci.edge.getLastStepMeanSpeed(edge_id)
        egde_len = edge_leninfo[edge_id]
        edge_speed_lim = edge_speedliminfo[edge_id]
        edge_vehnum = traci.edge.getLastStepVehicleNumber(edge_id)
        egde_halt_num = traci.edge.getLastStepHaltingNumber(edge_id)
        
        if edge_mean_speed >= 0.001:
            edge_delay = step_length*(1-edge_mean_speed/edge_speed_lim)*edge_vehnum
        else:
            edge_delay = step_length*edge_vehnum
       
        cumul_delay+=edge_delay

        cumul_veh_num+=edge_vehnum
        cumul_veh_speed+=edge_mean_speed*edge_vehnum

        cumul_halt_num+=egde_halt_num

avg_delay = cumul_delay/1006
avg_speed = cumul_veh_speed/cumul_veh_num*3.6
avg_halt_num = cumul_halt_num/cumul_veh_num

traci.close()


print(avg_delay)
print(avg_speed)
print(avg_halt_num)