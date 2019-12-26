# -*- coding: utf-8 -*-
"""
Ebay Accounts Models
"""
from uuid import uuid4
from datetime import datetime
from urllib.parse import urlencode

import django
from django.urls import reverse
from django.db import models

from .trading_api import TradingAPI
from . import app_settings as settings


APP_NAME = 'ebay_accounts'


def gen_uuid_hex():
    return uuid4().hex


class Account(models.Model):
    """An eBay account"""
    user_id = models.CharField(max_length=255)
    expires = models.DateTimeField()
    token = models.TextField()
    production = models.BooleanField(default=False)
    site_id = models.IntegerField(choices=settings.EBAY_SITE_CHOICES)
    active = models.BooleanField(default=True)

    class Meta:
        if django.get_version() < '2.1.0':
            permissions = (
                ('view_account', 'Can view account'),
            )

    def __str__(self):
        return '{user_id}'.format(user_id=self.user_id)

    def get_absolute_url(self):
        return reverse(APP_NAME + '_account_detail', kwargs={'pk': self.pk})

    def is_active(self):
        if datetime.now() >= self.expires:
            return False
        if not self.token:
            return False
        if self.active:
            return True
        return False


class Session(models.Model):
    """An Ebay session that is used in creating the account"""
    session_id = models.CharField(
        max_length=40, blank=True)
    uuid = models.CharField(max_length=32, default=gen_uuid_hex, unique=True)
    production = models.BooleanField(default=False)
    site_id = models.IntegerField(choices=settings.EBAY_SITE_CHOICES)

    def __str__(self):
        return '{user_id}'.format(user_id=self.uuid)

    def set_session_id(self):
        trading = TradingAPI(
            production=self.production,
            site_id=self.site_id)
        response = trading.execute(
            'GetSessionID', {'RuName': trading.ru_name})
        print(response)
        self.session_id = response['SessionID']
        self.save()
        return self.session_id

    def get_sign_in_url(self):
        if self.production is True:
            url_template = settings.EBAY_PRODUCTION_TOKEN_SIGNIN_URL_TEMPLATE
            ru_name = settings.EBAY_PRODUCTION_RU_NAME
        else:
            url_template = settings.EBAY_SANDBOX_TOKEN_SIGNIN_URL_TEMPLATE
            ru_name = settings.EBAY_SANDBOX_RU_NAME
        return url_template.format(
            params=urlencode({
                'RuName': ru_name,
                'SessID': self.session_id,
                'ruparams': 'UUID={0}'.format(self.uuid),
            }))

    def reject(self):
        self.delete()

    def create_account(self):
        trading = TradingAPI(
            production=self.production,
            site_id=self.site_id)
        response = trading.execute(
            'FetchToken', {'SessionID': self.session_id})
        token = response['eBayAuthToken']
        expires = response['HardExpirationTime']

        trading.set_token(token)
        response = trading.execute(
            'GetUser', {})
        user_id = response['User']['UserID']

        return Account.objects.create(
            user_id=user_id,
            expires=expires,
            token=token,
            production=self.production,
            site_id=self.site_id,
        )

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 fileencoding=utf-8
