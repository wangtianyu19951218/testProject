from django.shortcuts import render,redirect,HttpResponse
from .import models
import json
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.core.exceptions import ObjectDoesNotExist

from .models import Article,Tag,Shipinfo,User,Ownerinfo

# Create your views here.
def home(request):

    return render(request,'myauth/home.html')

def loginfun(request):
    #用户填好表单点了提交后，要判断用户是什么请求
    if(request.method == 'POST'):

        #如果是post请求，获取用户名和密码，使用authenticate方法获取
        #authenticate方法返回值是 如果有这个user就返回，如果没有就返回none
        #请求中的用户名，密码以字典的格式封装在request的POST中，字典的键名就是输入框的name值
        user = authenticate(request,username = request.POST.get('username',False),
                            password = request.POST.get('password1',False))
        if user is None:
            #如果user不存在返回主页，并且报错
            return render(request,'myauth/login-error.html',{'errortype':'user or password is wrong'})
        else:
            #如果用户存在，判断用户的权限
                #判断权限：根据username值到auth_user中找is_super字段是否为f

            username_pending = request.POST.get('username')
            #在数据库中查找用户输入的用户名是否存在，查到了继续，查不到跳到except
            try:
                userright_search = User.objects\
                .filter(username = username_pending)\
                .values_list('is_superuser',flat = True)[0]

                #如果是超级用户,登录并返回主页
                if(userright_search == True):
                    login(request, user)

                    return render(request, 'myauth/adminAfterLogin.html',{'right':'super'})
                #如果是普通用户
                else:
                    #login(request, user)
                    return render(request, 'myauth/login-error.html',{'errortype':'您没有管理员权限'})

            except ObjectDoesNotExist:

                return render(request, 'myauth/login-error.html', {'errortype': '账户不存在!'})
            #user存在则1、用这个user登录，2、并返回登录后的主页

    else:
        return render(request,'myauth/login.html')


def owner_login(request):
    if (request.method == 'POST'):
        # 如果是post请求，获取用户名和密码，使用authenticate方法获取
        # authenticate方法返回值是 如果有这个user就返回，如果没有就返回none
        # 请求中的用户名，密码以字典的格式封装在request的POST中，字典的键名就是输入框的name值
        user = authenticate(request, username=request.POST.get('username', False),
                            password=request.POST.get('password1', False))
        if user is None:
            # 如果user不存在返回主页，并且报错
            return render(request, 'myauth/login-error.html', {'errortype': 'user or password is wrong'})
        else:
            username_pending = request.POST.get('username')
            # 在数据库中查找用户输入的用户名是否存在，查到了继续，查不到跳到except
            try:
                userright_search = User.objects \
                    .filter(username=username_pending) \
                    .values_list('is_superuser', flat=True)[0]

                # 如果不是超级用户,登录并返回船主功能页
                if (userright_search == False):
                    login(request, user)

                    return render(request, 'myauth/ownerAfterLogin.html')
                # 如果是超级用户
                else:
                    #login(request, user)
                    return render(request, 'myauth/login-error.html', {'errortype': '您没有船主权限'})

            except ObjectDoesNotExist:

                return render(request, 'myauth/search_result.html', {'cuole': 'cuole!'})
    else:
        return render(request, 'myauth/login.html')

def tes(request):
    return render(request, 'myauth/xuanxiangka.html')


def searchship(request):
    #用户填好表单点了提交后，要判断用户是什么请求
    if(request.method == 'POST'):
        #如果是post请求，获取用户名和密码，使用authenticate方法获取
        #authenticate方法返回值是 如果有这个user就返回，如果没有就返回none
        #请求中的用户名，密码以字典的格式封装在request的POST中，字典的键名就是输入框的name值
        shipInfo = authenticate(request,shipid = request.POST.get('shipid',False))
        if shipInfo is None:
            #如果user不存在返回主页，并且报错
            return render(request,'myauth/login-error.html',{'errortype':'user or password is wrong'})
        else:
            # list = [
            #     '需求分析',
            #     '制作er图',
            #     '设计架构',
            #     '编写代码'
            # ]
            # context = {
            #     'title': '标题：',
            #     'yourlist': list,
            # }
            #user存在则1、用这个user登录，2、并返回登录后的主页
            #login(request,user)

            return render(request,'myauth/home.html')
    else:
        return render(request,'myauth/login.html')

