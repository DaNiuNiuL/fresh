from django.shortcuts import render,redirect

from django.http import JsonResponse,HttpResponseRedirect,HttpResponse

from .models import UserModel,CollectGoodsModel
from goods.models import GoodsModel
from order.models import OrderModel

from .forms import UserRegisterForm,UserLoginForm
from django.core.paginator import Paginator
from django.contrib.auth.hashers import make_password,check_password

from .utils import login_required
# Create your views here.

# 只接受post请求
def register_post(request):
    # 只接受post请求的注册接口
    if request.method == 'POST':
        # user = UserRegisterForm(request.POST)
        user = UserLoginForm(request.POST)
        # 验证表单数据
        if not user.is_valid():
            return JsonResponse(user.errors.get_json_data(),safe=False)
    user = UserLoginForm()
    return render(request,'user/register_post.html',{'user':user})

def register(request):
    # 注册接口
    if request.method == 'POST':
        username = request.POST.get('username','')
        # 忽略参数为空的
        password = request.POST.get('password','')
        phone = request.POST.get('phone','')
        address = request.POST.get('address','')
        email = request.POST.get('email','')

        # 新建用户
        user = UserModel()
        user.username = username
        # 密码加密后存储
        user.password = make_password(password)
        user.phone = phone
        user.address = address
        user.email = email
        user.save()
        return JsonResponse({'user':'success'})
        # return render(request, 'user/login.html')
    return render(request,'user/register.html')

def login(request):
    # 登陆接口
    if request.method == 'POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        # 当这个jizhu有值的时候，就是这个复选框被勾选的时候的值1，没有的话是0
        jizhu = request.POST.get('jizhu',0)

        # 根据用户名查用户对象
        user = UserModel.objects.filter(username=username)

        # 判断 如果没有查到说明用户名错误 ，如果查到判断密码是否正确
        # 密码错误：返回登陆页面 并且提示密码错误
        if user:
            user = user[0]
            # 检查密码是否正确
            is_password = check_password(password,user.password)
            if not is_password:
                # 密码错误
                return render(request,'user/login.html',{'username':username,'is_password':1,'is_user':0})
            else:
                # 密码正确
                # 先生成一个response对象
                next_url = request.COOKIES.get('next_url','/account/info/')
                response = HttpResponseRedirect(next_url)
                # 记住用户名
                # 设置cookie
                if jizhu !=0:
                    response.set_cookie('username',username)
                    # response.set_cookie('password',password)
                else:
                    response.set_cookie('username','',max_age=-1)#max_age=-1 表示立即过期
                # 把用户id和username放入session中
                request.session['user_id']=user.id
                request.session['username']=username
                return response
            # return render(request,'user/index.html',{'username':user.username})
        else:
            return render(request,'user/login.html',{'username':username,'is_user':1,'is_password':0})
    return render(request,'user/login.html')

#退出
def logout(request):
    del request.session['user_id']
    del request.session['username']
    return redirect('/account/login')

@login_required
def info(request):
    # 用户个人信息
    user_id = request.session['user_id']
    user = UserModel.objects.get(id=user_id)

    user_info = {
        'username':user.username,
        'phone':user.phone,
        'address':user.address,
    }
    # 从session中拿到商品id的列表（在商品详情页里写入session的）
    goods_id_list = request.session.get(str(user_id),[])
    # 用户最近浏览的商品记录
    goods_list = []
    # 通过遍历商品id列表 拿到商品对象组成一个有序的商品对象列表
    for goods_id in goods_id_list:
        goods_list.append(GoodsModel.objects.get(id=goods_id))

    context = {
        'title':'用户中心',
        'user_info': user_info,
        'goods_list': goods_list,
        'active':'info'
    }
    return render(request,'user/user_center_info.html',context)

@login_required
def all_order(request,page_num):
    # 全部订单
    # 查询当前登陆用户的所有订单信息
    user_id = request.session.get('user_id')
    all_order = OrderModel.objects.filter(user_id = user_id)
    # 每一页展示2个
    paginator = Paginator(all_order,2)
    page = paginator.page(page_num)

    context = {
        'page':page,
        'page_num':page_num,
        'title':'全部订单',
        'active':'all_order'
    }
    return render(request,'user/user_center_order.html',context)

@login_required
def site(request):
    user_id = request.session['user_id']
    person = UserModel.objects.get(id=user_id)
    user = CollectGoodsModel.objects.get(user_id=user_id)

    user_info = {
        'address':person.address,
        'person_name': user.person_name,
        'tel': user.tel,
        'detail_address': user.detail_address,
        'is_used':user.is_used,

    }
    context = {
        'user_info':user_info,
        'title': '用户中心',
        'active': 'site'
    }
    return render(request,'user/site.html',context)


def upload(request):
    # 上传接口
    if request.method == 'GET':
        return render(request,'upload.html')
    if request.method == 'POST':
        myfile = request.FILES.get('myfile')
        ext = myfile.name.split('.')[-1]
        filename = 'text.'+ext
        with open(filename,'wb')as fp:
            for chunk in myfile.chunks():
                fp.write(chunk)
        return JsonResponse({'result':'success'})



def handle_wx(request):
    # 微信公众平台绑定验证
    echostr = request.GET.get('echostr','')
    return HttpResponse(echostr,content_type='text/plain')