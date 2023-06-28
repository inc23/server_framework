class RequestLineHeadersParse:

    def __init__(self, start_headers: bytes):
        start_headers_list = start_headers.decode('utf-8').split('\r\n')
        self._start_line = start_headers_list.pop(0)
        self._headers = start_headers_list

    def parse_starline(self) -> tuple:
        method, path, protocol = self._start_line.split(' ')
        if '?' in path:
            path, qs = path.split('?')
        else:
            qs = ''
        return method, path, qs, protocol

    def parse_headers(self) -> dict:
        headers_dict = dict()
        for header in self._headers:
            k, v = header.split(': ')
            k: str = k.replace('-', '_')
            headers_dict.update({k.upper(): v})
        return headers_dict
