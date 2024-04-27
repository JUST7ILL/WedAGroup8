import csv
import logging
import math
from enum import IntEnum
from typing import List

import numpy as np
import pandas

from node import Direction, Node

log = logging.getLogger(__name__)


class Action(IntEnum):
    ADVANCE = 1
    U_TURN = 2
    TURN_RIGHT = 3
    TURN_LEFT = 4
    HALT = 5


class Maze:
    visited = []
    def __init__(self, filepath: str):
        # TODO : read file and implement a data structure you like
        # For example, when parsing raw_data, you may create several Node objects.
        # Then you can store these objects into self.nodes.
        # Finally, add to nd_dict by {key(index): value(corresponding node)}
        self.raw_data = pandas.read_csv(filepath).values
        self.nodes = []
        self.node_dict = dict()  # key: index, value: the correspond node
        for row in self.raw_data:
            index = row[0]
            node = Node(index)
            self.nodes.append(node)
            self.node_dict[index] = node
        for row in self.raw_data:
            for i in range(4):
                if (row[i+1]>0):
                    (self.node_dict[row[0].astype(int)]).set_successor(self.node_dict[row[i+1].astype(int)],i+1,row[i+5])
       
                
    def get_start_point(self):
        if len(self.node_dict) < 2:
            log.error("Error: the start point is not included.")
            return 0
        return self.node_dict[1]

    def get_node_dict(self):
        return self.node_dict
    
    def endcount(self):
        count = 0
        for i in range(1, len(self.node_dict) + 1):
            if len(self.node_dict[i].successors) == 1:
                count += 1
        return count
    
    def BFS(self, node: Node):
        # TODO : design your data structure here for your algorithm
        # Tips : return a sequence of nodes from the node to the nearest unexplored deadend
        def deadend(node: Node,marked: set):
            if len(node.successors) == 1: 
                # print(self.node_to_index(node))
                return True
            return False
            # for succ in node.successors:
            #     if succ[0] not in marked:
            #         return False
            # return True
        
        def reconstruct_path(start_node, end_node, path):
            current_node = end_node
            shortest_path = [current_node]
            while current_node != start_node:
                current_node = path[current_node]
                shortest_path.insert(0, current_node)
            return shortest_path
        
        marked = set()
        queue = []
        path = {}  
        queue.append(node)
        path[node] = None  
        while queue:
            current_node = queue.pop(0)
            marked.add(current_node)
            if deadend(current_node, marked):
                if current_node not in self.visited:
                    self.visited.append(current_node)
                    return reconstruct_path(node, current_node, path), current_node
            for succ in current_node.successors:
                if succ[0] not in marked:
                    queue.append(succ[0])
                    marked.add(succ[0])
                    path[succ[0]] = current_node  
        return []
    
    def BFS_2(self, node_from: Node, node_to: Node):
        # TODO : similar to BFS but with fixed start point and end point
        # Tips : return a sequence of nodes of the shortest path
        def reconstruct_path(start_node, end_node, path):
            current_node = end_node
            shortest_path = [current_node]
            while current_node != start_node:
                current_node = path[current_node]
                shortest_path.insert(0, current_node)
            return shortest_path
        
        marked = set()
        queue = []
        path = {}  
        queue.append(node_from)
        path[node_from] = None  
        while queue:
            current_node = queue.pop(0)
            marked.add(current_node)
            if (current_node == node_to):
                return reconstruct_path(node_from, current_node, path)
            for succ in current_node.successors:
                if succ[0] not in marked:
                    queue.append(succ[0])
                    marked.add(succ[0])
                    path[succ[0]] = current_node  
        return None

    def getAction(self, car_dir, node_from: Node, node_to: Node):
        # TODO : get the car action
        # Tips : return an action and the next direction of the car if the node_to is the Successor of node_to
        # If not, print error message and return 0
        if node_from.is_successor(node_to):
            next_direction = node_from.get_direction(node_to)

            if car_dir == Direction.NORTH:
                if next_direction == Direction.NORTH:
                    return Action.ADVANCE, next_direction
                if next_direction == Direction.SOUTH:
                    return Action.U_TURN, next_direction
                if next_direction == Direction.EAST:
                    return Action.TURN_RIGHT, next_direction
                if next_direction == Direction.WEST:
                    return Action.TURN_LEFT, next_direction
                
            elif car_dir == Direction.SOUTH:
                if next_direction == Direction.NORTH:
                    return Action.U_TURN, next_direction
                if next_direction == Direction.SOUTH:
                    return Action.ADVANCE, next_direction
                if next_direction == Direction.EAST:
                    return Action.TURN_LEFT, next_direction
                if next_direction == Direction.WEST:
                    return Action.TURN_RIGHT, next_direction
                
            elif car_dir == Direction.EAST:
                if next_direction == Direction.NORTH:
                    return Action.TURN_LEFT, next_direction
                if next_direction == Direction.SOUTH:
                    return Action.TURN_RIGHT, next_direction
                if next_direction == Direction.EAST:
                    return Action.ADVANCE, next_direction
                if next_direction == Direction.WEST:
                    return Action.U_TURN, next_direction
                
            else:
                if next_direction == Direction.NORTH:
                    return Action.TURN_RIGHT, next_direction
                if next_direction == Direction.SOUTH:
                    return Action.TURN_LEFT, next_direction
                if next_direction == Direction.EAST:
                    return Action.U_TURN, next_direction
                if next_direction == Direction.WEST:
                    return Action.ADVANCE, next_direction
        else:
            log.error("Error: the node_to is not the successor of node_from")
            return None

    def getActions(self, nodes: List[Node], dir):
        # TODO : given a sequence of nodes, return the corresponding action sequence
        # Tips : iterate through the nodes and use getAction() in each iteration
        actions = []
        car_dir = dir
        for i in range(len(nodes) - 1):
            node_from = nodes[i]
            node_to = nodes[i + 1]
            action, car_dir = self.getAction(car_dir, node_from, node_to)
            actions.append(action)
        return actions, car_dir

    def actions_to_str(self, actions):
        # cmds should be a string sequence like "fbrl....", use it as the input of BFS checklist #1
        cmd = "fbrls"
        cmds = ""
        for action in actions:
            cmds += cmd[action - 1]
        log.info(cmds)
        return cmds

    def strategy(self, node: Node):
        return self.BFS(node)

    def strategy_2(self, node_from: Node, node_to: Node):
        return self.BFS_2(node_from, node_to)
    
    def distance_find(self, node_start: Node):
        self.distance = {}
        for i in range(len(self.nodes)):
            path = self.BFS_2(node_start, self.node_dict[i + 1])
            hori,verti = 0,0
            for j in range(len(path)-1):
                dirc = path[j].get_direction(path[j+1])
                if dirc == Direction.NORTH:
                    verti+=1
                if dirc == Direction.SOUTH:
                    verti-=1
                if dirc == Direction.WEST:
                    hori+=1
                if dirc == Direction.EAST:
                    hori-=1
            if hori<0: hori=-hori
            if verti<0: verti=-verti
            distance = hori+verti
            self.distance[i + 1] = distance
        return self.distance
    
    def first_node(self, node_start: Node, distance: dict):
        distance = self.distance_find(node_start)
        maxvalue , maxindex = 0,0
        for i in range(1,len(self.nodes)+1):
            if distance[i]>maxvalue:
                maxvalue = distance[i]
                maxindex = i
            elif distance[i]==maxvalue:
                if len(self.BFS_2(node_start,self.node_dict[i])) < len(self.BFS_2(node_start,self.node_dict[maxindex])):
                    maxvalue = distance[i]
                    maxindex = i
        return maxindex

    def node_to_index(self, node: Node):
        for i in range(1,len(self.nodes)+1):
            if self.node_dict[i] == node:
                return i
            
    def tresure_hunt(self, init_point): # 先找最遠的 再都找最近的
        #init_point = 6
        dir = Direction.WEST
        nodeStart_index = self.first_node(self.node_dict[init_point],self.distance_find(self.node_dict[init_point]))
        t_str = ""
        node_str = str(init_point)
        self.visited.append(self.node_dict[init_point])
        firstAction , dir = self.getActions(self.strategy_2(self.node_dict[init_point],self.node_dict[nodeStart_index]),dir)
        t_str += self.actions_to_str(firstAction)
        # t_str += "  "
        node_str += "," + str(nodeStart_index)

        now_node = self.node_dict[nodeStart_index]        
        self.visited.append(now_node)
        for i in range(self.endcount() - 2):
            action, now_node = self.strategy(now_node)
            acts, dir = self.getActions(action, dir)
            t_str += self.actions_to_str(acts)
            # t_str += " " 
            node_str += "," + str(self.node_to_index(now_node)) 
        return t_str , node_str
    
    def tresure_hunt2(self, init_point): # 都找最近的
        #init_point = 6
        dir = Direction.WEST
        t_str = ""
        node_str = str(init_point)
        now_node = self.node_dict[init_point]        
        self.visited.append(now_node)
        for i in range(self.endcount() - 1):
            action, now_node = self.strategy(now_node)
            acts, dir = self.getActions(action, dir)
            t_str += self.actions_to_str(acts)
            # t_str += " " 
            node_str += "," + str(self.node_to_index(now_node)) 
        return t_str , node_str
   
#maze = Maze("C:\\Users\\Ricky\\Downloads\\big_maze_112.csv")
#print(maze.tresure_hunt(6))
#maze.visited.clear()
#print(maze.tresure_hunt2(6))
'''
for i in range(len(maze.nodes)):
    print("the distance from node 1 to node ", i+1 ,maze.distance_find(maze.node_dict[47])[i+1])
for i in range(1,len(maze.nodes)):
    print("start at node", i ,"the first node is node ", maze.first_node(maze.node_dict[i],maze.distance_find(maze.node_dict[i])))
'''

'''
maze = Maze("C:\\Users\\yehyo\\Downloads\\medium_maze.csv")
now_node = maze.node_dict[1]
dir = Direction.NORTH
maze.visited.append(now_node)
t_str = ""
for i in range(maze.endcount() - 1):
    action, now_node = maze.strategy(now_node)
    acts, dir = maze.getActions(action, dir)
    t_str += maze.actions_to_str(acts)
    
print(t_str)
'''