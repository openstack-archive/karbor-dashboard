#    Copyright (c) 2016 Huawei, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import collections
from collections import namedtuple
from django.utils.translation import ugettext_lazy as _
import json

FILTER_LIST = ['provider_filter', 'plan_filter', 'date_filter']

TODAY = 'today'
LASTESTONEWEEK = 'lastestoneweek'
LASTESTTWOWEEKS = 'lastesttwoweeks'
LASTESTONEMONTH = 'lastestonemonth'
LASTESTTHREEMONTHS = 'lastestthreemonths'

DATE_CHOICES = [(TODAY, _('Today')),
                (LASTESTONEWEEK, _('Lastest one week')),
                (LASTESTTWOWEEKS, _('Lastest two weeks')),
                (LASTESTONEMONTH, _('Lastest one month')),
                (LASTESTTHREEMONTHS, _('Lastest three months'))]
DATE_DICT = collections.OrderedDict(DATE_CHOICES)

Resource = namedtuple("Resource", (
    'type',
    'id',
    'name'
))
GraphNode = namedtuple("GraphNode", (
    "value",
    "child_nodes",
))

PackedGraph = namedtuple('PackedGraph', ['nodes', 'adjacency'])


def deserialize_resource_graph(serialized_resource_graph):
    deserialized_graph = json.loads(serialized_resource_graph)
    packed_resource_graph = PackedGraph(nodes=deserialized_graph[0],
                                        adjacency=deserialized_graph[1])
    for sid, node in packed_resource_graph.nodes.items():
        packed_resource_graph.nodes[sid] = Resource(type=node[0],
                                                    id=node[1],
                                                    name=node[2])
    resource_graph = unpack_graph(packed_resource_graph)
    return resource_graph


def unpack_graph(packed_graph):
    """Return a list of GraphNodes from a PackedGraph

    Unpacks a PackedGraph, which must have the property: each parent node in
    the adjacency list appears after its children.
    """
    (nodes, adjacency_list) = packed_graph
    nodes_dict = dict(nodes)
    graph_nodes_dict = {}

    for (parent_sid, children_sids) in adjacency_list:
        if parent_sid in graph_nodes_dict:
            raise Exception("PackedGraph adjacency list "
                            "must be topologically ordered")
        children = []
        for child_sid in children_sids:
            if child_sid not in graph_nodes_dict:
                graph_nodes_dict[child_sid] = GraphNode(
                    nodes_dict[child_sid], ())
            children.append(graph_nodes_dict[child_sid])
            nodes_dict.pop(child_sid, None)
        graph_nodes_dict[parent_sid] = GraphNode(nodes_dict[parent_sid],
                                                 tuple(children))

    result_nodes = []
    for sid in nodes_dict:
        if sid not in graph_nodes_dict:
            graph_nodes_dict[sid] = GraphNode(nodes_dict[sid], ())
        result_nodes.append(graph_nodes_dict[sid])
    return result_nodes
