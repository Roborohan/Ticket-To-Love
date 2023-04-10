from django.views import View
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import requests
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Message
from Crypto.Cipher import AES
import base64
 
def encrypt_message(text, key):
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(text.encode())
    return base64.b64encode(nonce + ciphertext + tag).decode()

def decrypt_message(ciphertext, key):
    ciphertext = base64.b64decode(ciphertext.encode())
    nonce = ciphertext[:16]
    tag = ciphertext[-16:]
    ciphertext = ciphertext[16:-16]
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag).decode()
    return plaintext

def get_conversations(user, sort_by='name'):
    if sort_by == 'name':
        conversations = user.matches.order_by('username')
    elif sort_by == 'recent':
        conversations = user.matches.annotate(
            last_sent=Max('received_messages__sent_at')
        ).order_by('-last_sent')
    else:
        raise ValueError('Invalid sort_by argument')
    return conversations

def get_messages(user1, user2):
    messages = Message.objects.filter(
        (Q(sender=user1) & Q(receiver=user2)) | (Q(sender=user2) & Q(receiver=user1))
    ).order_by('sent_at')
    return messages

# @login_required
# def messages(request):
#     conversations = request.user.sent_messages.all() | request.user.received_messages.all()
#     conversations = conversations.order_by('sent_at').distinct('sender', 'recipient')
#     context = {'conversations': conversations}
#     return render(request, 'messages.html', context)

@login_required
def chat(request, recipient_id):
    recipient = get_object_or_404(User, id=recipient_id)
    messages = Message.objects.filter(sender=request.user, recipient=recipient) | Message.objects.filter(sender=recipient, recipient=request.user)
    messages = messages.order_by('sent_at')
    context = {'recipient': recipient, 'messages_chat': messages}
   
    return render(request, 'chat.html', context)


@login_required
def send_message_recipient(request,recipient_id):
    if request.method == 'POST':         
        recipient = get_object_or_404(User, id=recipient_id)
        content = request.POST.get('content')
        message = Message(sender=request.user, recipient=recipient, content=content)       
        message.save()
        return redirect('chatapp:chat', recipient_id=recipient_id)
     
        # return JsonResponse({'status': 'success'})
        # url = reverse('chatapp:chat', args=[recipient_id])
 