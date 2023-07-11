from framework.fw.request import Request


class Message:

    @staticmethod
    def success(request, msg: str):
        msg = f'<h4 id="success-message">{msg}</h4>'
        request.extra['message'] = msg

    @staticmethod
    def warning(request, msg: str):
        msg = f'<h4 id="warning-message">{msg}</h4>'
        request.extra['message'] = msg


message = Message()
