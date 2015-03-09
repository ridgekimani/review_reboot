from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

__author__ = 'm'

PRIVATE_IPS_PREFIX = ('10.', '172.', '192.', )


def get_client_ip(request):
    """get the client ip from the request
    """
    remote_address = request.META.get('REMOTE_ADDR')
    # set the default value of the ip to be the REMOTE_ADDR if available
    # else None
    ip = remote_address
    # try to get the first non-proxy ip (not a private ip) from the
    # HTTP_X_FORWARDED_FOR
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        proxies = x_forwarded_for.split(',')
        # remove the private ips from the beginning
        while (len(proxies) > 0 and
                   proxies[0].startswith(PRIVATE_IPS_PREFIX)):
            proxies.pop(0)
        # take the first ip which is not a private one (of a proxy)
        if len(proxies) > 0:
            ip = proxies[0]

    return ip


class TestCaseEx(TestCase):
    """
    Extended TestCase class with ability to login, logout and some helpers methods
    """
    password = '12345'

    def setUp(self):
        self.root = User.objects.create_superuser('root', 'mailm@mail.ru', self.password)
        self.user = User.objects.create_user('default', 'admin@admin.ru', self.password)

    @staticmethod
    def superuser(fn):
        def _wrapper(self=None):
            self.client.login(username=self.root.username, password=self.password)
            fn(self)
            self.client.logout()

        return _wrapper

    @staticmethod
    def login(fn, user=None):
        def _wrapper(self=None):
            if user:
                self.client.login(username=user.username, password=user.password)
            else:
                self.client.login(username=self.user.username, password=self.password)
            fn(self)
            self.client.logout()

        return _wrapper

    def redirect_to_login_on_post(self, view_name, params=None, pargs=None, ajax=False):
        """
        :rtype: django.http.HttpResponse
        """
        if not pargs:
            pargs = []
        if not params:
            params = {}
        response = self.client.post(
            reverse(view_name, args=pargs),
            params,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest' if ajax else None
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                             reverse("django.contrib.auth.views.login") + '?next=%s' % reverse(view_name, args=pargs))
        return response

    def redirect_to_login_on_get(self, view_name, params=None, pargs=None, ajax=False):
        """
        :rtype: django.http.HttpResponse
        """
        if not pargs:
            pargs = []
        if not params:
            params = {}
        response = self.client.get(
            reverse(view_name, args=pargs),
            params,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest' if ajax else None
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                             reverse("django.contrib.auth.views.login") + '?next=%s' % reverse(view_name, args=pargs))
        return response

    def redirect_on_post(self, view_name, params=None, pargs=None, ajax=False):
        """
        :rtype: django.http.HttpResponse
        """
        if not pargs:
            pargs = []
        if not params:
            params = {}
        response = self.client.post(
            reverse(view_name, args=pargs),
            params,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest' if ajax else None
        )
        self.assertEqual(response.status_code, 302)
        return response

    def redirect_on_get(self, view_name, params=None, pargs=None, ajax=False):
        """
        :rtype: django.http.HttpResponse
        """
        if not pargs:
            pargs = []
        if not params:
            params = {}
        response = self.client.get(
            reverse(view_name, args=pargs),
            params,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest' if ajax else None
        )
        self.assertEqual(response.status_code, 302)
        return response

    def post(self, view_name, params=None, pargs=None, ajax=False):
        """
        :rtype: django.http.HttpResponse
        """
        if not params:
            params = {}
        if not pargs:
            pargs = []
        response = self.client.post(
            reverse(view_name, args=pargs),
            params,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest' if ajax else None
        )
        return response


    def get(self, view_name, params=None, pargs=None, ajax=False):
        """
        :rtype: django.http.HttpResponse
        """
        if not params:
            params = {}
        if not pargs:
            pargs = []
        response = self.client.get(
            reverse(view_name, args=pargs),
            params,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest' if ajax else None
        )
        return response

    def can_post(self, view_name, params=None, pargs=None, ajax=False):
        """
        :rtype: django.http.HttpResponse
        """
        if not params:
            params = {}
        if not pargs:
            pargs = []
        response = self.client.post(
            reverse(view_name, args=pargs),
            params,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest' if ajax else None
        )
        self.assertEqual(response.status_code, 200)
        return response

    def can_get(self, view_name, params=None, pargs=None, ajax=False):
        """
        :rtype: django.http.HttpResponse
        """
        if not pargs:
            pargs = []
        if not params:
            params = {}
        response = self.client.get(
            reverse(view_name, args=pargs),
            params,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest' if ajax else None
        )
        self.assertEqual(response.status_code, 200)
        return response