import cv2
import numpy as np
import os
import keyboard  # New import for detecting key presses from the console
from datetime import datetime, timedelta

# List of available fonts in OpenCV
fonts = [
    cv2.FONT_HERSHEY_SIMPLEX,
    cv2.FONT_HERSHEY_PLAIN,
    cv2.FONT_HERSHEY_DUPLEX,
    cv2.FONT_HERSHEY_COMPLEX,
    cv2.FONT_HERSHEY_TRIPLEX,
    cv2.FONT_HERSHEY_COMPLEX_SMALL,
    cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
    cv2.FONT_HERSHEY_SCRIPT_COMPLEX,
]

# Ensure the "render" folder exists
os.makedirs("render", exist_ok=True)

# Loop through each font and create two versions of the video
for font_index, font in enumerate(fonts):
    for hora in range(1, 11):
        for variant in ["light_bg", "dark_bg"]:
            # Video properties
            width, height = 1920, 1080
            fps = 60
            duration = 3600 * hora  # Duration in seconds for each hour

            # Determine background and font colors based on variant
            if variant == "light_bg":
                background_color = (255, 255, 255)  # White background
                font_color = (0, 0, 0)  # Black font
            else:
                background_color = (0, 0, 0)  # Black background
                font_color = (255, 255, 255)  # White font

            output_file = f"render/countdown_timer_{duration // 3600}h_font_{font_index}_{variant}.mp4"

            # Create a VideoWriter object
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

            # Define a smaller font scale and thickness for the text
            font_scale = 4  # Smaller text for the countdown
            thickness = 8  # Slightly reduced thickness for countdown

            # Create a background image
            background = np.full((height, width, 3), background_color, dtype=np.uint8)

            # Ring properties
            center = (width // 2, height // 2)
            outer_radius = int((height / 2) * 0.9)  # Outer ring radius
            ring_thickness = 20

            # Calculate the total number of frames
            total_frames = duration * fps

            # Start time
            start_time = datetime.now()

            for frame_count in range(total_frames):
                # Check if the Escape key is pressed via the console
                if keyboard.is_pressed("esc"):  # Check if "Escape" is pressed
                    print("Escape key pressed. Terminating the video creation process.")
                    out.release()
                    exit()

                # Calculate the remaining time in seconds
                remaining_seconds = duration - (frame_count // fps)
                
                # Calculate the time in HH:MM:SS format
                hours = remaining_seconds // 3600
                minutes = (remaining_seconds % 3600) // 60
                seconds = remaining_seconds % 60
                time_str = f"{hours:02}:{minutes:02}:{seconds:02}"

                # Calculate angles for the rings (full circle is 360 degrees)
                hour_angle = int(360 * (hours / (hora if hora <= 24 else 24)))
                minute_angle = int(360 * (minutes / 60))
                second_angle = int(360 * (seconds / 60))

                # Create a copy of the background
                frame = background.copy()

                # Draw the hour ring (Red)
                cv2.ellipse(frame, center, (outer_radius, outer_radius), 0, 0, hour_angle, (0, 0, 255), ring_thickness)

                # Draw the minute ring (Green)
                cv2.ellipse(frame, center, (outer_radius - ring_thickness * 2, outer_radius - ring_thickness * 2), 0, 0, minute_angle, (0, 255, 0), ring_thickness)

                # Draw the second ring (Blue)
                cv2.ellipse(frame, center, (outer_radius - ring_thickness * 4, outer_radius - ring_thickness * 4), 0, 0, second_angle, (255, 0, 0), ring_thickness)

                # Center the countdown timer on the entire image
                text_size = cv2.getTextSize(time_str, font, font_scale, thickness)[0]
                text_x = center[0] - text_size[0] // 2
                text_y = center[1] + text_size[1] // 2

                # Draw the countdown timer centered on the image
                cv2.putText(frame, time_str, (text_x, text_y), font, font_scale, font_color, thickness)

                # Calculate and print statistics every 60 frames
                if frame_count % 60 == 0:
                    time_passed = timedelta(seconds=(duration - remaining_seconds))
                    time_remaining = timedelta(seconds=remaining_seconds)
                    percentage_complete = (frame_count / total_frames) * 100
                    estimated_finish = start_time + timedelta(seconds=remaining_seconds)

                    stats_str = (
                        f"Time Passed: {time_passed}\n"
                        f"Time Remaining: {time_remaining}\n"
                        f"Estimated Finish: {estimated_finish.strftime('%H:%M:%S')}\n"
                        f"Completion: {percentage_complete:.2f}%"
                    )

                    # Print statistics to the console
                    print(f"Font {font_index}, Variant {variant}, Frame: {frame_count}/{total_frames}")
                    print(stats_str)
                    print('-' * 40)

                # Write the frame to the video
                out.write(frame)

            # Release the video writer
            out.release()

            print(f"Video creation complete and saved in the 'render' folder! Font {font_index}, Duration: {duration // 3600}h, Variant: {variant}")
