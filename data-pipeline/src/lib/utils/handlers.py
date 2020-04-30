from logging import warning
import traceback


def iteration_handler(iterator, handler, error_callback=None):
    if error_callback is None:

        def error_callback(*args, **kwargs):
            pass

    total = 0
    success = 0
    for item in iterator:
        total += 1
        try:
            handler(item)
            success += 1
        except Exception as err:
            warning(traceback.format_exc())
            error_callback(item)
    if total != 0 and success == 0:
        raise Exception("No records were processed successfully")
    return success, total
