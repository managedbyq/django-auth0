# -*- coding: utf-8 -*-
import json
import requests

from django.contrib.auth import get_user_model, login, authenticate
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import redirect
from django.conf import settings

UserModel = get_user_model()


def process_login(request):
    code = request.GET.get('code', None)
    json_header = {'content-type': 'application/json'}
    token_url = 'https://%s/oauth/token' % settings.AUTH0_DOMAIN

    token_payload = {
        'client_id': settings.AUTH0_CLIENT_ID,
        'client_secret': settings.AUTH0_SECRET,
        'redirect_uri': '%s%s' % (settings.FULL_URL, reverse('auth0:auth_callback')),
        'code': code,
        'grant_type': 'authorization_code'
    }

    token_info = requests.post(token_url, data=json.dumps(token_payload), headers=json_header).json()
    user_url = "https://%s/userinfo?access_token=%s" % (settings.AUTH0_DOMAIN, token_info['access_token'])
    user_info = requests.get(user_url).json()

    # We're saving all user information into the session
    request.session['profile'] = user_info
    user = authenticate(**user_info)

    if user:
        login(request, user)
        # Redirect to the User logged in page that you want here
        # In our case it's /dashboard
        return redirect('dEngine2app:plan')

    return HttpResponse(status=400)
