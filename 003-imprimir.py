import cv2
import numpy as np
import os
from datetime import datetime, timedelta

# Ensure the "render" folder exists
os.makedirs("render", exist_ok=True)

# Video properties
width, height = 1920, 1080
fps = 60
duration = 10  # 1 hour in seconds
output_file = "render/countdown_timer.mp4"

# Create a VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

# Define font and color for the text
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 4
font_color = (255, 255, 255)  # White color
thickness = 8

# Smaller font for statistics
font_scale_small = 1.5
thickness_small = 3

# Create a black background image
background = np.zeros((height, width, 3), dtype=np.uint8)

# Calculate the total number of frames
total_frames = duration * fps

# Start time
start_time = datetime.now()

for frame_count in range(total_frames):
    # Calculate the current time in seconds
    second = frame_count // fps
    remaining_frames = total_frames - frame_count

    # Calculate the time in HH:MM:SS format
    hours = second // 3600
    minutes = (second % 3600) // 60
    seconds = second % 60
    time_str = f"{hours:02}:{minutes:02}:{seconds:02}"

    # Calculate statistics every 60 frames
    if frame_count % 60 == 0:
        time_passed = timedelta(seconds=second)
        time_remaining = timedelta(seconds=(duration - second))
        percentage_complete = (frame_count / total_frames) * 100
        estimated_finish = start_time + timedelta(seconds=duration)
        
        stats_str = (
            f"Time Passed: {time_passed}\n"
            f"Time Remaining: {time_remaining}\n"
            f"Estimated Finish: {estimated_finish.strftime('%H:%M:%S')}\n"
            f"Completion: {percentage_complete:.2f}%"
        )
        
        # Print statistics to the console
        print(f"Frame: {frame_count}/{total_frames}")
        print(stats_str)
        print('-' * 40)

    # Create a copy of the background
    frame = background.copy()

    # Draw the countdown timer
    text_size = cv2.getTextSize(time_str, font, font_scale, thickness)[0]
    text_x = (width - text_size[0]) // 2
    text_y = (height + text_size[1]) // 2
    cv2.putText(frame, time_str, (text_x, text_y), font, font_scale, font_color, thickness)

    # Draw the statistics on the frame
    y_offset = 100  # Starting y position for statistics
    for i, line in enumerate(stats_str.split('\n')):
        cv2.putText(frame, line, (50, y_offset + i * 50), font, font_scale_small, font_color, thickness_small)

    # Write the frame to the video
    out.write(frame)

# Release the video writer
out.release()

print("Video creation complete and saved in the 'render' folder!")
