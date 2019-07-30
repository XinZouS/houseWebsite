from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .models import Contact

def contact(request):
	if request.method == 'POST':
		listing_id = request.POST.get('listing_id')
		listing = request.POST.get('listing')
		name = request.POST.get('name')
		email = request.POST.get('email')
		phone = request.POST.get('phone')
		message = request.POST.get('message')
		user_id = request.POST.get('user_id')
		realtor_email = request.POST.get('realtor_email')

	# check if user already made inquiry:
	if request.user.is_authenticated:
		user_id = request.user.id 
		has_contacted = Contact.objects.filter(listing_id=listing_id, user_id=user_id)
		if has_contacted:
			messages.error(request, 'You have already made an inquiry for this listing')
			return redirect('/listings/'+listing_id)
	# else create new contact:
	contact = Contact(listing=listing, listing_id=listing_id, name=name,
		email=email, phone=phone, message=message, user_id=user_id)
	contact.save()

	# send main
	send_mail(
		'Property Listing Inquiry',
		'There has been an inquiry for ' + listing + '. Sign in to see more;',
		'traversy.brad@gmail.com',
		[realtor_email, 'sanking.saphira@gmail.com'],
		fail_silently=False,
	)
	messages.success(request, 'Your request has been submitted')

	return redirect('/listings/'+listing_id)


