def count_user_clicks_middleware(get_response):
    def middleware(request):
        clicks_count = request.session.get('clicks_count', 0)
        clicks_count += 1
        request.session['clicks_count'] = clicks_count
        request.clicks_count = clicks_count
        return get_response(request)
    return middleware


def last_viewed_photo_middleware(get_response):
    def middleware(request):
        request.last_viewed_photos = request.session['last_viewed_photo_ids']
        return get_response(request)
    return middleware
