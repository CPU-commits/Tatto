import requests
import hmac
import time
import hashlib
from urllib.parse import urlparse, parse_qs, urlencode
# FastAPI
from fastapi import UploadFile
# Settings
from app.dependencies import settings

class ImageService():
    _url: str
    _headers: map
    _secret_key_data: bytes

    def __init__(self):
        self._url = settings.API_CLOUDFLARE.replace('<ACCOUNT_ID>', settings.API_CLOUDFLARE_ACCOUNT_ID)
        self._headers = {
            'Authorization': f'Bearer {settings.API_CLOUDFLARE_TOKEN}',
        }
        self._secret_key_data = settings.API_KEY_SECRET.encode('utf-8')

    def _is_supported_format(self, file: UploadFile) -> bool:
        return True

    def _is_valid_dimensions_ans_sizes(self, file: UploadFile) -> bool:
        return True

    def upload(self, file: UploadFile, type = 'tattoo', require_signed_urls = True) -> str | None:
        if self._is_supported_format(file) is False:
            return
        if self._is_valid_dimensions_ans_sizes(file) is False:
            return
        # Body
        files = {
            'file': (file.filename, file.file),
        }
        payload = {
            'metadata': '{"type":"@type"}'.replace('@type', type),
            'requireSignedURLs': 'true' if require_signed_urls else 'false',
        }

        response = requests.post(self._url, headers=self._headers, files=files, data=payload)
        if response.ok is False:
            return None

        return response.json()['result']['variants'][0]

    def _buffer_to_hex(self, buffer: bytes):
        return ''.join(format(x, '02x') for x in buffer)
    
    def get_signed_url(self, url: str, expiration = 60 * 5) -> str:
        key = hmac.new(self._secret_key_data, digestmod=hashlib.sha256)
        expiry = int(time.time()) + expiration
        url_parts = urlparse(url)
        query_params = parse_qs(url_parts.query)
        query_params['exp'] = str(expiry)

        url = url_parts._replace(query=urlencode(query_params, doseq=True)).geturl()
        url_parts = urlparse(url)

        string_to_sign = url_parts.path + '?' + url_parts.query

        # Generate signature
        key.update(string_to_sign.encode('utf-8'))
        sig = self._buffer_to_hex(key.digest())

        url_parts = urlparse(url)
        query_params['sig'] = sig
        url = url_parts._replace(query=urlencode(query_params, doseq=True)).geturl()

        return url

image_service = ImageService()
