import click
from .avsync import AVsync


@click.command()
@click.argument("video_fn", type=click.Path(exists=True))
@click.argument("audio_fn", type=click.Path(exists=True))
@click.argument("out_fn", type=click.Path())
def cli(video_fn, audio_fn, out_fn):
    video_out = AVsync(audio_fn, video_fn, verbose=True)

    if click.confirm("Do you want to continue?"):
        video_out.write_videofile(out_fn)