def logoutfun(request):
    logout(request)
    return redirect('homename')

def register(request):
    if(request.method == 'POST'):#如果是post请求，应该这么做：
    #只要用户是post请求，不管填的对错，都创建成表单，然后再判断表单里的键值对不对
        registerForm = UserCreationForm(request.POST)#UserCreationForm不仅可以创建空表单，还可以根据已有信息创建表单
        #判断创建的表单正确与否
        if(registerForm.is_valid()):
            #如果表单的数据是对的，存到数据库中,然后创建这个用户(只有存到数据库中了，才能获取到username)
            registerForm.save()
            user = authenticate(username = registerForm.cleaned_data['username'],
                                password = registerForm.cleaned_data['password1'])

            #auth这个方法既可以创建用户，也可以验证用户是否存在
            #username,password不再不是从请求中取
            #现在是从创建的表单的键值中取，不同于login中的author的username是绑定的input框传来的
            #现在注册页面的表单是Django创建的，要通过审查元素看出input的name值
            #表单对了，就顺便登录，再回到主页
            loginfun(request)
            print(user)
            return redirect('homename')

    else:#如果不是post请求，应该这么做：
        #新建一个空表单
        registerForm = UserCreationForm()

    # 如果表单的数据是错的，传递表单信息回注册界面，表单信息中有error信息
    content = {'registerViews': registerForm}
    return render(request,'myauth/register.html',content)


def search(request):
    # allarticle = Article.objects.all()
    # alltag = Tag.objects.all()
    # context = {
    #     'allarticle':allarticle,
    #     'alltag':alltag,
    # }
    if request.method == 'POST':

        shipid = request.POST.get('shipid')

        #shipid = type(shipid)
        #while(1):

        try:
            #根据船号查到坐标
            zuobiao_search = Shipinfo.objects.filter(id=shipid).values_list('jindu','weidu')[0]
            zuobiao_search = list(zuobiao_search)
            zuobiao_search = json.dumps(zuobiao_search)
            #从shipinfo中查找船舶信息
            ship_info = Shipinfo.objects.filter(id=shipid).values_list(
                'speed','Freight_type','ship_status','task_status','tonnage','shipname')[0]
            ship_info = list(ship_info)
            #1、根据船号查到ownerinfo_id
            ownerinfo_id = Shipinfo.objects.filter(id=shipid).values_list('ownerinfo_id')[0]
            ownerinfo_id = list(ownerinfo_id)[0]
            # 2、根据ownerinfo_id查到电话号，身份证号
            personal_info = Ownerinfo.objects.filter(id=ownerinfo_id).values_list('phone_number','identity_number','owner_name')[0]
            personal_info = list(personal_info)

            #把所有需要展示的数据统一封装到字典中
            context = {
                'speed':ship_info[0],
                'Freight_type':ship_info[1],
                'ship_status':ship_info[2],
                'task_status':ship_info[3],
                'tonnage':ship_info[4],
                'shipname':ship_info[5],
                'shipid':shipid,
                #以上是船的信息
                'phone_number': personal_info[0],
                'identity_number': personal_info[1],
                'owner_name':personal_info[2],
                #以上是船主信息
                'zuobiao_search': zuobiao_search,
                #以上是高德api需要的坐标
            }
            return render(request, 'myauth/search_result.html',
                          context)

        except ObjectDoesNotExist:

            return render(request, 'myauth/search_result.html', {'cuole':'cuole!'})

        #jindu = Article.objects.filter(id= shipid).get().title
        #weidu = Article.objects.filter(id= shipid).get().excerpt
        #jindu = jindu[:]
        #weidu = weidu[:]

        #weidu = Article.objects.filter(id= shipid).get().excerpt



        #jindu = str(jindu)


        # conn = psycopg2.connect(
        #     host='127.0.0.1',
        #     port=5432,
        #     user='postgres',
        #     password='123',
        #     database='form',
        #
        # )
        # # 获取数据
        # cur = conn.cursor()
        #
        # def insertData():
        #     cur.execute("INSERT INTO myauth_article (id,title,exce,ADDRESS,SALARY) \
        #           VALUES (1, 'Paul', 32, 'California', 20000.00 )");
        #
        #
        #
        #     conn.commit()
        #     print("Records created successfully")

        # content = {
        #     'ship':shipid,
        #     'jindu': jindu,
        #     'weidu': weidu,
        #
        # }





    else:
        return render(request,'myauth/search_result.html',{'cuole':'cuole'})

