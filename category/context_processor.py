from .models import Category

#context processor to show the categories in the navbar
#this is a function that returns a dictionary
#the dictionary contains the categories that are available


def menu_links(request): 
    links = Category.objects.all()
    return dict(links=links)
#this is a dictionary that contains the categories that are available
