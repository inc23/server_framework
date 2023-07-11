from framework.fw.view.redirect import redirect


class UserCheckMixin:

    url_if_denied = None

    def dispatch(self):
        if not self.request.user:
            return redirect(self.request, self.url_if_denied)
        return super(UserCheckMixin, self).dispatch()


class AdminCheckMixin:

    url_if_denied = None

    def dispatch(self):
        if not self.request.user or not self.request.user.is_admin:
            return redirect(self.request, self.url_if_denied)
        return super(UserCheckMixin, self).dispatch()


class AuthorCheckMixin:

    url_if_denied = None

    def dispatch(self):
        if not self.request.user and not self.get_object.author != self.request.user.id:
            return redirect(self.request, self.url_if_denied)
        return super(AuthorCheckMixin, self).dispatch()