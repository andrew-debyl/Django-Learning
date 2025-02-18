from django.shortcuts import render
from datetime import date, timedelta
from django.db.models import Count
from .models import *

# these run from urls.py when you go to a specific path


# this one gets all customers and sends it to index.html
def index(request):
    customers = Customer.objects.all()
    context = {"customers":customers}
    return render(request,"index.html",context=context)


# this one creates a customer and sends either a success msg, or if the form hasnt been sen
# yet, it just shows the page without the msg
def create_customer(request):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        address = request.POST["address"]
        social_media = request.POST["social_media"]
        customer = Customer.objects.create(name=name,email=email,phone=phone,address=address,social_media=social_media)
        customer.save()
        msg = "Successfully Saved a Customer"
        return render(request,"add.html",context={"msg":msg})
    return render(request,"add.html")


# this one is getting all interactions within the last 30 days and sending
# it to summary.html
def summary(request):
    # these lines are filtering all interactions within the last 30 days
    thirty_days_ago = date.today() - timedelta(days=30)
    interactions = Interaction.objects.filter(interaction_date__gte=thirty_days_ago)

    count = len(interactions)

    # this is saying the data is grouped by channel and direction.
    # And then for each unique combination of channel and direction, 
    # the Count('channel') counts how many times that combination appears in the dataset
    interactions = interactions.values("channel","direction").annotate(count=Count('channel'))
    
    context={
                "interactions":interactions,
                "count":count
             }

    return render(request,"summary.html",context=context)


# this one is saving a new interaction
def interact(request,cid):

    channels = Interaction.CHANNEL_CHOICES  # Get possible channel choices from the Interaction model
    directions = Interaction.DIRECTION_CHOICES  # Get possible direction choices from the Interaction model
    context = {"channels":channels,"directions":directions}

    if request.method == "POST":

        customer = Customer.objects.get(id=cid)  # Get the customer object with the given id (cid)
        channel = request.POST["channel"]  # Get the selected channel and direction from the form
        direction = request.POST["direction"]
        summary = request.POST["summary"]
        interaction = Interaction.objects.create(
                                    customer=customer,
                                    channel=channel,
                                    direction=direction,
                                    summary=summary)
        interaction.save()  # create and save a new interaction
        context["msg"] = "Interaction Success"
        return render(request,"interact.html",context=context)

    return render(request,"interact.html",context=context)