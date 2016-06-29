"""Parse QR codes using zbar."""

from subprocess import Popen, PIPE

def zbar(fpath):
    """Return stdout and stderr from zbarimg."""
    process = Popen(["zbarimg", fpath], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    return stdout, stderr, process.returncode


if __name__ == "__main__":
    import sys
    print zbar(sys.argv[1])
