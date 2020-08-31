"""
Replaces the audio of a video file with an external audio file, and syncronises
the audio file with the original video file audio.
"""
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.editor import VideoFileClip
import numpy as np
from scipy import signal

audio_fn = "blackbird.wav"
video_fn = "blackbird.mp4"
out_fn = None  # "out.mp4"


def calculate_time_offset(a, b, fs):
    """
    Calculates the time offset of two signals by performing a cross correlation
    analysis. Assumes both signals have the same sampling frequency.
    args:
        a (1D array): first signal.
        b (1D array): second signal.
        fs (float): Sampling frequency of signals.
    returns:
        offset (float): The time offset in seconds. Positive offset means a lags
        behind b.
        max_corr (float): The Pearson correlation coefficient of the two signals
        at the optimal time offset.
    """
    a = np.reshape(a, (-1))
    b = np.reshape(b, (-1))
    corr = signal.correlate(a - a.mean(), b - b.mean(), mode="full")
    corr /= len(b) * a.std() * b.std()

    lag = np.arange(0, len(corr)) - (len(b) - 1)

    offset = lag[corr.argmax()]
    max_corr = corr.max()
    return offset / fs, max_corr


def AVsync(audio_fn, video_fn, offset=None, verbose=False):
    audio = AudioFileClip(audio_fn)
    video = VideoFileClip(video_fn)

    if offset is None:
        x1 = audio.to_soundarray()
        x2 = video.audio.to_soundarray()
        offset, corr = calculate_time_offset(x1[:, 0], x2[:, 0], fs=44100)
        if verbose:
            print(f"Offset: {offset:2.3f}s\nCorrelation: {corr*100:2.2f}%")

    if offset > 0:
        video_out = video.set_audio(audio.subclip(offset))
    else:
        video_out = video.subclip(-offset).set_audio(audio)

    return video_out


if __name__ == "__main__":

    video_out = AVsync(audio_fn, video_fn, verbose=True)
    if out_fn:
        video_out.write_videofile(out_fn)
