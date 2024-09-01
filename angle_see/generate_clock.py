import math

from PIL import Image, ImageDraw


def draw_clock(
    resolution,
    hour_hand_length,
    minute_hand_length,
    hour_color,
    minute_color,
    hour,
    minute,
):
    # Create a blank image
    radius = resolution // 2
    image = Image.new("RGB", (radius * 2 + 10, radius * 2 + 10), (255, 255, 255))
    draw = ImageDraw.Draw(image)

    # Draw the clock face
    draw.ellipse(
        (radius - radius, radius - radius, radius + radius, radius + radius),
        outline=(0, 0, 0),
    )

    # Draw the hour markers
    for i in range(12):
        angle = i * 30
        x = radius * 0.7 * math.cos(math.radians(angle))
        y = radius * 0.7 * math.sin(math.radians(angle))
        draw.line(
            (radius + 0.7 * x, radius + 0.7 * y, radius + x, radius + y),
            fill=(0, 0, 0),
            width=2,
        )

    # Draw the hour hand
    hour_angle = (hour * 30) + (minute * 0.5)
    hour_x = radius + hour_hand_length * math.cos(math.radians(hour_angle - 90))
    hour_y = radius + hour_hand_length * math.sin(math.radians(hour_angle - 90))
    draw.line((radius, radius, hour_x, hour_y), fill=hour_color, width=8)

    # Draw the minute hand
    minute_angle = minute * 6
    minute_x = radius + minute_hand_length * math.cos(math.radians(minute_angle - 90))
    minute_y = radius + minute_hand_length * math.sin(math.radians(minute_angle - 90))
    draw.line((radius, radius, minute_x, minute_y), fill=minute_color, width=4)

    return image


# Example usage
if __name__ == "__main__":
    image = draw_clock(
        resolution=512,
        hour_hand_length=100,
        minute_hand_length=200,
        hour_color=(255, 0, 0),
        minute_color=(0, 0, 255),
        hour=6,
        minute=37,
    )
    # show interactively
    image.show()
