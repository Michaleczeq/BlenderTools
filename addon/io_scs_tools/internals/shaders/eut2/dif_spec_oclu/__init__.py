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


class DifSpecOclu(DifSpec):
    SEC_UVMAP_NODE = "SecUVMap"
    OCLU_TEX_NODE = "OcclusionTexture"
    OCLU_SEPARATE_RGB_NODE = "OcclusionSeparateRGB"
    OCLU_A_MIX_NODE = "OcclusionAlphaMix"
    OCLU_MIX_NODE = "OcclusionMix"

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
        spec_mult_n = node_tree.nodes[DifSpec.SPEC_MULT_NODE]
        vcol_mult_n = node_tree.nodes[DifSpec.VCOLOR_MULT_NODE]

        # move existing
        for node in node_tree.nodes:
            if node.location.x > start_pos_x + pos_x_shift:
                node.location.x += pos_x_shift * 2

        # node creation
        sec_uvmap_n = node_tree.nodes.new("ShaderNodeUVMap")
        sec_uvmap_n.name = sec_uvmap_n.label = DifSpecOclu.SEC_UVMAP_NODE
        sec_uvmap_n.location = (start_pos_x - pos_x_shift, start_pos_y + 900)
        sec_uvmap_n.uv_map = _MESH_consts.none_uv

        oclu_tex_n = node_tree.nodes.new("ShaderNodeTexImage")
        oclu_tex_n.name = oclu_tex_n.label = DifSpecOclu.OCLU_TEX_NODE
        oclu_tex_n.location = (start_pos_x + pos_x_shift, start_pos_y + 1200)
        oclu_tex_n.width = 140

        oclu_sep_rgb_n = node_tree.nodes.new("ShaderNodeSeparateColor")
        oclu_sep_rgb_n.name = oclu_sep_rgb_n.label = DifSpecOclu.OCLU_SEPARATE_RGB_NODE
        oclu_sep_rgb_n.location = (start_pos_x + pos_x_shift * 3, start_pos_y + 1200)

        oclu_mix_n = node_tree.nodes.new("ShaderNodeVectorMath")
        oclu_mix_n.name = oclu_mix_n.label = DifSpecOclu.OCLU_MIX_NODE
        oclu_mix_n.location = (start_pos_x + pos_x_shift * 4, start_pos_y + 1400)
        oclu_mix_n.operation = "MULTIPLY"

        oclu_a_mix_n = node_tree.nodes.new("ShaderNodeMath")
        oclu_a_mix_n.name = oclu_a_mix_n.label = DifSpecOclu.OCLU_A_MIX_NODE
        oclu_a_mix_n.location = (start_pos_x + pos_x_shift * 4, start_pos_y + 1600)
        oclu_a_mix_n.operation = "MULTIPLY"

        # links creation
        node_tree.links.new(oclu_tex_n.inputs["Vector"], sec_uvmap_n.outputs["UV"])

        # pass 1
        node_tree.links.new(oclu_sep_rgb_n.inputs["Color"], oclu_tex_n.outputs["Color"])

        # pass 2
        node_tree.links.new(oclu_a_mix_n.inputs[0], base_tex_n.outputs["Alpha"])
        node_tree.links.new(oclu_a_mix_n.inputs[1], oclu_sep_rgb_n.outputs["Red"])

        node_tree.links.new(oclu_mix_n.inputs[0], base_tex_n.outputs["Color"])
        node_tree.links.new(oclu_mix_n.inputs[1], oclu_sep_rgb_n.outputs["Red"])

        # pass 3
        node_tree.links.new(spec_mult_n.inputs[1], oclu_a_mix_n.outputs["Value"])

        # pass 4
        node_tree.links.new(vcol_mult_n.inputs[1], oclu_mix_n.outputs[0])

    @staticmethod
    def set_oclu_texture(node_tree, image):
        """Set occlusion texture to shader.

        :param node_tree: node tree of current shader
        :type node_tree: bpy.types.NodeTree
        :param image: texture image which should be assigned to oclu texture node
        :type image: bpy.types.Texture
        """

        node_tree.nodes[DifSpecOclu.OCLU_TEX_NODE].image = image

    @staticmethod
    def set_oclu_texture_settings(node_tree, settings):
        """Set occlusion texture settings to shader.

        :param node_tree: node tree of current shader
        :type node_tree: bpy.types.NodeTree
        :param settings: binary string of TOBJ settings gotten from tobj import
        :type settings: str
        """
        _material_utils.set_texture_settings_to_node(node_tree.nodes[DifSpecOclu.OCLU_TEX_NODE], settings)

    @staticmethod
    def set_oclu_uv(node_tree, uv_layer):
        """Set UV layer to occlusion texture in shader.

        :param node_tree: node tree of current shader
        :type node_tree: bpy.types.NodeTree
        :param uv_layer: uv layer string used for oclu texture
        :type uv_layer: str
        """

        if uv_layer is None or uv_layer == "":
            uv_layer = _MESH_consts.none_uv

        node_tree.nodes[DifSpecOclu.SEC_UVMAP_NODE].uv_map = uv_layer

    @staticmethod
    def set_tg1_flavor(node_tree, switch_on):
        """Set zero texture generation flavor to this shader.

        :param node_tree: node tree of current shader
        :type node_tree: bpy.types.NodeTree
        :param switch_on: flag indication if flavor should be switched on or off
        :type switch_on: bool
        """

        if switch_on and not tg1.is_set(node_tree):

            out_node = node_tree.nodes[DifSpecOclu.GEOM_NODE]
            in_node = node_tree.nodes[DifSpecOclu.OCLU_TEX_NODE]

            out_node.location.x -= 185
            location = (out_node.location.x + 185, out_node.location.y)

            tg1.init(node_tree, location, out_node.outputs["Position"], in_node.inputs["Vector"])

        elif not switch_on:

            tg1.delete(node_tree)

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
