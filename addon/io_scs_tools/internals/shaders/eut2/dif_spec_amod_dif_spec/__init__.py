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
from io_scs_tools.utils import material as _material_utils

class DifSpecAmodDifSpec(DifSpec):
    SEC_UVMAP_NODE = "SecondUVMap"
    VCOLOR_SCALE_NODE = "VertexColorScale"
    VCOLOR_SUBTRACT_NODE = "VertexColorSubtract"
    VCOLOR_ABS_NODE = "VertexColorAbsolute"
    VCOLOR_INVERT_NODE = "VertexColorInvert"
    MASK_TEX_NODE = "MaskTex"
    OVER_TEX_NODE = "OverTex"
    MASK_COLOR_INVERT_NODE = "MaskColorInvert"
    MASK_VCOLOR_MIX_NODE = "MaskVertexColorMix"
    MASK_COLOR_MIX_NODE = "MaskColorMix"
    
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
        DifSpec.init(node_tree, disable_remap_alpha=False)
        
        base_tex_n = node_tree.nodes[DifSpec.BASE_TEX_NODE]
        vcol_multi_n = node_tree.nodes[DifSpec.VCOLOR_MULT_NODE]
        vcol_group_n = node_tree.nodes[DifSpec.VCOL_GROUP_NODE]
        
        # node creation
        # - column -1 -
        sec_uvmap_n = node_tree.nodes.new("ShaderNodeUVMap")
        sec_uvmap_n.name = DifSpecAmodDifSpec.SEC_UVMAP_NODE
        sec_uvmap_n.label = DifSpecAmodDifSpec.SEC_UVMAP_NODE
        sec_uvmap_n.location = (start_pos_x - pos_x_shift, start_pos_y + 1000)
        sec_uvmap_n.uv_map = _MESH_consts.none_uv
        
        # - column 1 -
        vcol_scale_n = node_tree.nodes.new("ShaderNodeVectorMath")
        vcol_scale_n.name = DifSpecAmodDifSpec.VCOLOR_SCALE_NODE
        vcol_scale_n.label = DifSpecAmodDifSpec.VCOLOR_SCALE_NODE
        vcol_scale_n.location = (start_pos_x + pos_x_shift, start_pos_y + 1200)
        vcol_scale_n.operation = "MULTIPLY"
        vcol_scale_n.inputs[1].default_value = (2,) * 3
        
        mask_tex_n = node_tree.nodes.new("ShaderNodeTexImage")
        mask_tex_n.name = DifSpecAmodDifSpec.MASK_TEX_NODE
        mask_tex_n.label = DifSpecAmodDifSpec.MASK_TEX_NODE
        mask_tex_n.location = (start_pos_x + pos_x_shift, start_pos_y + 1000)
        mask_tex_n.width = 140
        
        over_tex_n = node_tree.nodes.new("ShaderNodeTexImage")
        over_tex_n.name = DifSpecAmodDifSpec.OVER_TEX_NODE
        over_tex_n.label = DifSpecAmodDifSpec.OVER_TEX_NODE
        over_tex_n.location = (start_pos_x + pos_x_shift, start_pos_y + 700)
        over_tex_n.width = 140

        # - column 2 -
        vcol_subtract_n = node_tree.nodes.new("ShaderNodeVectorMath")
        vcol_subtract_n.name = DifSpecAmodDifSpec.VCOLOR_SUBTRACT_NODE
        vcol_subtract_n.label = DifSpecAmodDifSpec.VCOLOR_SUBTRACT_NODE
        vcol_subtract_n.location = (start_pos_x + pos_x_shift * 2, start_pos_y + 1200)
        vcol_subtract_n.operation = "SUBTRACT"
        vcol_subtract_n.inputs[1].default_value = (1,) * 3

        mask_invert_n = node_tree.nodes.new("ShaderNodeInvert")
        mask_invert_n.name = DifSpecAmodDifSpec.MASK_COLOR_INVERT_NODE
        mask_invert_n.label = DifSpecAmodDifSpec.MASK_COLOR_INVERT_NODE
        mask_invert_n.location = (start_pos_x + pos_x_shift * 2, start_pos_y + 1000)
        mask_invert_n.inputs[0].default_value = 1
        
        # - column 3 -
        vcol_abs_n = node_tree.nodes.new("ShaderNodeVectorMath")
        vcol_abs_n.name = DifSpecAmodDifSpec.VCOLOR_ABS_NODE
        vcol_abs_n.label = DifSpecAmodDifSpec.VCOLOR_ABS_NODE
        vcol_abs_n.location = (start_pos_x + pos_x_shift * 3, start_pos_y + 1100)
        vcol_abs_n.operation = "ABSOLUTE"

        # - column 4 -
        vcol_invert_n = node_tree.nodes.new("ShaderNodeInvert")
        vcol_invert_n.name = DifSpecAmodDifSpec.VCOLOR_INVERT_NODE
        vcol_invert_n.label = DifSpecAmodDifSpec.VCOLOR_INVERT_NODE
        vcol_invert_n.location = (start_pos_x + pos_x_shift * 4, start_pos_y + 1100)
        vcol_invert_n.inputs[0].default_value = 1

        # - column 5 -
        mask_vcol_mix_n = node_tree.nodes.new("ShaderNodeMixRGB")
        mask_vcol_mix_n.name = DifSpecAmodDifSpec.MASK_VCOLOR_MIX_NODE
        mask_vcol_mix_n.label = DifSpecAmodDifSpec.MASK_VCOLOR_MIX_NODE
        mask_vcol_mix_n.location = (start_pos_x + pos_x_shift * 5, start_pos_y + 1100)
        mask_vcol_mix_n.blend_type = "MIX"
        mask_vcol_mix_n.inputs['Color2'].default_value = (1,) * 4

        # - column 6 -
        mask_color_mix_n = node_tree.nodes.new("ShaderNodeMixRGB")
        mask_color_mix_n.name = DifSpecAmodDifSpec.MASK_COLOR_MIX_NODE
        mask_color_mix_n.label = DifSpecAmodDifSpec.MASK_COLOR_MIX_NODE
        mask_color_mix_n.location = (start_pos_x + pos_x_shift * 6, start_pos_y + 1050)
        mask_color_mix_n.blend_type = "MIX"


        
        # links creation
        # - Column -1 -
        node_tree.links.new(vcol_group_n.outputs[1], vcol_scale_n.inputs[0])
        node_tree.links.new(sec_uvmap_n.outputs['UV'], mask_tex_n.inputs['Vector'])
        node_tree.links.new(sec_uvmap_n.outputs['UV'], over_tex_n.inputs['Vector'])
        
        # - Column 1 -
        node_tree.links.new(base_tex_n.outputs['Color'], mask_color_mix_n.inputs['Color2'])
        node_tree.links.new(vcol_scale_n.outputs['Vector'], vcol_subtract_n.inputs[0])
        node_tree.links.new(mask_tex_n.outputs['Color'], mask_invert_n.inputs['Color'])
        node_tree.links.new(over_tex_n.outputs['Color'], mask_color_mix_n.inputs['Color1'])
        
        # - Column 2 -
        node_tree.links.new(vcol_subtract_n.outputs['Vector'], vcol_abs_n.inputs[0])
        node_tree.links.new(mask_invert_n.outputs['Color'], mask_vcol_mix_n.inputs['Color1'])

        # - Column 3 -
        node_tree.links.new(vcol_abs_n.outputs['Vector'], vcol_invert_n.inputs['Color'])

        # - Column 4 -
        node_tree.links.new(vcol_invert_n.outputs['Color'], mask_vcol_mix_n.inputs['Fac'])
        
        # - Column 5 -
        node_tree.links.new(mask_vcol_mix_n.outputs['Color'], mask_color_mix_n.inputs['Fac'])
        
        # - Column 6 -
        node_tree.links.new(mask_color_mix_n.outputs['Color'], vcol_multi_n.inputs[1])
        

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

        node_tree.nodes[DifSpecAmodDifSpec.SEC_UVMAP_NODE].uv_map = uv_layer
        
    @staticmethod
    def set_mask_texture(node_tree, image):
        """Set mask texture to shader.

        :param node_tree: node tree of current shader
        :type node_tree: bpy.types.NodeTree
        :param image: texture image which should be assigned to over texture node
        :type image: bpy.types.Texture
        """

        node_tree.nodes[DifSpecAmodDifSpec.MASK_TEX_NODE].image = image
        
    @staticmethod
    def set_mask_texture_settings(node_tree, settings):
        """Set mask texture settings to shader.

        :param node_tree: node tree of current shader
        :type node_tree: bpy.types.NodeTree
        :param settings: binary string of TOBJ settings gotten from tobj import
        :type settings: str
        """
        # Commented because of texture linear colorspace problems in render
        # _material_utils.set_texture_settings_to_node(node_tree.nodes[DifSpecAmodDifSpec.MASK_TEX_NODE], settings)
        
    @staticmethod
    def set_over_texture(node_tree, image):
        """Set over texture to shader.

        :param node_tree: node tree of current shader
        :type node_tree: bpy.types.NodeTree
        :param image: texture image which should be assigned to mult texture node
        :type image: bpy.types.Texture
        """

        node_tree.nodes[DifSpecAmodDifSpec.OVER_TEX_NODE].image = image
    
    @staticmethod
    def set_over_texture_settings(node_tree, settings):
        """Set mask texture settings to shader.

        :param node_tree: node tree of current shader
        :type node_tree: bpy.types.NodeTree
        :param settings: binary string of TOBJ settings gotten from tobj import
        :type settings: str
        """
        _material_utils.set_texture_settings_to_node(node_tree.nodes[DifSpecAmodDifSpec.OVER_TEX_NODE], settings)
        