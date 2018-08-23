#! /usr/bin/env python3

import decimal
import sys

svg_width=400
svg_height=200
body_width  = int(svg_width  * 3/4)
body_height = int(svg_height * 1/2)
margin_x = int((svg_width  - body_width ) * 1/2)
margin_y = int((svg_height - body_height) * 1/2)

preamble = f"""\
<svg version="1.1"
     baseProfile="full"
     width="{svg_width}" height="{svg_height}"
     xmlns="http://www.w3.org/2000/svg">
  <!--
  Copyright (c) 2018 Nathaniel Morck Beaver
  This work is licensed under a Creative Commons Attribution 4.0 International License.
  https://creativecommons.org/licenses/by/4.0/
  -->
  <defs>
      <linearGradient id="wire" x1="0" x2="0" y1="0" y2="1">
        <stop offset="0%" stop-color="darkgray"/>
        <stop offset="50%" stop-color="white" stop-opacity="1"/>
        <stop offset="100%" stop-color="gray"/>
      </linearGradient>
      <linearGradient id="goldband" x1="0" x2="0" y1="0" y2="1">
        <stop offset="0%" stop-color="gold"/>
        <stop offset="50%" stop-color="white" stop-opacity="1"/>
        <stop offset="100%" stop-color="gold"/>
      </linearGradient>
      <linearGradient id="silverband" x1="0" x2="0" y1="0" y2="1">
        <stop offset="0%" stop-color="gray"/>
        <stop offset="50%" stop-color="white" stop-opacity="1"/>
        <stop offset="100%" stop-color="gray"/>
      </linearGradient>
  </defs>
"""

postamble = """
</svg>
"""

def get_wire(indent_level=2):
    wire_height = int(svg_height * 1/10)
    x = 0
    y = int((svg_height - wire_height) * 1/2)
    assert y > 0
    svg = f'<rect x="{x}"   y="{y}" width="100%" height="{wire_height}" fill="url(#wire)" />'
    return ' '*indent_level + svg + '\n'

def get_resistor_body(indent_level=2):
    x = margin_x
    y = margin_y
    rx = int(body_width / 20)
    ry = rx
    svg = f'<rect x="{x}"  y="{y}" width="{body_width}" height="{body_height}" fill="khaki" rx="{rx}" ry="{ry}" />'
    return ' '*indent_level + svg + '\n'

def get_digits(ohms, n):
    if ohms == 0:
        return [0], 0
    sign, digits, exponent = ohms.as_tuple()
    # Since we are adding more digits,
    # the multiplier exponent needs to be bumped down.
    extra_digits = n - 1
    adjusted_exponent = ohms.adjusted() - extra_digits
    d = []
    for i in range(n):
        try :
            d.append(digits[i])
        except IndexError:
            d.append(0)

    return d, adjusted_exponent

def get_resistor_bands(ohms_raw, tolerance="20%", n_bands=4, mirror=False):
    assert ohms_raw >= 0
    assert n_bands in (4, 5, 6)
    if n_bands != 4:
        raise NotImplementedError

    ohms = decimal.Decimal(ohms_raw)
    if ohms.is_zero():
        return get_band_0Ohm(n_bands)

    digit_color = {
        0 : "black",
        1 : "brown",
        2 : "red",
        3 : "orange",
        4 : "yellow",
        5 : "green",
        6 : "blue",
        7 : "purple",
        8 : "gray",
        9 : "white",
    }
    multiplier_color = {
        -3 : "pink",
        -2 : "url(#silverband)",
        -1 : "url(#goldband)",
        0 : "black",
        1 : "brown",
        2 : "red",
        3 : "orange",
        4 : "yellow",
        5 : "green",
        6 : "blue",
        7 : "purple",
        8 : "gray",
        9 : "white",
    }
    tolerance_color = {
        "20%"   : None,
        "10%"   : "url(#silverband)",
        "5%"    : "url(#goldband)",
        "1%"    : "brown",
        "2%"    : "red",
        "0.05%" : "orange",
        "0.02%" : "yellow",
        "0.5%"  : "green",
        "0.25%" : "blue",
        "0.1%"  : "purple",
        "0.01%" : "gray",
    }
    digits, exponent = get_digits(ohms, n_bands - 2)
    digit_1, digit_2 = digits
    assert digit_1 in digit_color
    assert digit_2 in digit_color
    if exponent not in multiplier_color:
        raise ValueError("for {} ohms, multiplier exponent not valid: '{}'".format(ohms, exponent))
    band_color_1 = digit_color[digit_1]
    band_color_2 = digit_color[digit_2]
    band_color_3 = multiplier_color[exponent]
    band_color_4 = tolerance_color[tolerance]
    svg = ''
    if mirror:
        svg += get_band(band_color_1, 4)
        svg += get_band(band_color_2, 3)
        svg += get_band(band_color_3, 2)
        svg += get_band(band_color_4, 1)
    else:
        svg += get_band(band_color_1, 1)
        svg += get_band(band_color_2, 2)
        svg += get_band(band_color_3, 3)
        svg += get_band(band_color_4, 4)
    return svg

