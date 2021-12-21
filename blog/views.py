# Create your views here.
from django.contrib import messages
from django.shortcuts import render, HttpResponse, redirect
from blog.models import Post, Comment

def blogHome(request):
    allPosts = Post.objects.all()
    context = {'allPosts': allPosts}
    return render(request, 'blog/blogHome.html', context)

def blogPost(request, slug):
    post = Post.objects.filter(slug=slug).first()
    comments = Comment.objects.filter(post=post, parent_comment=None)
    replies = Comment.objects.filter(post=post).exclude(parent_comment=None)
    replyDict = {}
    for reply in replies:
        if reply.parent_comment.sno not in replyDict.keys():
            replyDict[reply.parent_comment.sno] = [reply]
        else:
            replyDict[reply.parent_comment.sno].append(reply)
    return render(request, 'blog/blogPost.html', {'post': post, 'comments': comments, 'user': request.user, 'replyDict': replyDict})

def postComment(request):
    if request.method == "POST":
        comment=request.POST.get('comment')
        user=request.user
        postSno =request.POST.get('postSno')
        post= Post.objects.get(sno=postSno)
        parentSno= request.POST.get('parentSno')
        if parentSno=="":
            comment=Comment(comment_content= comment, user=user, post=post)
            comment.save()
            messages.success(request, "Your comment has been posted successfully")
        else:
            parent= Comment.objects.get(sno=parentSno)
            comment=Comment(comment_content= comment, user=user, post=post , parent_comment=parent)
            comment.save()
            messages.success(request, "Your reply has been posted successfully")
    return redirect(f"/blog/{post.slug}")