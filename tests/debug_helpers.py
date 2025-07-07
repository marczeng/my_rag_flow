import time
import signal

class Timeout:
    def __init__(self, seconds: int):
        self.seconds = seconds
        self._old_handler = None

    def _timeout(self, signum, frame):
        raise TimeoutError("operation timed out")

    def __enter__(self):
        self._old_handler = signal.signal(signal.SIGALRM, self._timeout)
        signal.alarm(self.seconds)

    def __exit__(self, exc_type, exc, tb):
        signal.alarm(0)
        if self._old_handler is not None:
            signal.signal(signal.SIGALRM, self._old_handler)


def debug_read2docx(parser, path: str):
    """Wrap ``parser.read2docx`` and print execution timestamps."""
    start = time.time()
    print(f"[debug] read2docx start: {time.strftime('%X', time.localtime(start))}")
    result = parser.read2docx(path)
    end = time.time()
    print(
        f"[debug] read2docx end  : {time.strftime('%X', time.localtime(end))} (took {end - start:.2f}s)"
    )
    return result
