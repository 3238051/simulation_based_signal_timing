# -*- coding: utf-8 -*-

# @Author: KeyangZhang
# @Email: 3238051@qq.com
# @Date: 2020-07-03 10:58:36
# @LastEditTime: 2020-07-08 13:44:22
# @LastEditors: Keyangzhang

import os
import sys
import logging
import optparse
sys.path.append(os.path.join(os.environ["SUMO_HOME"], "tools"))
import connections  # noqa
import turndefinitions  # noqa

connections_file_path = 'C:/Users/LEGION/Desktop/DRLSignalControl/YunLiangHeArtery_GuanghuaToQididajie/YunLiangHeArtery_GuanghuaToQididajie.con.xml'
turn_definitions_file_path = 'C:/Users/LEGION/Desktop/DRLSignalControl/YunLiangHeArtery_GuanghuaToQididajie/YunLiangHeArtery_GuanghuaToQididajie.turnsdef.xml'
begin = 0
end = 600
connections_file = open(connections_file_path, "r",encoding='utf-8')
turn_definitions_file = open(turn_definitions_file_path, "w",encoding='utf-8')

connections = connections.from_stream(connections_file)
turn_definitions = turndefinitions.from_connections(connections)
turn_definitions_xml = turndefinitions.to_xml(turn_definitions,
                                                begin,
                                                end)
turn_definitions_file.write(turn_definitions_xml)

connections_file.close()
turn_definitions_file.close()