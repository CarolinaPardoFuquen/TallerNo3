from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from .models import Review, Wine, Cluster, Recomendations, RecomendationsCat
from .forms import ReviewForm
from .forms import RegistrationForm
from .suggestions import update_clusters
from django.views.generic.list import ListView
from .filters import RecomendationsFilter
import datetime

from django.contrib.auth.decorators import login_required

def review_list(request):
    latest_review_list = Review.objects.order_by('-pub_date')[:9]
    context = {'latest_review_list':latest_review_list}
    return render(request, 'reviews/review_list.html', context)


def review_detail(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    return render(request, 'reviews/review_detail.html', {'review': review})


def wine_list(request):
    wine_list = Wine.objects.order_by('-name')
    context = {'wine_list':wine_list}
    return render(request, 'reviews/wine_list.html', context)

def top_list(request):
    return render(request,'reviews/pruebaa3.html')


def wine_detail(request, wine_id):
    wine = get_object_or_404(Wine, pk=wine_id)
    form = ReviewForm()
    return render(request, 'reviews/wine_detail.html', {'wine': wine, 'form': form})

@login_required
def add_review(request, wine_id):
    wine = get_object_or_404(Wine, pk=wine_id)
    form = ReviewForm(request.POST)
    if form.is_valid():
        rating = form.cleaned_data['rating']
        comment = form.cleaned_data['comment']
        user_name = request.user.username
        review = Review()
        review.wine = wine
        review.user_name = user_name
        review.rating = rating
        review.comment = comment
        review.pub_date = datetime.datetime.now()
        review.save()
        update_clusters()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('reviews:wine_detail', args=(wine.id,)))
    
    return render(request, 'reviews/wine_detail.html', {'wine': wine, 'form': form})
    

def user_review_list(request, username=None):
    if not username:
        username = request.user.username
    latest_review_list = Review.objects.filter(user_name=username).order_by('-pub_date')
    context = {'latest_review_list':latest_review_list, 'username':username}
    return render(request, 'reviews/user_review_list.html', context)


@login_required
def user_recommendation_list(request):
    
    # get request user reviewed wines
    user_reviews = Review.objects.filter(user_name=request.user.username).prefetch_related('wine')
    user_reviews_wine_ids = set(map(lambda x: x.wine.id, user_reviews))

    # get request user cluster name (just the first one righ now)
    try:
        #user_cluster_name = \
        #    User.objects.get(username=request.user.username).cluster_set.first().name
        user_cluster = \
            User.objects.get(username=request.user.username).cluster_set.first()
        user_cluster_name = user_cluster.name if user_cluster else None

    except: # if no cluster assigned for a user, update clusters
        update_clusters()
        user_cluster_name = \
            User.objects.get(username=request.user.username).cluster_set.first().name
    
    # get usernames for other memebers of the cluster
    user_cluster_other_members = \
        Cluster.objects.get(name=user_cluster_name).users \
            .exclude(username=request.user.username).all()
    other_members_usernames = set(map(lambda x: x.username, user_cluster_other_members))

    # get reviews by those users, excluding wines reviewed by the request user
    other_users_reviews = \
        Review.objects.filter(user_name__in=other_members_usernames) \
            .exclude(wine__id__in=user_reviews_wine_ids)
    other_users_reviews_wine_ids = set(map(lambda x: x.wine.id, other_users_reviews))
    
    # then get a wine list including the previous IDs, order by rating
    wine_list = sorted(
        list(Wine.objects.filter(id__in=other_users_reviews_wine_ids)), 
        key=lambda x: x.average_rating, 
        reverse=True
    )

    return render(
        request, 
        'reviews/user_recommendation_list.html', 
        {'username': request.user.username,'wine_list': wine_list}
    )


class WineListView(ListView):

    model = Wine
    paginate_by = 50
    # context_object_name = 'wine_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #print('context', context)
        return context


def RecomendationsListOnline(request):
    return render(request,'reviews/top_listonline.html')


