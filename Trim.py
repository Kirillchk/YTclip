import os
from moviepy.video.io.VideoFileClip import VideoFileClip


def trim_video(input_file_path, output_file, start_time, end_time):
    print(f"Trimming video from: {input_file_path}")
    print(f"Trimming from: {start_time, end_time}")

    # Check if input file exists
    if not os.path.exists(input_file_path):
        raise FileNotFoundError(f"The file '{input_file_path}' does not exist. Please check the path.")

    print(f"Saving trimmed video to: {output_file}")

    # Convert (hours, minutes, seconds) to seconds
    def time_to_seconds(t):
        return t[0] * 3600 + t[1] * 60 + t[2]

    start_seconds = time_to_seconds(start_time)
    end_seconds = time_to_seconds(end_time)

    # Load the video file and trim
    with VideoFileClip(input_file_path) as video:
        trimmed_video = video.subclip(start_seconds, end_seconds)

        # Write the output to a new file
        trimmed_video.write_videofile(output_file, codec='libx264', audio_codec='aac')

    print("Video trimming completed and file saved.")


