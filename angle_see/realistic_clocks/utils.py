import math
import cairo

def draw_clock_hands(ctx, width, height, time, hand_color):
    center_x, center_y = width / 2, height / 2
    radius = min(width, height) * 0.45

    hour = time.hour % 12
    minute = time.minute

    # Calculate angles
    hour_angle = (hour + minute / 60) * (math.pi / 6) - math.pi / 2
    minute_angle = minute * (math.pi / 30) - math.pi / 2

    # Draw hour hand
    hour_length = radius * 0.5
    hour_x = center_x + hour_length * math.cos(hour_angle)
    hour_y = center_y + hour_length * math.sin(hour_angle)
    ctx.move_to(center_x, center_y)
    ctx.line_to(hour_x, hour_y)
    ctx.set_source_rgb(*hex_to_rgb(hand_color))
    ctx.set_line_width(12)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.stroke()

    # Draw minute hand
    minute_length = radius * 0.7
    minute_x = center_x + minute_length * math.cos(minute_angle)
    minute_y = center_y + minute_length * math.sin(minute_angle)
    ctx.move_to(center_x, center_y)
    ctx.line_to(minute_x, minute_y)
    ctx.set_source_rgb(*hex_to_rgb(hand_color))
    ctx.set_line_width(8)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.stroke()

    # Draw center dot
    ctx.arc(center_x, center_y, 8, 0, 2 * math.pi)
    ctx.set_source_rgb(*hex_to_rgb(hand_color))
    ctx.fill()

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) / 255 for i in (0, 2, 4))
