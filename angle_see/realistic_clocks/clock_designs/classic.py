import cairo
import math

def draw_classic_clock(ctx, width, height, face_color):
    center_x, center_y = width / 2, height / 2
    radius = min(width, height) * 0.45

    # Draw clock face
    ctx.arc(center_x, center_y, radius, 0, 2 * math.pi)
    ctx.set_source_rgb(*hex_to_rgb(face_color))
    ctx.fill_preserve()
    ctx.set_source_rgb(0, 0, 0)
    ctx.set_line_width(10)
    ctx.stroke()

    # Draw hour markers
    for i in range(12):
        angle = i * math.pi / 6
        outer_x = center_x + radius * 0.9 * math.cos(angle)
        outer_y = center_y + radius * 0.9 * math.sin(angle)
        inner_x = center_x + radius * 0.8 * math.cos(angle)
        inner_y = center_y + radius * 0.8 * math.sin(angle)
        
        ctx.move_to(outer_x, outer_y)
        ctx.line_to(inner_x, inner_y)
        ctx.set_line_width(8)
        ctx.stroke()

    # Draw minute markers
    for i in range(60):
        if i % 5 != 0:
            angle = i * math.pi / 30
            outer_x = center_x + radius * 0.95 * math.cos(angle)
            outer_y = center_y + radius * 0.95 * math.sin(angle)
            inner_x = center_x + radius * 0.9 * math.cos(angle)
            inner_y = center_y + radius * 0.9 * math.sin(angle)
            
            ctx.move_to(outer_x, outer_y)
            ctx.line_to(inner_x, inner_y)
            ctx.set_line_width(3)
            ctx.stroke()

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) / 255 for i in (0, 2, 4))
