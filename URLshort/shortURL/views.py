from django.shortcuts import render, redirect
from .models import shortURL
from django.http import Http404

def shorten_url(request):
    if request.method == 'POST':
        # original_url = request.POST['original_url']
        original_url = request.POST.get('original_url')
        short_code = generate_short_code()
        shortened_url = shortURL(original_url=original_url, short_code=short_code)
        shortened_url.save()
        context = {
            'shortened_url': shortened_url
            }
        return render(request, 'shortened.html', context)
    return render(request, 'index.html')

def redirect_to_original(request, short_code):
    try:
        shortened_url = shortURL.objects.get(short_code=short_code)
        return redirect(shortened_url.original_url)
    except shortURL.DoesNotExist:
        raise Http404("Short URL does not exist")

def generate_short_code(length=6):
    import random
    import string
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