def test(request):
    if request.method == 'POST':

        shipid = request.POST.get('shipid')

        #while(1):

        try:
            jindu = Shipinfo.objects.filter(id= shipid).get().jindu
            weidu = Shipinfo.objects.filter(id= shipid).get().weidu
            return render(request, 'myauth/test.html', {'jindu': json.dumps(jindu), 'weidu': json.dumps(weidu),}
                                                        )

        except ObjectDoesNotExist:

            return render(request, 'myauth/test.html', {'cuole':'cuole!'})

        #jindu = Article.objects.filter(id= shipid).get().title
        #weidu = Article.objects.filter(id= shipid).get().excerpt
        #jindu = jindu[:]
        #weidu = weidu[:]

        #weidu = Article.objects.filter(id= shipid).get().excerpt



        #jindu = str(jindu)


        # conn = psycopg2.connect(
        #     host='127.0.0.1',
        #     port=5432,
        #     user='postgres',
        #     password='123',
        #     database='form',
        #
        # )
        # # 获取数据
        # cur = conn.cursor()
        #
        # def insertData():
        #     cur.execute("INSERT INTO myauth_article (id,title,exce,ADDRESS,SALARY) \
        #           VALUES (1, 'Paul', 32, 'California', 20000.00 )");
        #
        #
        #
        #     conn.commit()
        #     print("Records created successfully")

        # content = {
        #     'ship':shipid,
        #     'jindu': jindu,
        #     'weidu': weidu,
        #
        # }




    else:

        return render(request,'myauth/test.html')


def showall(request):
    zuobiao = Shipinfo.objects.all().values_list('jindu','weidu')
    #value_list返回queryset列表，列表中每个元素都是元组；values()得到的是一个字典形式的查询集
    #如果只传入单个字段，则还可以传入flat参数。如果为True，则表示返回的结果是单个值，而不是一个元组
    zuobiao_list = []
    for i in zuobiao:
        print(i)
        zuobiao_list.append(i)

    # 法2 发送列表给js
    # jindu_list = Shipinfo.objects.all().values('jindu')
    # jindu_list = list(jindu_list)



    return render(request,'myauth/showall.html', {'zuobiao_list': json.dumps(zuobiao_list)})
    # return render(request, 'home.html', {
    #     'List': json.dumps(List),
    #     'Dict': json.dumps(Dict)
    # })
    #return JsonResponse({'msg':'123131321!'})
    #render(request, 'myauth/ajaxsend.html', content)

def input_shipinfo(request):
    if request.POST:  # 如果数据提交

        shipid_input = request.POST.get('shipid')
        jindu_input = request.POST.get('jindu')
        weidu_input = request.POST.get('weidu')

        Freight_list = ['weixianping','huaxueping','yeti']
        Freight_selected = 666 if request.POST.get('Freight_type') in Freight_list else 0
        task_selected = request.POST.get('task_status')
        shipStatus_selected = request.POST.get('ship_status')
        print(shipid_input,Freight_selected, task_selected, shipStatus_selected,jindu_input,weidu_input)

        try:
            models.Shipinfo.objects.create(
                id=shipid_input,
                jindu=jindu_input,
                weidu=weidu_input,
                Freight_type=Freight_selected,
                ship_status=shipStatus_selected,
                task_status=task_selected,

            )
            return render(request, 'myauth/input_shipinfo.html',
                          {'prompt_message': '录入成功！'})  # your_html.html改为你的html页面并且参考前面的博客建立url链接。

        except :
            return render(request, 'myauth/input_shipinfo.html',{'errortype':'船号已存在!'})


    #else是get请求，请求访问页面
    else:
        return render(request,'myauth/input_shipinfo.html')
