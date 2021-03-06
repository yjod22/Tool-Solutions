#!env/bin/python3

# The confidential and proprietary information contained in this file may
# only be used by a person authorised under and to the extent permitted
# by a subsisting licensing agreement from ARM Limited or its affiliates.
#
# (C) COPYRIGHT 2020 ARM Limited or its affiliates.
# ALL RIGHTS RESERVED
#
# This entire notice must be reproduced on all copies of this file
# and copies of this file may only be made by a person if such person is
# permitted to do so under the terms of a subsisting license agreement
# from ARM Limited or its affiliates.

import datetime
import librosa
import math
import numpy as np
from os import path
from typing import IO

def write_license_header(f: IO, header_template_file):
    """
    Writes the license header
    """
    if not path.isfile(header_template_file):
        raise Exception(f"Header template file not found at {header_template_file}")

    with open(header_template_file, "r") as header_file:
        license_hdr = header_file.read()

        if 0 == len(license_hdr):
            raise Exception("License text is empty!")

        f.write(license_hdr)


def write_autogen_comment(f: IO, tool_name, file_name):
    # Constants:
    auto_gen_comments = f"""
/*********************    Autogenerated file. DO NOT EDIT *******************
 * Generated from {tool_name} tool and  {file_name} file.
 * Date: {str(datetime.datetime.now())}
 ***************************************************************************/\n"""
    f.write(auto_gen_comments)


def write_includes(f: IO, includes):
    # Write includes
    for include in includes:
        f.write(f"\n#include {include}")
    f.write('\n\n')


def write_hex_array(f: IO, hex_array):
    size = len(hex_array)
    f.write('{\n')
    for line in np.array_split(hex_array, math.ceil(size/20)):
        np.savetxt(f, line, newline=', ', fmt="%#4x")
        f.write('\n')
    f.write('\n};\n')


def prepare_audio_clip(path, sampling_rate_value=16000, mono_value=True, offset_value=0.0 , duration_value=0, res_type_value='kaiser_best', min_len=16000):
    duration_value_to_use = duration_value if duration_value > 0 else None
    y, sr = librosa.load(path,
                        sr=sampling_rate_value,
                        mono=mono_value,
                        offset=offset_value,
                        duration=duration_value_to_use,
                        res_type=res_type_value)
    if (y.shape[0]<min_len):
        sample_to_pad = min_len - y.shape[0]
        y =  np.pad(y, (0, sample_to_pad), 'constant', constant_values=(0))
    return y, sr