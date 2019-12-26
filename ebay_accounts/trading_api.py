# -*- coding: utf-8 -*-
"""
Ebay Trading API
"""
import xmltodict
import requests

from . import app_settings as settings


class TradingAPIWarning(Exception):
    pass


class TradingAPIFailure(Exception):
    pass


class TradingAPIInvalidResponse(Exception):
    pass


class TradingAPI(object):
    _last_response = None

    def __init__(self, production=False, site_id=0, token=None):
        self.production = production

        if self.production is True:
            self._dev_id = settings.EBAY_PRODUCTION_DEVID
            self._app_id = settings.EBAY_PRODUCTION_APPID
            self._cert_id = settings.EBAY_PRODUCTION_CERTID
            self._endpoint = settings.EBAY_PRODUCTION_TRADING_API_ENDPOINT
            self.ru_name = settings.EBAY_PRODUCTION_RU_NAME
        else:
            self._dev_id = settings.EBAY_SANDBOX_DEVID
            self._app_id = settings.EBAY_SANDBOX_APPID
            self._cert_id = settings.EBAY_SANDBOX_CERTID
            self._endpoint = settings.EBAY_SANDBOX_TRADING_API_ENDPOINT
            self.ru_name = settings.EBAY_SANDBOX_RU_NAME
        self.site_id = site_id
        self.version = settings.EBAY_TRADING_API_VERSION
        self._token = token

    def _get_requester_credentials(self):
        return {'eBayAuthToken': self._token}

    def _get_headers(self, call):
        return {
            'X-EBAY-API-COMPATIBILITY-LEVEL': str(self.version),
            'X-EBAY-API-DEV-NAME': self._dev_id,
            'X-EBAY-API-APP-NAME': self._app_id,
            'X-EBAY-API-CERT-NAME': self._cert_id,
            'X-EBAY-API-SITEID': str(self.site_id),
            'X-EBAY-API-CALL-NAME': call,
        }

    def _get_xml_request(self, call, kw_dict, include_requester_credentials):
        request_key = '{call}Request'.format(call=call)
        request_dict = {request_key: {
            '@xmlns': 'urn:ebay:apis:eBLBaseComponents',
        }}
        for key, value in kw_dict.items():
            request_dict[request_key][key] = value
        if self._token and include_requester_credentials:
            credentials = self._get_requester_credentials()
            request_dict[request_key]['RequesterCredentials'] = credentials
        data = xmltodict.unparse(request_dict)
        return data

    def _get_data_from_response(self, call, data, response):
        d = xmltodict.parse(response.content)
        response_key = '{call}Response'.format(call=call)
        data = d[response_key]
        return data

    def execute(
            self,
            call,
            kw_dict,
            include_requester_credentials=True,
            raise_on_warning=False,
            raise_on_failure=True):
        headers = self._get_headers(call)
        data = self._get_xml_request(
            call, kw_dict, include_requester_credentials)
        print('making trading call {} \n{}\n{}'.format(self._endpoint, data, headers))
        response = requests.post(self._endpoint, data=data, headers=headers)
        print('response: {}'.format(response))
        self._last_response = response
        response_data = self._get_data_from_response(call, data, response)
        if 'Ack' not in response_data:
            raise TradingAPIInvalidResponse('No Ack field in response')
        if raise_on_failure and response_data['Ack'].lower() == 'failure':
            raise TradingAPIFailure('{0}'.format(response_data.get(
                'Errors', 'No error list found')))
        if raise_on_warning and response_data['Ack'].lower() == 'warning':
            raise TradingAPIWarning('{0}'.format(response_data.get(
                'Errors', 'No error list found')))
        return response_data

    def set_token(self, token):
        self._token = token

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 fileencoding=utf-8
