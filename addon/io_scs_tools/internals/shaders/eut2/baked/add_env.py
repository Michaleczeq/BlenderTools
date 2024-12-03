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

from io_scs_tools.internals.shaders.eut2.baked.spec import BakedSpec
from io_scs_tools.internals.shaders.eut2.std_node_groups import linear_to_srgb_ng
from io_scs_tools.internals.shaders.eut2.std_passes.add_env import StdAddEnv
from io_scs_tools.utils import material as _material_utils

class BakedSpecAddEnv(BakedSpec, StdAddEnv):
    MASK_TEX_NODE = "MaskTex"
    MASK_LIN_TO_SRGB_NODE = "MaskLinearToSRGB"

    @staticmethod
    def get_name():
        """Get name of this shader file with full modules path."""
        return __name__

    @staticmethod
    def init(node_tree):
        BakedSpec.init(node_tree)

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
        BakedSpec.init(node_tree)

        
        StdAddEnv.add(node_tree,
                      BakedSpec.GEOM_NODE,
                      None,
                      None,
                      node_tree.nodes[BakedSpec.LIGHTING_EVAL_NODE].outputs['Normal'],
                      node_tree.nodes[BakedSpec.COMPOSE_LIGHTING_NODE].inputs['Env Color'])

        uvmap_n = node_tree.nodes[BakedSpec.UVMAP_NODE]

        add_env_gn = node_tree.nodes[StdAddEnv.ADD_ENV_GROUP_NODE]

        # overrides
        # set strength multiplier to 2 for better visualization in Blender
        node_tree.nodes[StdAddEnv.ADD_ENV_GROUP_NODE].inputs['Strength Multiplier'].default_value = 2.0


        # node creation
        mask_tex_n = node_tree.nodes.new("ShaderNodeTexImage")
        mask_tex_n.name = mask_tex_n.label = BakedSpecAddEnv.MASK_TEX_NODE
        mask_tex_n.location = (start_pos_x + pos_x_shift, start_pos_y + 2200)
        mask_tex_n.width = 140

        mask_lin_to_srgb_n = node_tree.nodes.new("ShaderNodeGroup")
        mask_lin_to_srgb_n.name = mask_lin_to_srgb_n.label = BakedSpecAddEnv.MASK_LIN_TO_SRGB_NODE
        mask_lin_to_srgb_n.location = (start_pos_x + pos_x_shift * 2, start_pos_y + 2100)
        mask_lin_to_srgb_n.node_tree = linear_to_srgb_ng.get_node_group()


        # links creation
        node_tree.links.new(uvmap_n.outputs['UV'], mask_tex_n.inputs['Vector'])

        node_tree.links.new(mask_tex_n.outputs['Color'], mask_lin_to_srgb_n.inputs['Value'])

        node_tree.links.new(mask_lin_to_srgb_n.outputs['Value'], add_env_gn.inputs['Env Factor Color'])


    @staticmethod
    def set_mask_texture(node_tree, image):
        """Set mask texture to shader.

        :param node_tree: node tree of current shader
        :type node_tree: bpy.types.NodeTree
        :param image: texture image which should be assignet to mask texture node
        :type image: bpy.types.Image
        """

        node_tree.nodes[BakedSpecAddEnv.MASK_TEX_NODE].image = image

    @staticmethod
    def set_mask_texture_settings(node_tree, settings):
        """Set mask texture settings to shader.

        :param node_tree: node tree of current shader
        :type node_tree: bpy.types.NodeTree
        :param settings: binary string of TOBJ settings gotten from tobj import
        :type settings: str
        """
        _material_utils.set_texture_settings_to_node(node_tree.nodes[BakedSpecAddEnv.MASK_TEX_NODE], settings)

        # due the fact mask colorspace is linear, we have to manually switch to sRGB and then convert values by node, for effect to work correctly
        node_tree.nodes[BakedSpecAddEnv.MASK_TEX_NODE].image.colorspace_settings.name = 'sRGB'

    @staticmethod
    def set_mask_uv(node_tree, uv_layer):
        """Set UV layer to mask texture in shader.

        :param node_tree: node tree of current shader
        :type node_tree: bpy.types.NodeTree
        :param uv_layer: uv layer string used for nmap texture
        :type uv_layer: str
        """

        pass    # NOTE: as in "baked" shader textures use this same UVs as base_tex, we just ignore this