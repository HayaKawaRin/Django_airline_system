import random
import string

class PromoCodeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'promo_code_seen' not in request.session:
            promo_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            request.session['promo_code'] = promo_code
            request.session['promo_code_seen'] = False

        response = self.get_response(request)
        return response