def RecomendationsList(request):
    context2 = {}
    recomendationfiltered=[]
    recomendationcatfiltered=[]
    userscontext = []
    users = Recomendations.objects.distinct('ID_User')
    aux = 0
    for u in users:
        if aux < 800:
            aux += 1
            userscontext.append(u)
    context2['users'] = userscontext 
    #def get_queryset(self):
    #    result = super(RecomendationsList, self).get_queryset()
    #    filter_uid =self.request.GET.get('user_id')
    #    print ("methodsssssssssssssssssssssssssssss", filter_uid)
    Recomendation = Recomendations.objects.all() #este es el query set
    RecomendationCat = RecomendationsCat.objects.all() #este es el query set
    for r in Recomendation:
        #print ("RECCCCC", r.ID_User)
        #print ("RECCCC1", request.GET.get('user_id'))
        if request.GET.get('user_id'):
            #print ("AAAAAAAAAAAAAAAAA")
            if int(request.GET.get('user_id')) == int(r.ID_User):
                #print ("LLEENAAANDOOOOOO")
                recomendationfiltered.append(r)
        else:
            if str(request.user) == "AnonymousUser":
                if int(r.ID_User) == 1:
                    recomendationfiltered.append(r)

            elif int(request.user.id) == int(r.ID_User):
                recomendationfiltered.append(r)

    for rc in RecomendationCat:
        if request.GET.get('user_id'):
            if int(request.GET.get('user_id')) == int(rc.ID_User2):
                recomendationcatfiltered.append(rc)
        else:
            if str(request.user) == "AnonymousUser":
                if int(rc.ID_User2) == 1:
                    recomendationcatfiltered.append(rc)

            elif int(request.user.id) == int(rc.ID_User2):
                recomendationcatfiltered.append(rc)

    #print ("REQUESTTTTTTTTTTTTTT", request.GET.get('user_id'))
    #if request.GET.get('user_id'):
    #    recomendationsFilter = RecomendationsFilter(request.GET, queryset=Recomendation)
    #    #recomendationsFilter = RecomendationsFilter(request.GET, queryset=0)
    #    print ('ENTROOOOOOOOOOOOOO')
    #    context2['Recomendations'] = recomendationsFilter
    #    context2['RecomendationsCat'] = RecomendationCat
    #    return render(request,'reviews/top_list2.html', context2)
    if request.GET.get('user_id') or request.user.id == None or request.user.id:
        context2['Recomendations'] = recomendationfiltered
        context2['RecomendationsCat'] = recomendationcatfiltered
    else:
        context2['Recomendations'] = Recomendation
        context2['RecomendationsCat'] = RecomendationCat
    #print (context2)
    return render(request,'reviews/top_list2.html', context2)

def RecomendationsListCat(request):
    RecomendationCat = RecomendationsCat.objects.all() #este es el query set
    context3 = {'RecomendationsCat':RecomendationCat}
    return render(request,'reviews/top_list2.html', context3)

def user_list(request):
    filter = UserFilter(request.GET, queryset=Recomendations.objects.all())
    return render(request,'reviews/top_list2.html', {'filter':filter})

#class RecomendationsList(object):
    """docstring for RecomendationsList"""
    #model = Recomendations
    #template_name = 
    #def __init__(self, arg):
        #super(RecomendationsList, self).__init__()
        #self.arg = arg
        

def register(request):
    #print ("ddd", request.method)

    if request.method == 'POST':
        #print ("11111")
        form = RegistrationForm(request.POST)
        #print ("11111", form.is_valid())
        if form.is_valid():
            #print ("11111")
            form.save()
            return render(request,'reviews/pruebaa3.html')
        args = {'form': form}
        #print ("MAPFARGSSSS",args)
        return render(request, 'reviews/registration_form.html', args)
    else:
        form = RegistrationForm()
        #print ("MAPFFFFFFFFFFFFFFFFFFFFFFFF2", form)

        args = {'form': form}
        #print ("MAPFARGSSSS",args)
        return render(request, 'reviews/registration_form.html', args)

