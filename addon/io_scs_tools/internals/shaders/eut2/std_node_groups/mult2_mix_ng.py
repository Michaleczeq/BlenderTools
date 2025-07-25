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

import bpy
from io_scs_tools.consts import Material as _MAT_consts

MULT2_MIX_G = _MAT_consts.node_group_prefix + "Mult2MixGroup"

_SEPARATE_MULT_NODE = "SeparateMult"
_MULT_GREEN_SCALE_NODE = "MultGScale"
_MULT_GREEN_MIX_NODE = "MultGMix"
_MULT_BASE_MULT_NODE = "MultBaseMult"
_ALPHA_MIX_NODE = "AlphaMix"


def get_node_group():
    """Gets node group for calcualtion of environment addition color.

    :return: node group which calculates environment addition color
    :rtype: bpy.types.NodeGroup
    """

    if MULT2_MIX_G not in bpy.data.node_groups:
        __create_node_group__()

    return bpy.data.node_groups[MULT2_MIX_G]


def __create_node_group__():
    """Creates mult2 mix group.

    Inputs: Base Tex Color, Base Tex Alpha, Mult Tex Color, Mult Tex Alpha
    Outputs: Mix Color, Mix Alpha
    """

    start_pos_x = 0
    start_pos_y = 0

    pos_x_shift = 185

    mult2_mix_g = bpy.data.node_groups.new(type="ShaderNodeTree", name=MULT2_MIX_G)

    # inputs defining
    mult2_mix_g.interface.new_socket(in_out = "INPUT", socket_type = "NodeSocketFloat", name = "Base Alpha")
    mult2_mix_g.interface.new_socket(in_out = "INPUT", socket_type = "NodeSocketColor", name = "Base Color")
    mult2_mix_g.interface.new_socket(in_out = "INPUT", socket_type = "NodeSocketFloat", name = "Mult Alpha")
    mult2_mix_g.interface.new_socket(in_out = "INPUT", socket_type = "NodeSocketColor", name = "Mult Color")

    # outputs defining
    mult2_mix_g.interface.new_socket(in_out = "OUTPUT", socket_type = "NodeSocketFloat", name = "Mix Alpha")
    mult2_mix_g.interface.new_socket(in_out = "OUTPUT", socket_type = "NodeSocketColor", name = "Mix Color")


    # nodes creation
    input_n = mult2_mix_g.nodes.new("NodeGroupInput")
    input_n.location = (start_pos_x - pos_x_shift, start_pos_y)

    output_n = mult2_mix_g.nodes.new("NodeGroupOutput")
    output_n.location = (start_pos_x + pos_x_shift * 6, start_pos_y)

    separate_mult_n = mult2_mix_g.nodes.new("ShaderNodeSeparateColor")
    separate_mult_n.name = _SEPARATE_MULT_NODE
    separate_mult_n.label = _SEPARATE_MULT_NODE
    separate_mult_n.location = (start_pos_x + pos_x_shift, start_pos_y)

    mult_green_scale_n = mult2_mix_g.nodes.new("ShaderNodeMath")
    mult_green_scale_n.name = _MULT_GREEN_SCALE_NODE
    mult_green_scale_n.label = _MULT_GREEN_SCALE_NODE
    mult_green_scale_n.location = (start_pos_x + pos_x_shift * 2, start_pos_y)
    mult_green_scale_n.operation = "MULTIPLY"
    mult_green_scale_n.inputs[1].default_value = 2.0

    mult_green_mix_n = mult2_mix_g.nodes.new("ShaderNodeMix")
    mult_green_mix_n.name = _MULT_GREEN_MIX_NODE
    mult_green_mix_n.label = _MULT_GREEN_MIX_NODE
    mult_green_mix_n.location = (start_pos_x + pos_x_shift * 3, start_pos_y + 200)
    mult_green_mix_n.data_type = "RGBA"
    mult_green_mix_n.blend_type = "MIX"
    mult_green_mix_n.inputs["B"].default_value = (1.0,) * 4

    mult_base_mult_n = mult2_mix_g.nodes.new("ShaderNodeVectorMath")
    mult_base_mult_n.name = _MULT_BASE_MULT_NODE
    mult_base_mult_n.label = _MULT_BASE_MULT_NODE
    mult_base_mult_n.location = (start_pos_x + pos_x_shift * 4, start_pos_y + 400)
    mult_base_mult_n.operation = "MULTIPLY"

    alpha_mix_n = mult2_mix_g.nodes.new("ShaderNodeMix")
    alpha_mix_n.name = _ALPHA_MIX_NODE
    alpha_mix_n.label = _ALPHA_MIX_NODE
    alpha_mix_n.location = (start_pos_x + pos_x_shift, start_pos_y - 200)
    alpha_mix_n.data_type = "RGBA"
    alpha_mix_n.blend_type = "MIX"

    # links creation
    mult2_mix_g.links.new(separate_mult_n.inputs["Color"], input_n.outputs["Mult Color"])

    mult2_mix_g.links.new(mult_green_scale_n.inputs[0], separate_mult_n.outputs["Green"])

    mult2_mix_g.links.new(mult_green_mix_n.inputs["Factor"], input_n.outputs["Base Alpha"])
    mult2_mix_g.links.new(mult_green_mix_n.inputs["A"], mult_green_scale_n.outputs["Value"])

    mult2_mix_g.links.new(mult_base_mult_n.inputs[0], input_n.outputs["Base Color"])
    mult2_mix_g.links.new(mult_base_mult_n.inputs[1], mult_green_mix_n.outputs["Result"])

    mult2_mix_g.links.new(alpha_mix_n.inputs["Factor"], input_n.outputs["Base Alpha"])
    mult2_mix_g.links.new(alpha_mix_n.inputs["A"], input_n.outputs["Mult Alpha"])
    mult2_mix_g.links.new(alpha_mix_n.inputs["B"], input_n.outputs["Base Alpha"])

    mult2_mix_g.links.new(output_n.inputs["Mix Color"], mult_base_mult_n.outputs[0])
    mult2_mix_g.links.new(output_n.inputs["Mix Alpha"], alpha_mix_n.outputs["Result"])
