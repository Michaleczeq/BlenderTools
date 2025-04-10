# ##### BEGIN GPL LICENSE BLOCK #####
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# Copyright (C) 2015: SCS Software


FLAVOR_ID = "tg1"
TG1_NODE = "TexGen1"


def __create_node__(node_tree):
    """Create node for scaling global coordinates.

    :param node_tree: node tree on which alpha test will be used
    :type node_tree: bpy.types.NodeTree
    """
    vector_mapping_n = node_tree.nodes.new("ShaderNodeMapping")
    vector_mapping_n.name = vector_mapping_n.label = TG1_NODE
    vector_mapping_n.vector_type = "POINT"
    vector_mapping_n.inputs['Location'].default_value = vector_mapping_n.inputs['Rotation'].default_value = (0.0,) * 3
    vector_mapping_n.inputs['Scale'].default_value = (1.0,) * 3


def init(node_tree, location, geom_output, texture_input):
    """Initialize tex generation.

    :param node_tree: node tree on which alpha test will be used
    :type node_tree: bpy.types.NodeTree
    :param location: position in node tree
    :type location: (int, int)
    :param geom_output: node socket from geometry giving vector
    :type geom_output: bpy.types.NodeSocket
    :param texture_input: node socket of texture node to which result should be pointed
    :type texture_input: bpy.types.NodeSocket
    """

    if TG1_NODE not in node_tree.nodes:
        __create_node__(node_tree)

        node_tree.nodes[TG1_NODE].location = location

    # links creation
    nodes = node_tree.nodes

    node_tree.links.new(nodes[TG1_NODE].inputs[0], geom_output)
    node_tree.links.new(texture_input, nodes[TG1_NODE].outputs[0])

    # FIXME: move to old system after: https://developer.blender.org/T68406 is resolved
    flavor_frame = node_tree.nodes.new(type="NodeFrame")
    flavor_frame.name = flavor_frame.label = FLAVOR_ID


def delete(node_tree):
    """Delete alpha test nodes from node tree.

    :param node_tree: node tree from which alpha test should be deleted
    :type node_tree: bpy.types.NodeTree
    """

    if TG1_NODE in node_tree.nodes:
        node_tree.nodes.remove(node_tree.nodes[TG1_NODE])

    if FLAVOR_ID in node_tree.nodes:
        node_tree.nodes.remove(node_tree.nodes[FLAVOR_ID])


def get_node(node_tree):
    """Gets flavor node.

    :param node_tree: node tree from which tex gen flavor node should be returned
    :type node_tree: bpy.types.NodeTree
    :return: node if it's set; otherwise None
    :rtype: bpy.types.NodeTree | None
    """
    return node_tree.nodes[TG1_NODE] if TG1_NODE in node_tree.nodes else None


def is_set(node_tree):
    """Check if flavor is set or not.

    :param node_tree: node tree which should be checked for existance of this flavor
    :type node_tree: bpy.types.NodeTree
    :return: True if flavor exists; False otherwise
    :rtype: bool
    """
    return FLAVOR_ID in node_tree.nodes


def set_scale(node_tree, scale_x, scale_y, rotation):
    """Set scale and rotation of tex generation.

    :param node_tree: node tree which should be checked for existance of this flavor
    :type node_tree: bpy.types.NodeTree
    :param scale_x: x coordinate scaling
    :type scale_x: float
    :param scale_y: y coordinate scaling
    :type scale_y: float
    :param rotation: base texture rotation
    :type rotation: float
    """
    vector_mapping_n = get_node(node_tree)

    if vector_mapping_n:

        vector_mapping_n.inputs['Rotation'].default_value[2] = rotation / 57.3
        vector_mapping_n.inputs['Scale'].default_value[0] = 1 / scale_x
        vector_mapping_n.inputs['Scale'].default_value[1] = 1 / scale_y
