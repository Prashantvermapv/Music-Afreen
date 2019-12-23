from django.shortcuts import render,get_object_or_404
from .models import Blog
from .forms import BlogForm



IMAGE_FILE_TYPES=['png','jpg','jpeg']
# Create your views here.
def indexView(request):
    all_blogs=Blog.objects.order_by('-post_date')
    return render(request,'blog/index.html',{'all_blogs':all_blogs})

def detailView(request,blog_id):
    blog=get_object_or_404(Blog,pk=blog_id)
    return render(request,'blog/detail.html',{'blog':blog})


def create_blog(request):
    form=BlogForm(request.POST or None ,request.FILES or None)
    if form.is_valid():
        blog=form.save(commit=False)
        blog.blog_image=request.FILES['blog_image']
        file_type=blog.blog_image.url.split('.')[-1]
        file_type=file_type.lower()
        if file_type not in IMAGE_FILE_TYPES:
            content={'blog':blog,'form':form,'error_message':'Image file must be PNG,JPG or JPEG'}
            return render(request,'blog/form.html',content)
        else:
            blog.save()
            return render(request,'blog/detail.html',{'blog':blog})
    else:
        return render(request,'blog/form.html',{'form':form})
