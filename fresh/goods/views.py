from django.shortcuts import render

from .models import CategoryModel,CategoryGoodsModel,GoodsModel
from cart.models import CartModel
from django.core.paginator import Paginator
from common.common import cart_count_goods

# Create your views here.






def index(request):
    # 主页
    # 拿出所有的分类
    category_list = CategoryModel.objects.all()
    # 分别取出分类下的最新的商品
    new_goods_dict = {} #存储每个分类下的最新的商品
    for category in category_list:
        # 直接通过商品分类id从goods中获取当前分类的商品
        goods_info_list = GoodsModel.objects.filter(category_id=category.id).order_by('id')[:4]
        # goods_list = CategoryGoodsModel.objects.filter(category_id=category.id).order_by('-goods_id')[:4]
        #拿到查询出的所有的goods的id
        # goods_ids = [goods.goods_id for goods in goods_list]
        # goods_info_list = GoodsModel.objects.filter(id__in=goods_ids)

        new_goods_dict[category]=goods_info_list

    # 从session中拿到user的id
    # user_id = request.session.get('user_id',0)
    # cart_list = CartModel.objects.filter(user_id=user_id)
    # cart_count = 0
    # 统计出购物车中所有的商品数量
    # for cart in cart_list:
    #     cart_count += cart.count
    cart_count = cart_count_goods(request,CartModel)
    context = {
        'new_goods_dict':new_goods_dict,
        'cart_count':cart_count
    }
    return render(request,'goods/index.html',context)




def list(request,category_id,sort,page_num):#order_by
    # 商品列表视图
    """category_id: 分类的id
        page_num: 获取当前页的页码
        sort:排序字段(默认的字段：default，价格：price，人气：popular)
    """
    category = CategoryModel.objects.get(id=category_id)
    # 取该类型最新的两个商品
    news = GoodsModel.objects.filter(category_id=category_id).order_by('-id')
    # 外键的用法
    # news = category.goodsModel_set.order_by('-id')[:2]
    goods_list = []

    if sort == 'default':#默认排序，最新在上面
        # if order_by == 0:
        #     goods_list = GoodsModel.objects.filter(category_id=category_id).order_by('id')
        # else:
        goods_list = GoodsModel.objects.filter(category_id=category_id).order_by('-id')
    elif sort == 'price':#按价格排序
        goods_list = GoodsModel.objects.filter(category_id=category_id).order_by('-price')
    elif sort == 'popular':#按人气排序
        goods_list = GoodsModel.objects.filter(category_id=category_id).order_by('-popular')
    # 根据商品的列表goods_list 进行分页
    paginator = Paginator(goods_list,2)
    page = paginator.page(page_num)
    cart_count = cart_count_goods(request,CartModel)
    context = {
        'category':category,
        'news':news,
        'goods_list':goods_list,#排序后的商品列表
        'sort':sort, #排序的条件
        'cart_count':cart_count,#购物车中的商品数量
        'page':page,
        'page_num':page_num,#当前的页数

    }
    return render(request,'goods/list.html',context)


def detail(request,goods_id):
    #某个商品的详细信息 goods_id 是具体的某个商品
    goods = GoodsModel.objects.get(id=goods_id)
    goods.popular = goods.popular+1#增加商品的人气值
    goods.save()
    # news =  GoodsModel.objects.filter(category_id=goods.category_id).order_by('-id')[:2]
    # 利用orm外键的特性
    news = goods.category.goodsmodel_set.order_by('-id')[:2]

    # 购物车内商品的数量
    cart_count=cart_count_goods(request,CartModel)

    # 记录最近的浏览记录 在用户中心使用
    # 判断是否已经登陆
    if request.session.has_key('user_id'):
        user_id = request.session.get('user_id')
        goods_id_list = request.session.get(user_id,[])
        if not goods_id_list:#判断是否有浏览记录
            goods_id_list.append(goods_id)
        else:
            if goods_id in goods_id_list:
                goods_id_list.remove(goods_id)
            goods_id_list.insert(0,goods_id) #添加元素到列表的第一个
            if len(goods_id_list)>5: #如果超过5个浏览记录 删除最后一个
                del goods_id_list[-1]
        # 把最近浏览的商品存储到session中 以user_id的值为key
        request.session[user_id]=goods_id_list
    return render(request,'goods/detail.html',{'goods':goods,'news':news,'cart_count':cart_count})