def get_band_0Ohm(n_bands = 4, indent_level=2):
    # This is laid out centered,
    # which doesn't correspond to a normal position
    # for an even number of bands.
    max_width = int(body_width / (n_bands + 1))
    band_width = int((2/3) * max_width)
    band_height = body_height
    x = int(margin_x + (body_width / 2) - (band_width / 2))
    y = margin_y
    stroke_width = int(min(svg_width, svg_height)*1/40)
    fill_color = "black"
    svg = f'<rect x="{x}"  y="{y}" width="{band_width}" height="{band_height}" fill="{fill_color}" stroke="black" stroke-width="{stroke_width}" />'
    return ' '*indent_level + svg + '\n'

def get_band(fill_color, band_position, n_bands = 4, indent_level=2):
    if fill_color is None:
        return ''
    max_width = int(body_width / (n_bands + 1))
    band_width = int(max_width * 2.0 / 3.0)
    band_height = body_height
    x = int(margin_x + max_width*band_position - (band_width / 2))
    y = margin_y
    stroke_width = int(min(svg_width, svg_height)*1/40)
    svg = f'<rect x="{x}"  y="{y}" width="{band_width}" height="{band_height}" fill="{fill_color}" stroke="black" stroke-width="{stroke_width}" />'
    return ' '*indent_level + svg + '\n'

def write_svg(fp, ohms, tolerance="20%", mirror=False):
    svg = ''
    svg += preamble
    svg += get_wire()
    svg += get_resistor_body()
    svg += get_resistor_bands(ohms, tolerance, mirror=mirror)
    svg += postamble
    fp.write(svg)

E6_series = [
    ('1.0', "20%"),
    ('1.5', "20%"),
    ('2.2', "20%"),
    ('3.3', "20%"),
    ('4.7', "20%"),
    ('6.8', "20%"),
]
# Example of how this works:
# Value Tolerance Min  Max  
#  1.0  20%       0.80  1.20
#  1.5  20%       1.20  1.80
#  2.2  20%       1.76  2.64
#  3.3  20%       2.64  3.96
#  4.7  20%       3.76  5.64
#  6.8  20%       5.44  8.16
# 10.0  20%       8.00 12.00

E12_series = [
    ('1.0', "10%"),
    ('1.2', "10%"),
    ('1.5', "10%"),
    ('1.8', "10%"),
    ('2.2', "10%"),
    ('2.7', "10%"),
    ('3.3', "10%"),
    ('3.9', "10%"),
    ('4.7', "10%"),
    ('5.6', "10%"),
    ('6.8', "10%"),
    ('8.2', "10%"),
]
E24_series = [
    ('1.0', "5%"),
    ('1.1', "5%"),
    ('1.2', "5%"),
    ('1.3', "5%"),
    ('1.5', "5%"),
    ('1.6', "5%"),
    ('1.8', "5%"),
    ('2.0', "5%"),
    ('2.2', "5%"),
    ('2.4', "5%"),
    ('2.7', "5%"),
    ('3.0', "5%"),
    ('3.3', "5%"),
    ('3.6', "5%"),
    ('3.9', "5%"),
    ('4.3', "5%"),
    ('4.7', "5%"),
    ('5.1', "5%"),
    ('5.6', "5%"),
    ('6.2', "5%"),
    ('6.8', "5%"),
    ('7.5', "5%"),
    ('8.2', "5%"),
    ('9.1', "5%"),
]

