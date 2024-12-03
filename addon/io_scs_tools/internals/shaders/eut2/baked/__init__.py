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

from io_scs_tools.consts import Mesh as _MESH_consts
from io_scs_tools.internals.shaders.base import BaseShader
from io_scs_tools.internals.shaders.eut2.std_node_groups import compose_lighting_ng
from io_scs_tools.internals.shaders.eut2.std_node_groups import lighting_evaluator_ng
from io_scs_tools.internals.shaders.eut2.std_node_groups import vcolor_input_ng
from io_scs_tools.internals.shaders.flavors import nmap
from io_scs_tools.utils import convert as _convert_utils
from io_scs_tools.utils import material as _material_utils


class Baked(BaseShader):
    GEOM_NODE = "Geometry"
    UVMAP_NODE = "FirstUVs"
    VCOL_GROUP_NODE = "VColorGroup"
    BASE_TEX_NODE = "BaseTex"
    VCOLOR_MULT_NODE = "VertexColorMultiplier"
    VCOLOR_SCALE_NODE = "VertexColorScale"
    LIGHTING_EVAL_NODE = "LightingEvaluator"
    COMPOSE_LIGHTING_NODE = "ComposeLighting"
    OUTPUT_NODE = "Output"

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

        # node creation
        vcol_group_n = node_tree.nodes.new("ShaderNodeGroup")
        vcol_group_n.name = Baked.VCOL_GROUP_NODE
        vcol_group_n.label = Baked.VCOL_GROUP_NODE
        vcol_group_n.location = (start_pos_x - pos_x_shift, start_pos_y + 1650)
        vcol_group_n.node_tree = vcolor_input_ng.get_node_group()

        uvmap_n = node_tree.nodes.new("ShaderNodeUVMap")
        uvmap_n.name = Baked.UVMAP_NODE
        uvmap_n.label = Baked.UVMAP_NODE
        uvmap_n.location = (start_pos_x - pos_x_shift, start_pos_y + 1500)
        uvmap_n.uv_map = _MESH_consts.none_uv

        geometry_n = node_tree.nodes.new("ShaderNodeNewGeometry")
        geometry_n.name = Baked.GEOM_NODE
        geometry_n.label = Baked.GEOM_NODE
        geometry_n.location = (start_pos_x - pos_x_shift, start_pos_y + 1350)

        vcol_scale_n = node_tree.nodes.new("ShaderNodeVectorMath")
        vcol_scale_n.name = Baked.VCOLOR_SCALE_NODE
        vcol_scale_n.label = Baked.VCOLOR_SCALE_NODE
        vcol_scale_n.location = (start_pos_x + pos_x_shift * 3, start_pos_y + 1550)
        vcol_scale_n.operation = "MULTIPLY"
        vcol_scale_n.inputs[1].default_value = (2,) * 3

        base_tex_n = node_tree.nodes.new("ShaderNodeTexImage")
        base_tex_n.name = Baked.BASE_TEX_NODE
        base_tex_n.label = Baked.BASE_TEX_NODE
        base_tex_n.location = (start_pos_x + pos_x_shift, start_pos_y + 1500)
        base_tex_n.width = 140

        vcol_mult_n = node_tree.nodes.new("ShaderNodeVectorMath")
        vcol_mult_n.name = Baked.VCOLOR_MULT_NODE
        vcol_mult_n.label = Baked.VCOLOR_MULT_NODE
        vcol_mult_n.location = (start_pos_x + pos_x_shift * 4, start_pos_y + 1500)
        vcol_mult_n.operation = "MULTIPLY"

        lighting_eval_n = node_tree.nodes.new("ShaderNodeGroup")
        lighting_eval_n.name = Baked.LIGHTING_EVAL_NODE
        lighting_eval_n.label = Baked.LIGHTING_EVAL_NODE
        lighting_eval_n.location = (start_pos_x + pos_x_shift * 7, start_pos_y + 1800)
        lighting_eval_n.node_tree = lighting_evaluator_ng.get_node_group()

        compose_lighting_n = node_tree.nodes.new("ShaderNodeGroup")
        compose_lighting_n.name = Baked.COMPOSE_LIGHTING_NODE
        compose_lighting_n.label = Baked.COMPOSE_LIGHTING_NODE
        compose_lighting_n.location = (start_pos_x + pos_x_shift * 8, start_pos_y + 2000)
        compose_lighting_n.node_tree = compose_lighting_ng.get_node_group()
        compose_lighting_n.inputs["Alpha"].default_value = 1.0

        output_n = node_tree.nodes.new("ShaderNodeOutputMaterial")
        output_n.name = Baked.OUTPUT_NODE
        output_n.label = Baked.OUTPUT_NODE
        output_n.location = (start_pos_x + pos_x_shift * 9, start_pos_y + 1800)

        # links creation
        node_tree.links.new(base_tex_n.inputs['Vector'], uvmap_n.outputs['UV'])
        node_tree.links.new(vcol_scale_n.inputs[0], vcol_group_n.outputs['Vertex Color'])

        node_tree.links.new(vcol_mult_n.inputs[0], vcol_scale_n.outputs[0])
        node_tree.links.new(vcol_mult_n.inputs[1], base_tex_n.outputs['Color'])

        node_tree.links.new(lighting_eval_n.inputs['Normal Vector'], geometry_n.outputs['Normal'])
        node_tree.links.new(lighting_eval_n.inputs['Incoming Vector'], geometry_n.outputs['Incoming'])

        node_tree.links.new(compose_lighting_n.inputs['Diffuse Color'], vcol_mult_n.outputs[0])
        node_tree.links.new(compose_lighting_n.inputs['Specular Lighting'], lighting_eval_n.outputs['Specular Lighting'])
        node_tree.links.new(compose_lighting_n.inputs['Diffuse Lighting'], lighting_eval_n.outputs['Diffuse Lighting'])

        node_tree.links.new(output_n.inputs['Surface'], compose_lighting_n.outputs['Shader'])

    @staticmethod
    def finalize(node_tree, material):
        """Finalize node tree and material settings. Should be called as last.

        :param node_tree: node tree on which this shader should be finalized
        :type node_tree: bpy.types.NodeTree
        :param material: material used for this shader
        :type material: bpy.types.Material
        """

        material.use_backface_culling = True
        material.blend_method = "OPAQUE"

        if material.blend_method == "OPAQUE" and node_tree.nodes[Baked.COMPOSE_LIGHTING_NODE].inputs['Alpha'].links:
            node_tree.links.remove(node_tree.nodes[Baked.COMPOSE_LIGHTING_NODE].inputs['Alpha'].links[0])

    @staticmethod
    def set_shadow_bias(node_tree, value):
        """Set shadow bias attirbute for this shader.

        :param node_tree: node tree of current shader
        :type node_tree: bpy.types.NodeTree
        :param value: shador bias factor
        :type value: float
        """

        pass  # NOTE: shadow bias won't be visualized as game uses it's own implementation

    @staticmethod
    def set_queue_bias(node_tree, value):
        """Set queue bias attirbute for this shader.

        :param node_tree: node tree of current shader
        :type node_tree: bpy.types.NodeTree
        :param value: queue bias index
        :type value: int
        """

        pass  # NOTE: shadow bias won't be visualized as game uses it's own implementation

    @staticmethod
    def set_base_texture(node_tree, image):
        """Set base texture to shader.

        :param node_tree: node tree of current shader
        :type node_tree: bpy.types.NodeTree
        :param image: texture image which should be assignet to base texture node
        :type image: bpy.types.Image
        """

        node_tree.nodes[Baked.BASE_TEX_NODE].image = image

    @staticmethod
    def set_base_texture_settings(node_tree, settings):
        """Set base texture settings to shader.

        :param node_tree: node tree of current shader
        :type node_tree: bpy.types.NodeTree
        :param settings: binary string of TOBJ settings gotten from tobj import
        :type settings: str
        """
        _material_utils.set_texture_settings_to_node(node_tree.nodes[Baked.BASE_TEX_NODE], settings)

    @staticmethod
    def set_base_uv(node_tree, uv_layer):
        """Set UV layer to base texture in shader.

        :param node_tree: node tree of current shader
        :type node_tree: bpy.types.NodeTree
        :param uv_layer: uv layer string used for base texture
        :type uv_layer: str
        """

        if uv_layer is None or uv_layer == "":
            uv_layer = _MESH_consts.none_uv

        node_tree.nodes[Baked.UVMAP_NODE].uv_map = uv_layer

    @staticmethod
    def set_nmap_flavor(node_tree, switch_on):
        """Set normal map flavor to this shader.

        :param node_tree: node tree of current shader
        :type node_tree: bpy.types.NodeTree
        :param switch_on: flag indication if normal map should be switched on or off
        :type switch_on: bool
        """

        if switch_on:

            # find minimal y position for input nodes and position flavor beneath it
            min_y = None
            for node in node_tree.nodes:
                if node.location.x <= 185 and (min_y is None or min_y > node.location.y):
                    min_y = node.location.y

            lighting_eval_n = node_tree.nodes[Baked.LIGHTING_EVAL_NODE]
            geom_n = node_tree.nodes[Baked.GEOM_NODE]
            location = (lighting_eval_n.location.x - 185, min_y - 400)

            nmap.init(node_tree, location, lighting_eval_n.inputs['Normal Vector'], geom_n.outputs['Normal'])
        else:
            nmap.delete(node_tree)

    @staticmethod
    def set_nmap_texture(node_tree, image):
        """Set normal map texture to shader.

        :param node_tree: node tree of current shader
        :type node_tree: bpy.types.NodeTree
        :param image: texture image which should be assignet to nmap texture node
        :type image: bpy.types.Image
        """

        nmap.set_texture(node_tree, image)

    @staticmethod
    def set_nmap_texture_settings(node_tree, settings):
        """Set normal map texture settings to shader.

        :param node_tree: node tree of current shader
        :type node_tree: bpy.types.NodeTree
        :param settings: binary string of TOBJ settings gotten from tobj import
        :type settings: str
        """
        nmap.set_texture_settings(node_tree, settings)

    @staticmethod
    def set_nmap_uv(node_tree, uv_layer):
        """Set UV layer to normal map texture in shader.

        :param node_tree: node tree of current shader
        :type node_tree: bpy.types.NodeTree
        :param uv_layer: uv layer string used for nmap texture
        :type uv_layer: str
        """

        nmap.set_uv(node_tree, uv_layer)
