import subprocess
from django.conf import settings

class SignMobileConfigMiddleware(object):

    def process_request(self, request):
        request._mobile_config_should_sign = (
            request.path.endswith(".mobileconfig") and 
            getattr(settings, "MOBILE_CONFIG_ENABLE_SIGN", False)
        )

    def process_response(self, request, response):
        if getattr(request, '_mobile_config_should_sign', False):
            response.content = self._sign(response.content)
        return response

    def _sign(self, text):
        openssl_path = getattr(settings, "MOBILE_CONFIG_OPENSSL_BIN_PATH", "/usr/bin/openssl")
        cert_file = getattr(settings, "MOBILE_CONFIG_SIGNER_CERT_FILE")
        key_file = getattr(settings, "MOBILE_CONFIG_SIGNER_KEY_FILE")
        cacert_file = getattr(settings, "MOBILE_CONFIG_SIGNER_CACERT_FILE")
        p = subprocess.Popen([
            openssl_path, "smime", "-sign",
            "-signer", cert_file, 
            "-inkey",  key_file,
            "-certfile", cacert_file, 
            "-outform", "der", "-nodetach"
        ], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        output, output_err = p.communicate(text)
        return output

