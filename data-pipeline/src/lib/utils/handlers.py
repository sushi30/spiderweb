from logging import warning


def iteration_handler(iterator, handler, error_callback=None):
    total = 0
    success = 0
    for item in iterator:
        total += 1
        try:
            handler(item)
            success += 1
        except Exception as err:
            warning(err)
            error_callback()
    return success, total
