from app.post.model import Post
from framework.fw.context_manager import add_context_manager
from framework.fw.request import Request


@add_context_manager
def post_context_manager(context: dict, request: Request):
    footer_post = Post.objects.limit(3)
    context.update({'footer_post': footer_post})