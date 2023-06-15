class RequestParse:

    def __init__(self, data: bytes):
        self.data = data.decode('utf-8').split('\r\n\r\n')
        if len(self.data) > 1:
            start_headers, self.body = self.data
        else:
            start_headers, self.body = self.data[0], None
        start_headers_list = start_headers.split('\r\n')
        self.start_line = start_headers_list.pop(0)
        self.headers = start_headers_list

    def parse_starline(self) -> tuple:
        method, path, protocol = self.start_line.split(' ')
        if '?' in path:
            path, qs = path.split('?')
        else:
            qs = ''
        return method, path, qs, protocol

    def parse_headers(self) -> dict:
        headers_dict = dict()
        for header in self.headers:
            k, v = header.split(': ')
            headers_dict.update({k.upper(): v})
        return headers_dict

    def parse_body(self) -> str:
        if self.body is not None:
            return self.body
        return ''

