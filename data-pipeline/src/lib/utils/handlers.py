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
    if total != 0 and success == 0:
        raise Exception("No records were processed successfully")
    return success, total
