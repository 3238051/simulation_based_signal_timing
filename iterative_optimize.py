# -*- coding: utf-8 -*-

# @Author: KeyangZhang
# @Email: 3238051@qq.com
# @Date: 2020-07-10 16:21:28
# @LastEditTime: 2020-08-16 16:29:19
# @LastEditors: Keyangzhang

import traci
import xml.etree.ElementTree as ET
from sumolib.net import readNet
from itertools import product
import csv

def get_edge_id(edge_file):
    tree = ET.parse(edge_file)
    root = tree.getroot()
    edg_ids = [edg.attrib['id'] for edg in root.iter('edge')]
    return edg_ids

def update_add_file(add_file,cycle,offsets):
    splits = [1.25,1,0.625,0.5]
    green_splits = [int(cycle*s/sum(splits)+0.5) for s in splits]
    phase_durations = []
    for green_split in green_splits:
        phase_durations.append(green_split)
        phase_durations.append(3)

    tree = ET.parse(add_file)
    root = tree.getroot()
    tlclogics = root.findall('tlLogic')
    for tlclogic,offset in zip(tlclogics,offsets):
        tlclogic.attrib['offset']=str(offset)
        for phase,dura in zip(tlclogic,phase_durations):
            phase.attrib['duration']=str(dura)
    tree.write(add_file)

def eval_plan(sumoconfig_file,additional_file,route_file,mode='sumo'):

    traci.start([mode, "-c", sumoconfig_file,"-a",additional_file,'-r',route_file,"--start","--quit-on-end"])
    step_length = traci.simulation.getDeltaT()

    cumul_delay = 0
    cumul_halt_num = 0
    cumul_veh_speed = 0
    cumul_veh_num = 0

    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()

        for edge_id in edge_ids:
            edge_mean_speed = traci.edge.getLastStepMeanSpeed(edge_id)
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
    
    traci.close()

    avg_delay = cumul_delay/1006
    avg_speed = cumul_veh_speed/cumul_veh_num
    avg_halt_num = cumul_halt_num/cumul_veh_num
    return avg_delay,avg_speed*3.6,avg_halt_num

cfg_file = "C:/Users/LEGION/Desktop/DRLSignalControl/YunLiangHeArtery_GuanghuaToQididajie/sumo_files/YunLiangHeArtery_GuanghuaToQididajie.sumocfg"
net_file = "C:/Users/LEGION/Desktop/DRLSignalControl/YunLiangHeArtery_GuanghuaToQididajie/sumo_files/YunLiangHeArtery_GuanghuaToQididajie.net.xml"
edg_file = "C:/Users/LEGION/Desktop/DRLSignalControl/YunLiangHeArtery_GuanghuaToQididajie/sumo_files/YunLiangHeArtery_GuanghuaToQididajie.edg.xml"
add_file = "C:/Users/LEGION/Desktop/DRLSignalControl/YunLiangHeArtery_GuanghuaToQididajie/sumo_files/YunLiangHeArtery_GuanghuaToQididajie.add.xml"
rou_file = "C:/Users/LEGION/Desktop/DRLSignalControl/YunLiangHeArtery_GuanghuaToQididajie/sumo_files/YunLiangHeArtery_GuanghuaToQididajie.rou.xml"

simnet = readNet(net_file)
edge_ids = get_edge_id(edg_file)
edge_leninfo = {edge_id:simnet.getEdge(edge_id).getLength() for edge_id in edge_ids}
edge_speedliminfo = {edge_id:simnet.getEdge(edge_id).getSpeed() for edge_id in edge_ids}

delt_c = 10
delt_o = 4
mean_offsets = [0,27,58,87]
mean_cycle = 75
cycle_range = range(mean_cycle-delt_c,mean_cycle+delt_c,5)
offset0_range = [mean_offsets[0]]
offset1_range = range(mean_offsets[1]-delt_o,mean_offsets[1]+delt_o,2)
offset2_range = range(mean_offsets[2]-delt_o,mean_offsets[2]+delt_o,2)
offset3_range = range(mean_offsets[3]-delt_o,mean_offsets[3]+delt_o,2)
planset = product(cycle_range,offset0_range,offset1_range,offset2_range,offset3_range)


with open('C:/Users/LEGION/Desktop/DRLSignalControl/YunLiangHeArtery_GuanghuaToQididajie/result/方案枚举.txt','w',newline="") as f:    
    for plan in planset:
        cycle = plan[0]
        offsets = plan[1:]
        update_add_file(add_file,cycle,offsets)
        res = eval_plan(cfg_file,add_file,rou_file,mode='sumo-gui')
        f.write(str(cycle)+' ')
        f.write(str(offsets)+' ')
        f.write(str(res))
        f.write('\n')