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
from io_scs_tools.internals.shaders.eut2.dif_spec_weight_mult2 import DifSpecWeightMult2
from io_scs_tools.internals.shaders.eut2.std_node_groups import mult2_mix_ng
from io_scs_tools.internals.shaders.flavors import tg1
from io_scs_tools.utils import material as _material_utils


class DifSpecWeightMult2Weight2(DifSpecWeightMult2):
    SEC_UVMAP_NODE = "ThrdGeometry"
    SEC_UV_SCALE_NODE = "SecUVScale"
    SEC_SPEC_COLOR_NODE = "SecSpecularColor"
    SEC_SHININESS_MIX_NODE = "SecShininnesMix"
    SPEC_COLOR_MIX_NODE = "SpecularColorMix"
    BASE_1_TEX_NODE = "Base1Tex"
    MULT_1_TEX_NODE = "Mult1Tex"
    SEC_MULT2_MIX_GROUP_NODE = "SecMult2MixGroup"
    COMBINED_ALPHA_MIX_NODE = "CombinedAlphaMixes"
    COMBINED_MIX_NODE = "CombinedMixes"

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
        DifSpecWeightMult2.init(node_tree)

        first_uv_n = node_tree.nodes[DifSpecWeightMult2.UVMAP_NODE]
        base_tex_n = node_tree.nodes[DifSpecWeightMult2.BASE_TEX_NODE]
        spec_col_n = node_tree.nodes[DifSpecWeightMult2.SPEC_COL_NODE]
        vcol_group_n = node_tree.nodes[DifSpecWeightMult2.VCOL_GROUP_NODE]
        mult2_mix_gn = node_tree.nodes[DifSpecWeightMult2.MULT2_MIX_GROUP_NODE]
        spec_mult_n = node_tree.nodes[DifSpecWeightMult2.SPEC_MULT_NODE]
        vcol_mult_n = node_tree.nodes[DifSpecWeightMult2.VCOLOR_MULT_NODE]
        opacity_mult_n = node_tree.nodes[DifSpecWeightMult2.OPACITY_NODE]
        lighting_eval_n = node_tree.nodes[DifSpecWeightMult2.LIGHTING_EVAL_NODE]

        # delete existing
        node_tree.nodes.remove(opacity_mult_n)

        # move existing
        for node in node_tree.nodes:
            if node.location.x > start_pos_x + pos_x_shift * 3:
                node.location.x += pos_x_shift

        # nodes creation
        sec_uv_n = node_tree.nodes.new("ShaderNodeUVMap")
        sec_uv_n.name = sec_uv_n.label = DifSpecWeightMult2Weight2.SEC_UVMAP_NODE
        sec_uv_n.location = (start_pos_x - pos_x_shift * 3, start_pos_y + 600)
        sec_uv_n.uv_map = _MESH_consts.none_uv

        sec_uv_scale_n = node_tree.nodes.new("ShaderNodeMapping")
        sec_uv_scale_n.name = sec_uv_scale_n.label = DifSpecWeightMult2Weight2.SEC_UV_SCALE_NODE
        sec_uv_scale_n.location = (start_pos_x - pos_x_shift, start_pos_y + 600)
        sec_uv_scale_n.vector_type = "POINT"
        sec_uv_scale_n.inputs['Location'].default_value = sec_uv_scale_n.inputs['Rotation'].default_value = (0.0,) * 3
        sec_uv_scale_n.inputs['Scale'].default_value = (1.0,) * 3
        sec_uv_scale_n.width = 140

        sec_spec_col_n = node_tree.nodes.new("ShaderNodeRGB")
        sec_spec_col_n.name = sec_spec_col_n.label = DifSpecWeightMult2Weight2.SEC_SPEC_COLOR_NODE
        sec_spec_col_n.location = (start_pos_x + pos_x_shift, start_pos_y + 2100)

        sec_shininess_mix_n = node_tree.nodes.new("ShaderNodeMix")
        sec_shininess_mix_n.name = sec_shininess_mix_n.label = DifSpecWeightMult2Weight2.SEC_SHININESS_MIX_NODE
        sec_shininess_mix_n.location = (start_pos_x + pos_x_shift * 3, start_pos_y + 2400)
        sec_shininess_mix_n.data_type = "RGBA"
        sec_shininess_mix_n.blend_type = "MIX"

        base_1_tex_n = node_tree.nodes.new("ShaderNodeTexImage")
        base_1_tex_n.name = base_1_tex_n.label = DifSpecWeightMult2Weight2.BASE_1_TEX_NODE
        base_1_tex_n.location = (start_pos_x + pos_x_shift, start_pos_y + 900)
        base_1_tex_n.width = 140

        mult_1_tex_n = node_tree.nodes.new("ShaderNodeTexImage")
        mult_1_tex_n.name = mult_1_tex_n.label = DifSpecWeightMult2Weight2.MULT_1_TEX_NODE
        mult_1_tex_n.location = (start_pos_x + pos_x_shift, start_pos_y + 600)
        mult_1_tex_n.width = 140

        spec_col_mix_n = node_tree.nodes.new("ShaderNodeMix")
        spec_col_mix_n.name = spec_col_mix_n.label = DifSpecWeightMult2Weight2.SPEC_COLOR_MIX_NODE
        spec_col_mix_n.location = (start_pos_x + pos_x_shift * 3, start_pos_y + 2150)
        spec_col_mix_n.data_type = "RGBA"
        spec_col_mix_n.blend_type = "MIX"

        sec_mult2_mix_n = node_tree.nodes.new("ShaderNodeGroup")
        sec_mult2_mix_n.name = sec_mult2_mix_n.label = DifSpecWeightMult2Weight2.SEC_MULT2_MIX_GROUP_NODE
        sec_mult2_mix_n.location = (start_pos_x + pos_x_shift * 3, start_pos_y + 800)
        sec_mult2_mix_n.node_tree = mult2_mix_ng.get_node_group()

        combined_a_mix_n = node_tree.nodes.new("ShaderNodeMix")
        combined_a_mix_n.name = combined_a_mix_n.label = DifSpecWeightMult2Weight2.COMBINED_ALPHA_MIX_NODE
        combined_a_mix_n.location = (start_pos_x + pos_x_shift * 4, start_pos_y + 1250)
        combined_a_mix_n.data_type = "RGBA"
        combined_a_mix_n.blend_type = "MIX"

        combined_mix_n = node_tree.nodes.new("ShaderNodeMix")
        combined_mix_n.name = combined_mix_n.label = DifSpecWeightMult2Weight2.COMBINED_MIX_NODE
        combined_mix_n.location = (start_pos_x + pos_x_shift * 4, start_pos_y + 1000)
        combined_mix_n.data_type = "RGBA"
        combined_mix_n.blend_type = "MIX"

        # links creation
        node_tree.links.new(sec_uv_scale_n.inputs["Vector"], sec_uv_n.outputs["UV"])
        node_tree.links.new(base_tex_n.inputs["Vector"], first_uv_n.outputs["UV"])

        node_tree.links.new(mult_1_tex_n.inputs["Vector"], sec_uv_scale_n.outputs["Vector"])
        node_tree.links.new(base_1_tex_n.inputs["Vector"], sec_uv_n.outputs["UV"])

        # pass 1
        node_tree.links.new(sec_shininess_mix_n.inputs["Factor"], vcol_group_n.outputs["Vertex Color Alpha"])

        node_tree.links.new(spec_col_mix_n.inputs["Factor"], vcol_group_n.outputs["Vertex Color Alpha"])
        node_tree.links.new(spec_col_mix_n.inputs["A"], spec_col_n.outputs["Color"])
        node_tree.links.new(spec_col_mix_n.inputs["B"], sec_spec_col_n.outputs["Color"])

        node_tree.links.new(sec_mult2_mix_n.inputs["Base Alpha"], base_1_tex_n.outputs["Alpha"])
        node_tree.links.new(sec_mult2_mix_n.inputs["Base Color"], base_1_tex_n.outputs["Color"])
        node_tree.links.new(sec_mult2_mix_n.inputs["Mult Alpha"], mult_1_tex_n.outputs["Alpha"])
        node_tree.links.new(sec_mult2_mix_n.inputs["Mult Color"], mult_1_tex_n.outputs["Color"])

        # pass 2
        node_tree.links.new(combined_a_mix_n.inputs["Factor"], vcol_group_n.outputs["Vertex Color Alpha"])
        node_tree.links.new(combined_a_mix_n.inputs["A"], mult2_mix_gn.outputs["Mix Alpha"])
        node_tree.links.new(combined_a_mix_n.inputs["B"], sec_mult2_mix_n.outputs["Mix Alpha"])

        node_tree.links.new(combined_mix_n.inputs["Factor"], vcol_group_n.outputs["Vertex Color Alpha"])
        node_tree.links.new(combined_mix_n.inputs["A"], mult2_mix_gn.outputs["Mix Color"])
        node_tree.links.new(combined_mix_n.inputs["B"], sec_mult2_mix_n.outputs["Mix Color"])

        # pass 3
        node_tree.links.new(spec_mult_n.inputs[0], spec_col_mix_n.outputs["Result"])
        node_tree.links.new(spec_mult_n.inputs[1], combined_a_mix_n.outputs["Result"])

        node_tree.links.new(vcol_mult_n.inputs[1], combined_mix_n.outputs["Result"])

        # pass 4
        node_tree.links.new(lighting_eval_n.inputs["Shininess"], sec_shininess_mix_n.outputs["Result"])

    @staticmethod
    def set_shininess(node_tree, factor):
        """Set shininess factor to shader.

        :param node_tree: node tree of current shader
        :type node_tree: bpy.types.NodeTree
        :param factor: shininess factor
        :type factor: float
        """

        node_tree.nodes[DifSpecWeightMult2Weight2.SEC_SHININESS_MIX_NODE].inputs["A"].default_value = (factor,) * 4

    @staticmethod
    def set_reflection2(node_tree, value):
        """Set second reflection.

        NOTE: just passed because it's not reflected in 3D viewport anyway

        :param node_tree: node tree of current shader
        :type node_tree: bpy.types.NodeTree
        :param value: reflection value
        :type value: float
        """
        pass

    @staticmethod
    def set_aux3(node_tree, aux_property):
        """Set second specular and second shininess for the shader.

        :param node_tree: node tree of current shader
        :type node_tree: bpy.types.NodeTree
        :param aux_property: second specular and shininess factor represented with property group
        :type aux_property: bpy.types.IDPropertyGroup
        """

        color = (aux_property[0]["value"], aux_property[1]["value"], aux_property[2]["value"], 1.0)
        node_tree.nodes[DifSpecWeightMult2Weight2.SEC_SPEC_COLOR_NODE].outputs["Color"].default_value = color

        factor = aux_property[3]["value"]
        node_tree.nodes[DifSpecWeightMult2Weight2.SEC_SHININESS_MIX_NODE].inputs["B"].default_value = (factor,) * 4

    @staticmethod
    def set_aux5(node_tree, aux_property):
        """Set UV scaling factors for the shader.

        :param node_tree: node tree of current shader
        :type node_tree: bpy.types.NodeTree
        :param aux_property: UV scale factor represented with property group
        :type aux_property: bpy.types.IDPropertyGroup
        """

        DifSpecWeightMult2.set_aux5(node_tree, aux_property)

        node_tree.nodes[DifSpecWeightMult2Weight2.SEC_UV_SCALE_NODE].inputs['Scale'].default_value[0] = aux_property[2]["value"]
        node_tree.nodes[DifSpecWeightMult2Weight2.SEC_UV_SCALE_NODE].inputs['Scale'].default_value[1] = aux_property[3]["value"]

    @staticmethod
    def set_base_uv(node_tree, uv_layer):
        """Set UV layer to base texture in shader.

        :param node_tree: node tree of current shader
        :type node_tree: bpy.types.NodeTree
        :param uv_layer: uv layer string used for first base and mult texture
        :type uv_layer: str
        """

        DifSpecWeightMult2.set_mult_uv(node_tree, uv_layer)

    @staticmethod
    def set_base_1_texture(node_tree, image):
        """Set base_1 texture to shader.

        :param node_tree: node tree of current shader
        :type node_tree: bpy.types.NodeTree
        :param image: texture image which should be assigned to base_1 texture node
        :type image: bpy.types.Texture
        """

        node_tree.nodes[DifSpecWeightMult2Weight2.BASE_1_TEX_NODE].image = image

    @staticmethod
    def set_base_1_texture_settings(node_tree, settings):
        """Set base_1 texture settings to shader.

        :param node_tree: node tree of current shader
        :type node_tree: bpy.types.NodeTree
        :param settings: binary string of TOBJ settings gotten from tobj import
        :type settings: str
        """
        _material_utils.set_texture_settings_to_node(node_tree.nodes[DifSpecWeightMult2Weight2.BASE_1_TEX_NODE], settings)

    @staticmethod
    def set_base_1_uv(node_tree, uv_layer):
        """Set UV layer to base_1 texture in shader.

        :param node_tree: node tree of current shader
        :type node_tree: bpy.types.NodeTree
        :param uv_layer: uv layer string used for base_1 texture
        :type uv_layer: str
        """

        if uv_layer is None or uv_layer == "":
            uv_layer = _MESH_consts.none_uv

        node_tree.nodes[DifSpecWeightMult2Weight2.SEC_UVMAP_NODE].uv_map = uv_layer

    @staticmethod
    def set_mult_1_texture(node_tree, image):
        """Set mult_1 texture to shader.

        :param node_tree: node tree of current shader
        :type node_tree: bpy.types.NodeTree
        :param image: texture image which should be assigned to mult_1 texture node
        :type image: bpy.types.Texture
        """

        node_tree.nodes[DifSpecWeightMult2Weight2.MULT_1_TEX_NODE].image = image

    @staticmethod
    def set_mult_1_texture_settings(node_tree, settings):
        """Set mult_1 texture settings to shader.

        :param node_tree: node tree of current shader
        :type node_tree: bpy.types.NodeTree
        :param settings: binary string of TOBJ settings gotten from tobj import
        :type settings: str
        """
        _material_utils.set_texture_settings_to_node(node_tree.nodes[DifSpecWeightMult2Weight2.MULT_1_TEX_NODE], settings)

    @staticmethod
    def set_mult_1_uv(node_tree, uv_layer):
        """Set UV layer to mult_1 texture in shader.

        :param node_tree: node tree of current shader
        :type node_tree: bpy.types.NodeTree
        :param uv_layer: uv layer string used for mult_1 texture
        :type uv_layer: str
        """

        DifSpecWeightMult2Weight2.set_base_1_uv(node_tree, uv_layer)

    @staticmethod
    def set_alpha_test_flavor(node_tree, switch_on):
        """Set alpha test flavor to this shader.

        :param node_tree: node tree of current shader
        :type node_tree: bpy.types.NodeTree
        :param switch_on: flag indication if alpha test should be switched on or off
        :type switch_on: bool
        """

        pass  # NOTE: no support for this flavor; overriding with empty function

    @staticmethod
    def set_blend_over_flavor(node_tree, switch_on):
        """Set blend over flavor to this shader.

        :param node_tree: node tree of current shader
        :type node_tree: bpy.types.NodeTree
        :param switch_on: flag indication if blend over should be switched on or off
        :type switch_on: bool
        """

        pass  # NOTE: no support for this flavor; overriding with empty function

    @staticmethod
    def set_blend_add_flavor(node_tree, switch_on):
        """Set blend add flavor to this shader.

        :param node_tree: node tree of current shader
        :type node_tree: bpy.types.NodeTree
        :param switch_on: flag indication if blend add should be switched on or off
        :type switch_on: bool
        """

        pass  # NOTE: no support for this flavor; overriding with empty function

    @staticmethod
    def set_blend_mult_flavor(node_tree, switch_on):
        """Set blend mult flavor to this shader.

        :param node_tree: node tree of current shader
        :type node_tree: bpy.types.NodeTree
        :param switch_on: flag indication if blend mult should be switched on or off
        :type switch_on: bool
        """

        pass  # NOTE: no support for this flavor; overriding with empty function

    @staticmethod
    def set_tg1_flavor(node_tree, switch_on):
        """Set zero texture generation flavor to this shader.

        :param node_tree: node tree of current shader
        :type node_tree: bpy.types.NodeTree
        :param switch_on: flag indication if flavor should be switched on or off
        :type switch_on: bool
        """

        if switch_on and not tg1.is_set(node_tree):

            out_node = node_tree.nodes[DifSpecWeightMult2Weight2.GEOM_NODE]
            in_node = node_tree.nodes[DifSpecWeightMult2Weight2.SEC_UV_SCALE_NODE]
            in_node2 = node_tree.nodes[DifSpecWeightMult2Weight2.BASE_1_TEX_NODE]

            out_node.location.x -= 185 * 2
            location = (out_node.location.x + 185, out_node.location.y)

            tg1.init(node_tree, location, out_node.outputs["Position"], in_node.inputs["Vector"])
            tg1.init(node_tree, location, out_node.outputs["Position"], in_node2.inputs["Vector"])

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
