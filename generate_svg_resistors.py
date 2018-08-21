#! /usr/bin/env python3

import argparse
import decimal

svg_width=400
svg_height=200
body_width  = int(svg_width  * 3/4)
body_height = int(svg_height * 1/2)
margin_x = int((svg_width  - body_width ) * 1/2)
margin_y = int((svg_height - body_height) * 1/2)

preamble = f"""
<svg version="1.1"
     baseProfile="full"
     width="{svg_width}" height="{svg_height}"
     xmlns="http://www.w3.org/2000/svg">
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

def get_resistor_bands(ohms_raw, tolerance="20%", n_bands=4, mirrored=False):
    assert ohms_raw > 0
    assert n_bands in (4, 5, 6)
    if n_bands != 4:
        raise NotImplementedError
    if mirrored:
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
        7 : "violet",
        8 : "gray",
        9 : "white",
    }
    multiplier_color = {
        decimal.Decimal(1)/10**3 : "pink",
        decimal.Decimal(1)/10**2 : "url(#silverbad)",
        decimal.Decimal(1)/10**1 : "url(#goldband)",
        decimal.Decimal(1)*10**0 : "black",
        decimal.Decimal(1)*10**1 : "brown",
        decimal.Decimal(1)*10**2 : "red",
        decimal.Decimal(1)*10**3 : "orange",
        decimal.Decimal(1)*10**4 : "yellow",
        decimal.Decimal(1)*10**5 : "green",
        decimal.Decimal(1)*10**6 : "blue",
        decimal.Decimal(1)*10**7 : "violet",
        decimal.Decimal(1)*10**8 : "gray",
        decimal.Decimal(1)*10**9 : "white",
    }
    tolerance_color = {
        "20%"   : None,
        "10%"   : "url(#silverbad)",
        "5%"    : "url(#goldband)",
        "1%"    : "brown",
        "2%"    : "red",
        "0.05%" : "orange",
        "0.02%" : "yellow",
        "0.5%"  : "green",
        "0.25%" : "blue",
        "0.1%"  : "violet",
        "0.01%" : "gray",
    }
    sign, digits, exponent = ohms.as_tuple()
    digit_1 = digits[0]
    assert digit_1 in digit_color
    try:
        digit_2 = digits[1]
    except IndexError:
        digit_2 = 0
    assert digit_2 in digit_color
    multiplier = ohms / decimal.Decimal(digit_1*10 + digit_2)
    assert multiplier in multiplier_color
    band_color_1 = digit_color[digit_1]
    band_color_2 = digit_color[digit_2]
    band_color_3 = multiplier_color[multiplier]
    band_color_4 = tolerance_color[tolerance]
    svg = ''
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

def write_svg(fp, ohms, tolerance):
    svg = ''
    svg += preamble
    svg += get_wire()
    svg += get_resistor_body()
    svg += get_resistor_bands(ohms, tolerance)
    svg += postamble
    fp.write(svg)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generate SVGs of resistors.'
    )
    parser.add_argument(
        'svg_file',
        type=argparse.FileType('w'),
        help='SVG filepath',
    )
    args = parser.parse_args()

    write_svg(args.svg_file, ohms=1000, tolerance="5%")
