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

# Copyright (C) 2025: SCS Software

# Converting script based on the mwl4 script from https://github.com/mwl4/ConverterPIX/

class AttributeConvert:
    def __init__(self, name, value_count, start_index):
        self.name = name
        self.value_count = value_count
        self.start_index = start_index

default_map_to_material = {
    "additional_ambient": AttributeConvert("add_ambient", 1, 0),
    "glass_tint_color": AttributeConvert("tint", 3, 0),
    "glass_tint_opacity": AttributeConvert("tint_opacity", 1, 0),
    "shadowmap_bias": AttributeConvert("shadow_bias", 1, 0),
    "paintjob_base_color": AttributeConvert("aux[8]", 3, 0),
    "specular_secondary": AttributeConvert("aux[3]", 4, 0),
    "shininess_secondary": AttributeConvert("aux[3]", 4, 3),
    "reflection_secondary": AttributeConvert("reflection2", 1, 0),
    "lod_selector": AttributeConvert("aux[1]", 1, 0),
    "shadow_offset": AttributeConvert("aux[0]", 1, 0),
    "amod_decal_blending_factors": AttributeConvert("aux[0]", 2, 0),
    "texgen_0_gen": AttributeConvert("aux[0]", 4, 0),
    "texgen_0_rot": AttributeConvert("aux[0]", 4, 2),
    "texgen_1_gen": AttributeConvert("aux[1]", 4, 0),
    "texgen_1_rot": AttributeConvert("aux[1]", 4, 2),
    "far_color": AttributeConvert("aux[2]", 4, 0),
    "far_specular_power": AttributeConvert("aux[2]", 4, 3),
    "depth_bias": AttributeConvert("aux[0]", 1, 0),
    "luminance_output": AttributeConvert("aux[5]", 2, 0),
    "luminance_night": AttributeConvert("aux[5]", 2, 1),
    "interior_atlas_dimensions": AttributeConvert("aux[1]", 2, 0),
    "interior_glass_color": AttributeConvert("aux[2]", 4, 0),
    "interior_unit_room_dimensions": AttributeConvert("aux[0]", 2, 0),
    "water_distances": AttributeConvert("aux[0]", 3, 0),
    "water_near_color": AttributeConvert("aux[1]", 3, 0),
    "water_horizon_color": AttributeConvert("aux[2]", 3, 0),
    "water_layer_0_yaw": AttributeConvert("aux[3]", 4, 0),
    "water_layer_0_speed": AttributeConvert("aux[3]", 4, 1),
    "water_layer_0_scale": AttributeConvert("aux[3]", 4, 2),
    "water_layer_1_yaw": AttributeConvert("aux[4]", 4, 0),
    "water_layer_1_speed": AttributeConvert("aux[4]", 4, 1),
    "water_layer_1_scale": AttributeConvert("aux[4]", 4, 2),
    "water_mirror": AttributeConvert("aux[5]", 1, 0),
    "animsheet_cfg_fps": AttributeConvert("aux[0]", 3, 0),
    "animsheet_cfg_frames_row": AttributeConvert("aux[0]", 3, 1),
    "animsheet_cfg_frames_total": AttributeConvert("aux[0]", 3, 2),
    "animsheet_frame_width": AttributeConvert("aux[1]", 2, 0),
    "animsheet_frame_height": AttributeConvert("aux[1]", 2, 1),
    "detail_fadeout_from": AttributeConvert("aux[5]", 4, 0),
    "detail_fadeout_range": AttributeConvert("aux[5]", 4, 1),
    "detail_blend_bias": AttributeConvert("aux[5]", 4, 2),
    "detail_uv_scale": AttributeConvert("aux[5]", 4, 3),
    "animation_speed": AttributeConvert("aux[0]", 1, 0),
    "showroom_r_color": AttributeConvert("aux[0]", 1, 0),
    "showroom_speed": AttributeConvert("aux[4]", 3, 0),
    "flake_uvscale": AttributeConvert("aux[5]", 4, 0),
    "flake_shininess": AttributeConvert("aux[5]", 4, 1),
    "flake_clearcoat_rolloff": AttributeConvert("aux[5]", 4, 2),
    "flake_vratio": AttributeConvert("aux[5]", 4, 3),
    "flake_color": AttributeConvert("aux[6]", 4, 0),
    "flake_density": AttributeConvert("aux[6]", 4, 3),
    "flip_color": AttributeConvert("aux[7]", 4, 0),
    "flip_strength": AttributeConvert("aux[7]", 4, 3),
    "mix00_diffuse_secondary": AttributeConvert("aux[0]", 3, 0),
    "mult_uvscale": AttributeConvert("aux[5]", 4, 0),
    "mult_uvscale_secondary": AttributeConvert("aux[5]", 4, 2),
    "sheet_frame_size_r": AttributeConvert("aux[0]", 4, 0),
    "sheet_frame_size_g": AttributeConvert("aux[0]", 4, 2),
    "sheet_frame_size_b": AttributeConvert("aux[1]", 4, 0),
    "sheet_frame_size_a": AttributeConvert("aux[1]", 4, 2),
    "paintjob_r_color": AttributeConvert("aux[5]", 3, 0),
    "paintjob_g_color": AttributeConvert("aux[6]", 3, 0),
    "paintjob_b_color": AttributeConvert("aux[7]", 3, 0),
}

class AttributeConverter:
    def __init__(self):
        self.temp_values = {}

    def effect_to_material(self, attribute, value):
        """Converts effect attribute to material attribute if present in the mapping list.
    
        :param attribute: attribute name to convert
        :type attribute: str
        :param value: value of attribute to convert
        :type value: int, float, tuple
        :return: tuple of converted attribute name and value
        :rtype: (attr, val)
        """
        if attribute in default_map_to_material:
            conversion = default_map_to_material[attribute]
            attr = conversion.name

            if not isinstance(value, tuple):
                value = (value,)

            # check for values in temp_values
            if attr in self.temp_values:
                val = list(self.temp_values[attr])
            else:
                val = [None] * conversion.value_count

            # insert values into correct positions
            for i, v in enumerate(value):
                val[conversion.start_index + i] = v

            # save updated value in temp_values if not fully filled
            if None in val or 0.0 in val:
                self.temp_values[attr] = tuple(val)
            else:
                self.temp_values.pop(attr, None)

            # set none to 0.0
            val = tuple(v if v is not None else 0.0 for v in val)

            # return single value if only one
            if len(val) == 1:
                val = val[0]

        else:
            attr = attribute
            val = value

        return attr, val
