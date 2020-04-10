import io
import json


def read_until(file_descriptor, char):
    start = True
    res = ""
    next_char = " "
    while (start or res[-1] != char) and len(next_char):
        start = False
        next_char = file_descriptor.read(1)
        res += next_char
    return char in res


def json_stream(fp):
    while True:
        has_next = read_until(fp, "{")
        if not has_next:
            break
        bracers = {"{": 1, "}": 0}
        item = "{"
        while bracers["{"] != bracers["}"]:
            item += fp.read(1)
            last_char = item[-1]
            if last_char in ["{", "}"]:
                bracers[last_char] = bracers[last_char] + 1
        yield json.loads(item)


def json_stream_from_request(response):
    try:
        for o in json_stream(
            FileFromGenerator(response.iter_content(decode_unicode=True, chunk_size=1))
        ):
            yield o
    except StopIteration:
        return None


class FileFromGenerator:
    def __init__(self, generator):
        self.generator = generator
        self.buffer = io.StringIO()
        self.len = 0

    def read(self, n):
        if n != 1:
            raise NotImplemented
        res = self.buffer.read(1)
        while len(res) < 1:
            try:
                next_chunk = next(self.generator).decode()
            except StopIteration:
                next_chunk = ""
            self.buffer.write(next_chunk)
            self.len += len(next_chunk)
            self.buffer.seek(self.len - len(next_chunk))
            res += self.buffer.read(1)
        return res
