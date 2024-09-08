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

# Time intervals for the countdowns
time_intervals = [
    10, 20, 30,  # 10, 20, 30 seconds
    *[60 * i for i in range(1, 11)],  # 1-10 minutes
    *[60 * i for i in range(10, 61, 5)]  # 10-60 minutes (every 5 minutes)
]

# Loop through each font and create versions of the video for each time interval
for font_index, font in enumerate(fonts):
    for duration in time_intervals:
        for variant in ["light_bg", "dark_bg"]:
            # Define the output file path
            output_file = f"render/countdown_timer_{duration}s_font_{font_index}_{variant}.mp4"

            # Check if the file already exists
            if os.path.exists(output_file):
                print(f"File {output_file} already exists. Skipping to next video.")
                continue

            # Video properties
            width, height = 1920, 1080
            fps = 60

            # Determine background and font colors based on variant
            if variant == "light_bg":
                background_color = (255, 255, 255)  # White background
                font_color = (0, 0, 0)  # Black font
            else:
                background_color = (0, 0, 0)  # Black background
                font_color = (255, 255, 255)  # White font

            # Create a VideoWriter object
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

            # Define a smaller font scale and thickness for the text
            font_scale = 4  # Smaller text for the countdown
            thickness = 16  # Slightly reduced thickness for countdown

            # Create a background image
            background = np.full((height, width, 3), background_color, dtype=np.uint8)

            # Ring properties
            center = (width // 2, height // 2)
            outer_radius = int((height / 2) * 0.9)  # Outer ring radius
            ring_thickness = 50

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

                # Calculate the time in MM:SS format (handling hours if needed)
                hours = remaining_seconds // 3600
                minutes = (remaining_seconds % 3600) // 60
                seconds = remaining_seconds % 60
                time_str = f"{hours:02}:{minutes:02}:{seconds:02}" if hours > 0 else f"{minutes:02}:{seconds:02}"

                # Calculate angles for the rings (full circle is 360 degrees)
                if duration >= 3600 and hours > 0:
                    hour_angle = int(360 * (hours / (duration // 3600 if duration // 3600 <= 24 else 24)))
                else:
                    hour_angle = 0  # No hour ring for durations under 1 hour or if hours is 0

                minute_angle = int(360 * (minutes / 60)) if minutes > 0 else 0
                second_angle = int(360 * (seconds / 60)) if seconds > 0 else 0

                # Create a copy of the background
                frame = background.copy()

                # Rotate the rings 90 degrees counterclockwise by adding 90 degrees to the start angle
                start_angle = -90

                # Draw the hour ring (Red) only if duration is 1 hour or more and hours is non-zero
                if hour_angle > 0:
                    cv2.ellipse(frame, center, (outer_radius, outer_radius), start_angle, 0, hour_angle, (0, 0, 255), ring_thickness)

                # Draw the minute ring (Green) only if minutes is non-zero
                if minute_angle > 0:
                    cv2.ellipse(frame, center, (outer_radius - ring_thickness * 2, outer_radius - ring_thickness * 2), start_angle, 0, minute_angle, (0, 255, 0), ring_thickness)

                # Draw the second ring (Blue) only if seconds is non-zero
                if second_angle > 0:
                    cv2.ellipse(frame, center, (outer_radius - ring_thickness * 4, outer_radius - ring_thickness * 4), start_angle, 0, second_angle, (255, 0, 0), ring_thickness)

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

            print(f"Video creation complete and saved in the 'render' folder! Font {font_index}, Duration: {duration} seconds, Variant: {variant}")
