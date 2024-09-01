import math

from PIL import Image, ImageDraw


def generate_line_intersection_image(
    angle_degrees,
    line_thickness=5,
    line_color=(255, 0, 0),
    background_color=(255, 255, 255),  # White
    resolution=512,
    draw_angle_arc=True,
    arc_color=(0, 0, 255),  # Blue
    arc_thickness=2,
):
    # Create a new image with the specified background color
    image = Image.new("RGB", (resolution, resolution), background_color)
    draw = ImageDraw.Draw(image)

    # Calculate the center of the image
    center = resolution // 2

    # Convert angle to radians
    angle_radians = math.radians(angle_degrees)

    # Calculate the endpoints of the lines
    line1_start = (center, center)
    line1_end = (center + 200, center)

    # Calculate the next line
    line2_start = (center, center)
    line2_end = (
        center + 200 * math.cos(angle_radians),
        center - 200 * math.sin(angle_radians),
    )
    # import pdb; pdb.set_trace()

    # # Draw the lines
    draw.line([line1_start, line1_end], fill=line_color, width=line_thickness)
    draw.line([line2_start, line2_end], fill=line_color, width=line_thickness)

    # # Draw the angle arc if requested
    if draw_angle_arc:
        arc_radius = resolution // 8  # Increased radius for better visibility
        arc_bbox = [
            center - arc_radius,
            center - arc_radius,
            center + arc_radius,
            center + arc_radius,
        ]
        # Draw arc from 0 to the specified angle
        draw.arc(arc_bbox, -angle_degrees, 0, fill=arc_color, width=arc_thickness)

    return image


if __name__ == "__main__":
    img = generate_line_intersection_image(angle_degrees=293, draw_angle_arc=True)
    img.show()
