import cairo
import math

def draw_minimalist_clock(ctx, width, height, face_color):
    center_x, center_y = width / 2, height / 2
    radius = min(width, height) * 0.45

    # Draw clock face
    ctx.arc(center_x, center_y, radius, 0, 2 * math.pi)
    ctx.set_source_rgb(*hex_to_rgb(face_color))
    ctx.fill()

    # Draw hour markers
    for i in range(12):
        angle = i * math.pi / 6
        x = center_x + radius * 0.9 * math.cos(angle)
        y = center_y + radius * 0.9 * math.sin(angle)
        
        ctx.arc(x, y, 5, 0, 2 * math.pi)
        ctx.set_source_rgb(0.2, 0.2, 0.2)
        ctx.fill()

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) / 255 for i in (0, 2, 4))
