import subprocess

def generate_clock_image(time, design, face_color, hand_color, output):
    command = [
        "python", "main.py",
        time,
        "--design", design,
        "--face-color", face_color,
        "--hand-color", hand_color,
        "--output", output
    ]
    subprocess.run(command, check=True)

def main():
    examples = [
        ("3:30 PM", "classic", "#FFFFFF", "#000000", "classic_clock.png"),
        ("9:45 AM", "modern", "#E0E0FF", "#000080", "modern_clock.png"),
        ("6:00 PM", "minimalist", "#F0F0F0", "#333333", "minimalist_clock.png"),
        ("12:15 AM", "vintage", "#FFF8DC", "#8B4513", "vintage_clock.png"),
        ("7:30 AM", "classic", "#FFE4B5", "#4B0082", "custom_classic_clock.png"),
        ("2:45 PM", "numbered", "#F5F5DC", "#2F4F4F", "numbered_clock.png"),
        ("8:00 AM", "roman", "#FFF0F5", "#800000", "roman_clock.png"),
    ]

    for time, design, face_color, hand_color, output in examples:
        print(f"Generating {output}...")
        generate_clock_image(time, design, face_color, hand_color, output)
        print(f"{output} generated successfully.")

if __name__ == "__main__":
    main()
