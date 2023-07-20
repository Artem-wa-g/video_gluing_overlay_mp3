import argparse
import os
import random
from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip, CompositeAudioClip


def get_random_file(directory) -> str:
    files = os.listdir(directory)
    while True:
        file = random.choice(files)
        if file.endswith(".mp4"):
            return file


def trim_video(video_file, time):
    clip = VideoFileClip(video_file).subclip(t_end=time)
    return clip.without_audio()


def merge_videos(video1, video2):
    final_clip = concatenate_videoclips([video1, video2], method='compose')
    return final_clip


def add_audio(video, audio_file, time):
    audioclip = AudioFileClip(audio_file).subclip(t_end=time * 2)
    new_audioclip = CompositeAudioClip([audioclip])
    video.audio = new_audioclip
    return video


def save_video(video, output_file) -> None:
    video.write_videofile(output_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f1", "--folder1", help="Path to first folder")
    parser.add_argument("-f2", "--folder2", help="Path to second folder")
    parser.add_argument("-m", "--music", help="Path to music file")
    parser.add_argument("-t", "--time", help="Pruning time")

    args = parser.parse_args()
    folder1 = args.folder1
    folder2 = args.folder2
    music_file = args.music
    time = args.time

    random_video1 = get_random_file(folder1)
    random_video2 = get_random_file(folder2)

    video1 = trim_video(os.path.join(folder1, random_video1), time)
    video2 = trim_video(os.path.join(folder2, random_video2), time)

    merged_video = merge_videos(video1, video2)

    final_video = add_audio(merged_video, music_file, time)

    output_file = "result.mp4"
    save_video(merged_video, output_file)
