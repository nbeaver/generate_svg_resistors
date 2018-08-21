#! /usr/bin/env python3

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

def get_bands(ohms, tolerance, n_bands=4, mirrored=False):
    assert ohms > 0
    assert tolerance > 0
    assert n_bands in (4, 5, 6)
    if n_bands != 4:
        raise NotImplementedError
    if mirrored:
        raise NotImplementedError
    return

def get_band(fill_color, band_position, n_bands = 4, indent_level=2):
    max_width = int(body_width / (n_bands + 1))
    band_width = int((2/3) * max_width)
    band_height = body_height
    x = int(margin_x + max_width*band_position - (band_width / 2))
    y = margin_y
    stroke_width = int(min(svg_width, svg_height)*1/40)
    svg = f'<rect x="{x}"  y="{y}" width="{band_width}" height="{band_height}" fill="{fill_color}" stroke="black" stroke-width="{stroke_width}" />'
    return ' '*indent_level + svg + '\n'

if __name__ == '__main__':
    svg = ''
    svg += preamble
    svg += get_wire()
    svg += get_resistor_body()
    svg += get_band('brown',         1)
    svg += get_band('black',         2)
    svg += get_band('red',           3)
    svg += get_band('url(#goldband)',4)
    svg += postamble
    print(svg)
