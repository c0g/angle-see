import cairo
from PIL import Image
import io
from angle_see.realistic_clocks.clock_designs import get_clock_design
from angle_see.realistic_clocks.utils import draw_clock_hands

def generate_clock_image(time, design, face_color, hand_color):
    # Set up Cairo surface and context
    width, height = 800, 800
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    ctx = cairo.Context(surface)

    # Clear the background
    ctx.set_source_rgb(1, 1, 1)
    ctx.paint()

    # Get the clock design function
    clock_design_func = get_clock_design(design)

    # Draw the clock face
    clock_design_func(ctx, width, height, face_color)

    # Draw clock hands
    draw_clock_hands(ctx, width, height, time, hand_color)

    # Convert Cairo surface to PIL Image
    buf = io.BytesIO()
    surface.write_to_png(buf)
    buf.seek(0)
    image = Image.open(buf)

    return image

