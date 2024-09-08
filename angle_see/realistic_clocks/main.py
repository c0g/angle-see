import argparse
from datetime import datetime
from clock_generator import generate_clock_image
from clock_designs import AVAILABLE_DESIGNS

def parse_time(time_str):
    try:
        return datetime.strptime(time_str, "%I:%M %p")
    except ValueError:
        try:
            return datetime.strptime(time_str, "%H:%M")
        except ValueError:
            raise ValueError("Invalid time format. Use 'HH:MM' or 'HH:MM AM/PM'")

def main():
    parser = argparse.ArgumentParser(description="Generate a customizable analogue clock image")
    parser.add_argument("time", help="Time to display on the clock (e.g., '3:30 PM' or '15:30')")
    parser.add_argument("--design", choices=AVAILABLE_DESIGNS, default="classic", help="Clock face design")
    parser.add_argument("--face-color", default="#FFFFFF", help="Clock face color (hex code)")
    parser.add_argument("--hand-color", default="#000000", help="Clock hand color (hex code)")
    parser.add_argument("--output", default="clock.png", help="Output file name")

    args = parser.parse_args()

    try:
        time = parse_time(args.time)
        generate_clock_image(time, args.design, args.face_color, args.hand_color, args.output)
        print(f"Clock image generated: {args.output}")
    except ValueError as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
