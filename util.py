import sys
import traceback


def _get_exception_msg():
    return "".join(traceback.format_exception(*sys.exc_info()))