def idiomatic_name(ohms):
    if ohms == 0:
        return "0 Ohm"
    import math
    magnitude = math.log10(ohms)
    if magnitude >= 10:
        name = "{:.0f} G Ohm".format(ohms/10**9)
    elif magnitude >= 9:
        name = "{:.1f} G Ohm".format(ohms/10**9)
    elif magnitude >= 7:
        name = "{:.0f} M Ohm".format(ohms/10**6)
    elif magnitude >= 6:
        name = "{:.1f} M Ohm".format(ohms/10**6)
    elif magnitude >= 4:
        name = "{:.0f} k Ohm".format(ohms/10**3)
    elif magnitude >= 3:
        name = "{:.1f} k Ohm".format(ohms/10**3)
    elif magnitude < -1:
        name = "{:.0f} m Ohm".format(ohms*10**3)
    elif magnitude > 1:
        name = "{:.0f} Ohm".format(ohms)
    else:
        name = "{} Ohm".format(ohms)
    return name

def get_anki_note(filename, ohms, tolerance=None, mirror=False):
    # TODO: make sure this is valid for an HTML tag
    note_front = '<img src="{}">'.format(filename)
    note_back = ''
    if ohms == 0:
        note_back += '<div>0</div>'
    else:
        n_bands = 4
        digits, exponent = get_digits(ohms, n_bands - 2)
        digit_1, digit_2 = digits
        note_back += '<div>{}{}&times;10<sup>{}</sup></div>'.format(digit_1, digit_2, exponent)
    note_back += '<div>{}</div>'.format(idiomatic_name(ohms))
    if tolerance is not None:
        note_back += '<div>&plusmn;{}</div>'.format(tolerance)
    if mirror:
        note_back += '<div>(mirrored)</div>'
    return note_front, note_back

def get_svg_filename(ohms, tolerance=None, mirror=False):
    if tolerance is None:
        # Probably a 0 Ohm resistor.
        return "resistor_{ohm:013.3f}Ohm.svg".format(ohm=ohms, tol=tolerance)
    if mirror:
        return "resistor_mirrored_{ohm:013.3f}Ohm_{tol}.svg".format(ohm=ohms, tol=tolerance)
    else:
        return "resistor_{ohm:013.3f}Ohm_{tol}.svg".format(ohm=ohms, tol=tolerance)

def write_resistor(outdir, fp_tsv, ohm, tol, mirror=False):
    filename = get_svg_filename(ohm, tol, mirror)
    filepath = os.path.join(outdir, filename)
    with open(filepath, 'w') as fp:
        write_svg(fp, ohms=ohm, tolerance=tol, mirror=mirror)

    front, back = get_anki_note(filename, ohms=ohm, tolerance=tol, mirror=mirror)
    fp_tsv.write('{}\t{}\n'.format(front, back))

def write_series(outdir, fp_tsv, series, mirror=False):
    # We go from -2 to 10 instead of -3 to 9
    # since E12 series use 1.0 <= x < 10,
    # but resistor color code uses 10 <= x < 100
    for i in range(-2, 11):
        for val in series:
            digits, tol = val
            if i > 0:
                ohm = decimal.Decimal(digits)*10**i
            else:
                ohm = decimal.Decimal(digits)/10**-i
            write_resistor(outdir, fp_tsv, ohm, tol, mirror)

def writable_directory(path):
    if not os.path.isdir(path):
        raise argparse.ArgumentTypeError(
            'not an existing directory: {}'.format(path))
    if not os.access(path, os.W_OK):
        raise argparse.ArgumentTypeError(
            'not a writable directory: {}'.format(path))
    return path

if __name__ == '__main__':
    import argparse
    import os.path
    parser = argparse.ArgumentParser(
        description='Generate SVGs of resistors.'
    )
    parser.add_argument(
        'out_dir',
        type=writable_directory,
        help='Target directory for SVGs',
    )
    parser.add_argument(
        'tsvfile',
        type=argparse.FileType('w'),
        help='TSV file for import into Anki deck',
    )
    args = parser.parse_args()

    write_resistor(args.out_dir, args.tsvfile, ohm=decimal.Decimal(0), tol=None)
    write_series(args.out_dir, args.tsvfile, E6_series)
    write_series(args.out_dir, args.tsvfile, E6_series, mirror=True)
    write_series(args.out_dir, args.tsvfile, E12_series)
    write_series(args.out_dir, args.tsvfile, E12_series, mirror=True)
    write_series(args.out_dir, args.tsvfile, E24_series)
    write_series(args.out_dir, args.tsvfile, E24_series, mirror=True)
