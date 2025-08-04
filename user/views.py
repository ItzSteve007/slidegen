from django.shortcuts import render

# Create your views here.
def user(request):
    images = [
        {'src': 'images/1.jpg', 'alt': 'The Woods'},
        {'src': 'images/2.jpg', 'alt': 'Cinque Terre'},
        {'src': 'images/3.jpg', 'alt': 'Mountains and fjords'},
        {'src': 'images/4.jpg', 'alt': 'Northern Lights'},
    ]
    return render(request, 'user.html', {'page': 'user', 'images': images})
