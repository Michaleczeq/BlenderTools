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

# Copyright (C) 2015-2019: SCS Software

from io_scs_tools.consts import Mesh as _MESH_consts
from io_scs_tools.internals.shaders.eut2.dif_spec import DifSpec
from io_scs_tools.internals.shaders.flavors import tg1
from io_scs_tools.utils import material as _material_utils


class DifSpecOverDifOpac(DifSpec):
    SEC_UVMAP_NODE = "SecUVMap"
    OVER_TEX_NODE = "OverTex"
    OVER_MIX_NODE = "OverMix"

    @staticmethod
    def get_name():
        """Get name of this shader file with full modules path."""
        return __name__

    @staticmethod
    def init(node_tree):
        """Initialize node tree with links for this shader.

        :param node_tree: node tree on which this shader should be created
        :type node_tree: bpy.types.NodeTree
        """

        start_pos_x = 0
        start_pos_y = 0

        pos_x_shift = 185

        # init parent
        DifSpec.init(node_tree, disable_remap_alpha=True)

        base_tex_n = node_tree.nodes[DifSpec.BASE_TEX_NODE]
        vcol_mult_n = node_tree.nodes[DifSpec.VCOLOR_MULT_NODE]
        opacity_mult_n = node_tree.nodes[DifSpec.OPACITY_NODE]

        # move existing
        opacity_mult_n.location.y -= 200

        # nodes creation
        sec_uv_n = node_tree.nodes.new("ShaderNodeUVMap")
        sec_uv_n.name = DifSpecOverDifOpac.SEC_UVMAP_NODE
        sec_uv_n.label = DifSpecOverDifOpac.SEC_UVMAP_NODE
        sec_uv_n.location = (start_pos_x - pos_x_shift, start_pos_y + 900)
        sec_uv_n.uv_map = _MESH_consts.none_uv

        over_tex_n = node_tree.nodes.new("ShaderNodeTexImage")
        over_tex_n.name = DifSpecOverDifOpac.OVER_TEX_NODE
        over_tex_n.label = DifSpecOverDifOpac.OVER_TEX_NODE
        over_tex_n.location = (start_pos_x + pos_x_shift, start_pos_y + 1200)
        over_tex_n.width = 140

        over_mix_node = node_tree.nodes.new("ShaderNodeMix")
        over_mix_node.name = DifSpecOverDifOpac.OVER_MIX_NODE
        over_mix_node.label = DifSpecOverDifOpac.OVER_MIX_NODE
        over_mix_node.location = (start_pos_x + pos_x_shift * 3, start_pos_y + 1350)
        over_mix_node.data_type = "RGBA"
        over_mix_node.blend_type = "MIX"

        # links creation
        node_tree.links.new(over_tex_n.inputs['Vector'], sec_uv_n.outputs['UV'])

        node_tree.links.new(over_mix_node.inputs['Factor'], over_tex_n.outputs['Alpha'])
        node_tree.links.new(over_mix_node.inputs['A'], base_tex_n.outputs['Color'])
        node_tree.links.new(over_mix_node.inputs['B'], over_tex_n.outputs['Color'])

        node_tree.links.new(vcol_mult_n.inputs[1], over_mix_node.outputs['Result'])

    @staticmethod
    def set_aux1(node_tree, aux_property):
        """Set second texture generation scale and rotation.

        :param node_tree: node tree of current shader
        :type node_tree: bpy.types.NodeTree
        :param aux_property: secondary specular color represented with property group
        :type aux_property: bpy.types.IDPropertyGroup
        """

        if tg1.is_set(node_tree):
           # Fix for old float2 aux[1]
            if (len(aux_property)) == 2:
                tg1.set_scale(node_tree, aux_property[0]['value'], aux_property[1]['value'], 0)
            else:
                tg1.set_scale(node_tree, aux_property[0]['value'], aux_property[1]['value'], aux_property[2]['value'])

    @staticmethod
    def set_reflection2(node_tree, value):
        """Set second reflection factor to shader.

        :param node_tree: node tree of current shader
        :type node_tree: bpy.types.NodeTree
        :param value: reflection factor
        :type value: float
        """

        pass  # NOTE: reflection2 attribute doesn't change anything in rendered material, so pass it

    @staticmethod
    def set_over_texture(node_tree, image):
        """Set overlying texture to shader.

        :param node_tree: node tree of current shader
        :type node_tree: bpy.types.NodeTree
        :param image: texture image which should be assigned to over texture node
        :type image: bpy.types.Texture
        """

        node_tree.nodes[DifSpecOverDifOpac.OVER_TEX_NODE].image = image

    @staticmethod
    def set_over_texture_settings(node_tree, settings):
        """Set overlying texture settings to shader.

        :param node_tree: node tree of current shader
        :type node_tree: bpy.types.NodeTree
        :param settings: binary string of TOBJ settings gotten from tobj import
        :type settings: str
        """
        _material_utils.set_texture_settings_to_node(node_tree.nodes[DifSpecOverDifOpac.OVER_TEX_NODE], settings)

    @staticmethod
    def set_over_uv(node_tree, uv_layer):
        """Set UV layer to overlying texture in shader.

        :param node_tree: node tree of current shader
        :type node_tree: bpy.types.NodeTree
        :param uv_layer: uv layer string used for over texture
        :type uv_layer: str
        """

        if uv_layer is None or uv_layer == "":
            uv_layer = _MESH_consts.none_uv

        node_tree.nodes[DifSpecOverDifOpac.SEC_UVMAP_NODE].uv_map = uv_layer

    @staticmethod
    def set_tg1_flavor(node_tree, switch_on):
        """Set second texture generation flavor to this shader.

        :param node_tree: node tree of current shader
        :type node_tree: bpy.types.NodeTree
        :param switch_on: flag indication if flavor should be switched on or off
        :type switch_on: bool
        """

        if switch_on and not tg1.is_set(node_tree):

            out_node = node_tree.nodes[DifSpecOverDifOpac.GEOM_NODE]
            in_node = node_tree.nodes[DifSpecOverDifOpac.OVER_TEX_NODE]

            out_node.location.x -= 185
            location = (out_node.location.x + 185, out_node.location.y)

            tg1.init(node_tree, location, out_node.outputs["Position"], in_node.inputs["Vector"])

        elif not switch_on:

            tg1.delete(node_tree)
