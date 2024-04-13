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
                if (row[i+1]!=0):
                    node[row[0]].successors.append(self.node_dict(row[i+1]),i+1,row[i+5])

    def get_start_point(self):
        if len(self.node_dict) < 2:
            log.error("Error: the start point is not included.")
            return 0
        return self.node_dict[1]

    def get_node_dict(self):
        return self.node_dict
    
    def BFS(self, node: Node):
        # TODO : design your data structure here for your algorithm
        # Tips : return a sequence of nodes from the node to the nearest unexplored deadend
        def deadend(node: Node,marked: set):
            for succ in node.successors:
                if succ[0] not in marked:
                    return False
            return True
        
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
            if deadend(current_node):
                return reconstruct_path(node, current_node, path)
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
        if is_successor(node_from, node_to):
            next_direction = get_direction(node_from, node_to)

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

    def getActions(self, nodes: List[Node]):
        # TODO : given a sequence of nodes, return the corresponding action sequence
        # Tips : iterate through the nodes and use getAction() in each iteration
        actions = []
        car_dir = Direction.NORTH
        for i in range(len(nodes) - 1):
            node_from = nodes[i]
            node_to = nodes[i + 1]
            action, car_dir = getAction(car_dir, node_from, node_to)
            actions.append(action)
        return actions

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
