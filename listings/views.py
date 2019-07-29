from django.shortcuts import render, get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from .models import Listing
from .choices import price_choices, bedroom_choices, state_choices


def index(request):
	listings = list(Listing.objects.order_by('-list_date').filter(is_published=True))

	paginator = Paginator(listings, 3)
	page = request.GET.get('page')
	paged_listings = paginator.get_page(page)

	context = {'listings':paged_listings}
	return render(request, 'listings/listings.html', context)


def listing(request, listing_id):
	listing = get_object_or_404(Listing, pk=listing_id)
	context = {
		'listing': listing,
	}
	return render(request, 'listings/listing.html', context)


def search(request):
	queryset_list = Listing.objects.order_by('-list_date')
	# keywords; 
	if 'keywords' in request.GET:
		keywords = request.GET['keywords']
		if keywords:
			queryset_list = queryset_list.filter(description__icontains=keywords)
	# city:
	if 'city' in request.GET:
		city = request.GET.get('city')
		if city: # use __iexact filter: case insensitive; 
			queryset_list = queryset_list.filter(city__iexact=city)

	# state:
	if 'state' in request.GET:
		state = request.GET.get('state')
		if state: # use __iexact filter: case insensitive; 
			queryset_list = queryset_list.filter(state__iexact=city)

	# bedrooms:
	if 'bedrooms' in request.GET:
		bedrooms = request.GET.get('bedrooms')
		if bedrooms: # use __lte filter: less than or equal to
			queryset_list = queryset_list.filter(bedrooms__lte=bedrooms)

	# price:
	if 'price' in request.GET:
		price = request.GET.get('price')
		if price: # use __lte filter: less than or equal to
			queryset_list = queryset_list.filter(price__lte=price)

	context = {
		'listings': queryset_list,
		'state_choices': state_choices, 
		'bedroom_choices': bedroom_choices,
		'price_choices': price_choices,
		'values': request.GET,
	}
	return render(request, 'listings/search.html', context)

