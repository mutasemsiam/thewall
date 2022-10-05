from django.shortcuts import render, redirect

# from wall_app.models import Message
from .models import User, Message, Comment


def show_wall(request):
    if 'user_id' not in request.session:
        
        return redirect("/") 
    context = {
        "all_the_messages": Message.objects.all(),
    } 

    return render(request,"wall.html", context)

def create_message(request):

    Message.objects.create(user = User.objects.get(id = request.session['user_id']), message = request.POST['add-message'])
    
    return redirect("/wall")

def create_comment(request):

    Comment.objects.create(message = Message.objects.get(id = request.POST['which_message']),user = User.objects.get(id = request.session['user_id']), comment = request.POST['add-comment'])

    return redirect("/wall")

def delete_msg(request):

    msg = Message.objects.get(id = request.POST['which_message'])
    msg.delete()
    
    return redirect("/wall")
