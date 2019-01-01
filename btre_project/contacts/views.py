from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
# import yagmail
from .models import Contact
# Create your views here.

def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        user_id = request.POST['user_id']
        message = request.POST['message']
        realtor_email = request.POST['realtor_email']
        
        # Check if user had made inquiry already
        if request.user.is_authenticated:
                user_id = request.user.id
                has_contacted = Contact.objects.all().filter(listing_id=listing_id, user_id=user_id)
                if has_contacted:
                        messages.error(request, 'You have already made an inquiry for this listing.')
                        return redirect('/listings/'+listing_id)
        
        contact = Contact(listing_id=listing_id, listing=listing, name=name, email=email, 
                          phone=phone, user_id=user_id, message=message)
        contact.save()

        # Email Sending
        # First way
        # yag = yagmail.SMTP('faiz.niet2013@gmail.com','faiz162162')
        # yag.send(realtor_email, subject="sub", contents="Test.")
        
        # second way inbuild django library
        send_mail(
                'Property listing inquiry',
                'There has been an inquiry for '+ listing + '. Sign into the admin panel for more info',
                settings.EMAIL_HOST_USER,
                [realtor_email, 'mr.faizahmad94@gmail.com'],
                fail_silently=False
        )
        
        messages.success(request, 'Your request has been submitted, a realtor will get back to you soon.')
        return redirect('/listings/'+listing_id)
