from django.shortcuts import redirect


class RedirectToFascia:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('fascia')
        return super().dispatch(request, *args, **kwargs)
