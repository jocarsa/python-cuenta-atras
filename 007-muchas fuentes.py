import cv2
import numpy as np
import os
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

# Loop through each font and create a video
for font_index, font in enumerate(fonts):
    for hora in range(1, 11):
        # Video properties
        width, height = 1920, 1080
        fps = 60
        duration = 3600 * hora  # Duration in seconds for each hour

        output_file = f"render/countdown_timer_{duration // 3600}h_font_{font_index}.mp4"

        # Create a VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

        # Define font color and thickness for the text
        font_scale = 8  # Larger text
        font_color = (255, 255, 255)  # White color
        thickness = 12  # Increased thickness

        # Create a black background image
        background = np.zeros((height, width, 3), dtype=np.uint8)

        # Calculate the total number of frames
        total_frames = duration * fps

        # Start time
        start_time = datetime.now()

        for frame_count in range(total_frames):
            # Calculate the remaining time in seconds
            remaining_seconds = duration - (frame_count // fps)
            
            # Calculate the time in HH:MM:SS format
            hours = remaining_seconds // 3600
            minutes = (remaining_seconds % 3600) // 60
            seconds = remaining_seconds % 60
            time_str = f"{hours:02}:{minutes:02}:{seconds:02}"

            # Calculate statistics every 60 frames
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
                print(f"Font {font_index}, Frame: {frame_count}/{total_frames}")
                print(stats_str)
                print('-' * 40)

            # Create a copy of the background
            frame = background.copy()

            # Draw the countdown timer
            text_size = cv2.getTextSize(time_str, font, font_scale, thickness)[0]
            text_x = (width - text_size[0]) // 2
            text_y = (height + text_size[1]) // 2
            cv2.putText(frame, time_str, (text_x, text_y), font, font_scale, font_color, thickness)

            # Write the frame to the video
            out.write(frame)

        # Release the video writer
        out.release()

        print(f"Video creation complete and saved in the 'render' folder! Font {font_index}, Duration: {duration // 3600}h")
