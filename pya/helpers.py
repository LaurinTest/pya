"""Collection of small helper functions"""

import numpy as np
import pyaudio
import simpleaudio as sa
from pya.pyaudiostream import PyaudioStream

class _error(Exception):
    pass

def record(dur=2, channels=1, rate=44100, chunk=256):
    """Record audio

    (if you implement the for loop as a callback and put it to stream_callback = _,
        if will be a non-blocking way. )

    Keyword Arguments:
        dur {int} -- Duration (default: {2})
        channels {int} -- Number of channels (default: {1})
        rate {int} -- Audio sample rate (default: {44100})
        chunk {int} -- Chunk size (default: {256})

    Returns:
        ndarray -- Recorded signal
    """
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=channels, rate=rate, input=True,
                    output=True, frames_per_buffer=chunk)
    buflist = []
    for _ in range(0, int(rate/chunk*dur)):
        data = stream.read(chunk)
        buflist.append(data)
    stream.stop_stream()
    stream.close()
    p.terminate()
    return np.frombuffer(b''.join(buflist), dtype=np.int16)


def _play_with_pyaudio(seg, channels = 1,  format = pyaudio.paInt16):
    # Need to turn seg in to sig 
    # channels: 1 mono, 2 stereo, n -> n channels. 
    p = pyaudio.PyAudio()
    stream = p.open(format=format,
                    channels=channels,
                    rate=seg.frame_rate,
                    output=True)

    # break audio into half-second chunks (to allows keyboard interrupts)
    for chunk in make_chunks(seg, 500):
        stream.write(chunk._data)

    stream.stop_stream()
    stream.close()

    p.terminate()

def make_chunks(audio_segment, chunk_length):
    """
    Breaks an AudioSegment into chunks that are <chunk_length> milliseconds
    long.
    if chunk_length is 50 then you'll get a list of 50 millisecond long audio
    segments back (except the last one, which can be shorter)
    """
    number_of_chunks = ceil(len(audio_segment) / float(chunk_length))
    return [audio_segment[i * chunk_length:(i + 1) * chunk_length]
            for i in range(int(number_of_chunks))]

# This part uses pyaudio for playing. 
def playpyaudio(sig, num_channels=1, sr=44100, bs = 512, block=False):
    try:
        audiostream = PyaudioStream(bs = bs, sr =sr)
        audiostream.play(sig)

    except ImportError:
        raise ImportError("Can't play audio via Pyaudiostream")
    else:
        return
  
def play(sig, num_channels=1, sr=44100, block=False):
    """Plays audio signal via simpleaudio

    Arguments:
        sig {iterable} -- Signal to be played

    Keyword Arguments:
        num_channels {int} -- Number of channels (default: {1})
        sr {int} -- Audio sample rate (default: {44100})
        block {bool} -- if True, block until playback is finished
                        (default: {False})

    Returns:
        simpleaudio play_obj -- see description in simpleaudio
    """
    play_obj = sa.play_buffer((32767*sig).astype(np.int16), num_channels=num_channels, 
                              bytes_per_sample=2, sample_rate=sr)
    if block:
        play_obj.wait_done() # wait for playback to finish before returning
    return play_obj



def linlin(x, smi, sma, dmi, dma):
    """TODO

    Arguments:
        x {float} -- [description]
        smi {float} -- [description]
        sma {float} -- [description]
        dmi {float} -- [description]
        dma {float} -- [description]

    Returns:
        float -- [description]
    """

    return (x-smi)/(sma-smi)*(dma-dmi) + dmi


def midicps(m):
    """TODO

    Arguments:
        m {int} -- [description]

    Returns:
        float -- [description]
    """

    return 440.0*2**((m-69)/12.0)


def cpsmidi(c):
    """TODO

    Arguments:
        c {float} -- [description]

    Returns:
        float -- [description]
    """

    return 69+12*np.log2(c/440.0)


def clip(value, minimum=-float("inf"), maximum=float("inf")):
    """Clips a value to a certain range

    Arguments:
        value {float} -- Value to clip

    Keyword Arguments:
        minimum {float} -- Minimum value output can take
                           (default: {-float("inf")})
        maximum {float} -- Maximum value output can take
                            (default: {float("inf")})

    Returns:
        float -- clipped value
    """

    if value < minimum:
        return minimum
    if value > maximum:
        return maximum
    return value


def dbamp(db):
    """TODO

    Arguments:
        db {[type]} -- [description]

    Returns:
        [type] -- [description]
    """

    return 10**(db/20.0)


def ampdb(amp):
    """TODO

    Arguments:
        amp {[type]} -- [description]

    Returns:
        [type] -- [description]
    """

    return 20*np.log10(amp)
