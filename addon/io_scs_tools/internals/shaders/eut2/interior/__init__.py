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

# Copyright (C) 2015-2024: SCS Software

from io_scs_tools.internals.shaders.eut2.parameters import get_fresnel_window
from io_scs_tools.internals.shaders.eut2.dif_spec_add_env import DifSpecAddEnv

class InteriorLit(DifSpecAddEnv):
    VGCOLOR_MULT_NODE = "VertexGlassColorMultiplier"
    GLASS_COL_NODE = "GlassColor"
    GLASS_COL_MIX_NODE = "GlassColorMix"
    GLASS_COL_FAC_NODE = "GlassColorFactor"
    

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
        DifSpecAddEnv.init(node_tree)

        base_tex_n = node_tree.nodes[DifSpecAddEnv.BASE_TEX_NODE]
        vcol_mult_n = node_tree.nodes[DifSpecAddEnv.VCOLOR_MULT_NODE]
        diff_mult_n = node_tree.nodes[DifSpecAddEnv.DIFF_MULT_NODE]

        # set fresnel type to schlick
        node_tree.nodes[DifSpecAddEnv.ADD_ENV_GROUP_NODE].inputs['Fresnel Type'].default_value = 1.0

        # delete existing
        node_tree.nodes.remove(node_tree.nodes[DifSpecAddEnv.OPACITY_NODE])

        # move existing
        diff_mult_n.location.x += pos_x_shift
        vcol_mult_n.location.x += pos_x_shift

        # node creation
        # - column 1 -
        glass_col_n = node_tree.nodes.new("ShaderNodeRGB")
        glass_col_n.name = glass_col_n.label = InteriorLit.GLASS_COL_NODE
        glass_col_n.location = (start_pos_x + pos_x_shift, start_pos_y + 900)

        # - column 2 -
        glass_col_fac_n = node_tree.nodes.new("ShaderNodeValue")
        glass_col_fac_n.name = glass_col_fac_n.label = InteriorLit.GLASS_COL_FAC_NODE
        glass_col_fac_n.location = (start_pos_x + pos_x_shift * 2, start_pos_y + 800)

        # - column 3 -
        vgcol_mult_n = node_tree.nodes.new("ShaderNodeVectorMath")
        vgcol_mult_n.name = vgcol_mult_n.label = InteriorLit.VGCOLOR_MULT_NODE
        vgcol_mult_n.location = (start_pos_x + pos_x_shift * 3, start_pos_y + 1200)
        vgcol_mult_n.operation = "MULTIPLY"

        # - column 4 -
        glass_col_mix_n = node_tree.nodes.new("ShaderNodeMixRGB")
        glass_col_mix_n.name = glass_col_mix_n.label = InteriorLit.GLASS_COL_MIX_NODE
        glass_col_mix_n.location = (start_pos_x + pos_x_shift * 4, start_pos_y + 1200)


        # links creation
        # - column 1 -
        node_tree.links.new(base_tex_n.outputs['Color'], vgcol_mult_n.inputs[0])

        node_tree.links.new(glass_col_n.outputs['Color'], vgcol_mult_n.inputs[1])
        node_tree.links.new(glass_col_n.outputs['Color'], glass_col_mix_n.inputs['Color2'])

        # - column 2 -
        node_tree.links.new(glass_col_fac_n.outputs['Value'], glass_col_mix_n.inputs['Fac'])

        # - column 3 -
        node_tree.links.new(vgcol_mult_n.outputs['Vector'], glass_col_mix_n.inputs['Color1'])

        # - column 4 -
        node_tree.links.new(glass_col_mix_n.outputs['Color'], vcol_mult_n.inputs[1])

    @staticmethod
    def set_fresnel(node_tree, bias_scale):
        """Set fresnel bias and scale value to shader.

        :param node_tree: node tree of current shader
        :type node_tree: bpy.types.NodeTree
        :param bias_scale: bias and scale factors as tuple: (bias, scale)
        :type bias_scale: (float, float)
        """

        bias_scale_window = get_fresnel_window(bias_scale[0], bias_scale[1])

        DifSpecAddEnv.set_fresnel(node_tree, bias_scale_window)
    
    @staticmethod
    def set_aux0(node_tree, aux_property):
        """Set unit room dimension for the shader.

        :param node_tree: node tree of current shader
        :type node_tree: bpy.types.NodeTree
        :param aux_property: TBA
        :type aux_property: bpy.types.IDPropertyGroup
        """
        pass  # NOTE: TBA?

    @staticmethod
    def set_aux1(node_tree, aux_property):
        """Set atlas dimension for the shader.

        :param node_tree: node tree of current shader
        :type node_tree: bpy.types.NodeTree
        :param aux_property: TBA
        :type aux_property: bpy.types.IDPropertyGroup
        """
        pass  # NOTE: TBA?

    @staticmethod
    def set_aux2(node_tree, aux_property):
        """Set glass color for the shader.

        :param node_tree: node tree of current shader
        :type node_tree: bpy.types.NodeTree
        :param aux_property: glass color
        :type aux_property: bpy.types.IDPropertyGroup
        """

        color = (aux_property[0]["value"], aux_property[1]["value"], aux_property[2]["value"], 1.0)
        node_tree.nodes[InteriorLit.GLASS_COL_NODE].outputs["Color"].default_value = color

        factor = aux_property[3]["value"]
        node_tree.nodes[InteriorLit.GLASS_COL_FAC_NODE].outputs["Value"].default_value = factor
        
    @staticmethod
    def set_aux5(node_tree, aux_property):
        """Set luminance boost factor for the shader.

        :param node_tree: node tree of current shader
        :type node_tree: bpy.types.NodeTree
        :param aux_property: luminosity factor represented with property group
        :type aux_property: bpy.types.IDPropertyGroup
        """
        pass  # NOTE: as this variant doesn't use luminance effect we just ignore this factor
