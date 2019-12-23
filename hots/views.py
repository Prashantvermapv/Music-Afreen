from django.shortcuts import render, get_object_or_404
from .models import Hots


IMAGE_FILE_TYPES=['png','jpg','jpeg']
# Create your views here.
def indexView(request):
    all_hots=Hots.objects.order_by('-post_date')
    return render(request,'hots/index.html',{'all_hots':all_hots})

def detailView(request,hots_id):
    hots=get_object_or_404(Hots,pk=hots_id)
    return render(request,'hots/details.html',{'hots':hots})
