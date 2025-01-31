from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import NewsPostForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import NewsPost, Category
from django.views.generic import DetailView
from django.views.generic import DeleteView
from django.views.generic import FormView
from .forms import ContactForm
from django.contrib import messages
from django.core.mail import EmailMessage
from .forms import DeleteRequestForm
from django.shortcuts import get_object_or_404


class IndexView(ListView):
    template_name = 'index.html'
    queryset = NewsPost.objects.order_by('-posted_at')
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # カテゴリリストを追加
        context['categories'] = Category.objects.all()  # Categoryモデルからカテゴリを取得
        context['active_category_id'] = None  # トップページではアクティブカテゴリなし
        return context

@method_decorator(login_required, name='dispatch')
class CreateNewsView(CreateView):
    form_class = NewsPostForm
    template_name = "post_news.html"
    success_url = reverse_lazy('news:post_done')

    def form_valid(self, form):
        postdata = form.save(commit=False)
        postdata.user = self.request.user
        postdata.save()
        return super().form_valid(form)

class PostSuccessView(TemplateView):
    template_name = 'post_success.html'

class CategoryView(ListView):
    template_name = 'index.html'
    paginate_by = 9

    def get_queryset(self):
        category_id = self.kwargs['category']
        categories = NewsPost.objects.filter(
            category=category_id).order_by('-posted_at')
            
        return categories
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # カテゴリリストを取得して渡す
        context['categories'] = Category.objects.all()  # Categoryモデルからカテゴリを取得
        context['active_category_id'] = self.kwargs['category']  # 現在のカテゴリIDを渡す
        return context

class UserView(ListView):
    template_name = 'index.html'
    paginate_by = 9
    
    def get_queryset(self):
        user_id = self.kwargs['user']
        user_list = NewsPost.objects.filter(
            user=user_id).order_by('-posted_at')

        return user_list

class DetailView(DetailView):
    template_name = 'detail.html'
    model = NewsPost 

class MypageView(ListView):
    template_name = 'mypage.html'
    paginate_by = 9

    def get_queryset(self):
        queryset = NewsPost.objects.filter(
            user=self.request.user).order_by('-posted_at')
        return queryset

class NewsDeleteView(DeleteView):
    model = NewsPost
    template_name ='news_delete.html'
    success_url = reverse_lazy('news:mypage')

    def delete(self, request, *args, **kwargs):

        return super().delete(request, *args, **kwargs)

#お問い合わせ(オリジナル)
class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('news:contact_success')

    def form_valid(self, form):
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        title = form.cleaned_data['title']
        message = form.cleaned_data['message']

        subject = 'お問い合わせ : {}'.format(title)

        message = \
            '送信者名: {0}\nメールアドレス: {1}\n タイトル:{2}\n メッセージ:\n{3}'\
            .format(name, email, title, message)

        from_email = 'fko2447082@stu.o-hara.ac.jp'

        to_list = ['fko2447082@stu.o-hara.ac.jp']

        message = EmailMessage(subject=subject,
                                body=message,
                                from_email=from_email,
                                to=to_list,
                                )

        message.send()


            
        return super().form_valid(form)
    def contact_success(request):
        return render(request, 'contact_success.html')

class ContactSuccessView(TemplateView):
    template_name = 'contact_success.html'

#削除申請(オリジナル)
class DeleteRequestView(FormView):
    template_name = 'delete_request.html'
    form_class = DeleteRequestForm
    success_url = reverse_lazy('news:delete_request_success')

    def get(self, request, *args, **kwargs):
        # 投稿情報を取得
        record_id = self.kwargs['record_id']  # URLパラメータから投稿IDを取得
        record = get_object_or_404(NewsPost, id=record_id)  # NewsPost を使います
        
        # フォームを取得
        form = self.get_form()
        
        # 投稿情報をフォームに渡す
        form.fields['title'].initial = '削除申請' # 投稿のタイトルをフォームにセット
        self.extra_context = {'record': record}
        
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        # フォームが正常に送信された場合の処理
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']

        # 件名を固定に設定
        subject = '削除申請'

        # メッセージを作成
        body = '送信者名: {0}\nメールアドレス: {1}\n メッセージ:\n{2}'\
            .format(name, email, message)

        from_email = 'fko2447082@stu.o-hara.ac.jp'
        to_list = ['fko2447082@stu.o-hara.ac.jp']


        email_message = EmailMessage(subject=subject, body=body, from_email=from_email, to=to_list)
        email_message.send()



        return super().form_valid(form)
    def delete_request_success(request):

        return render(request, 'delete_request_success.html')

class DeleteRequestSuccessView(TemplateView):
    template_name = 'delete_request_success.html'

