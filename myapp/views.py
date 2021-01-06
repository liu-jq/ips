from django.shortcuts import render,redirect
from django.http import HttpResponse
import datetime
from myapp import models
from django.db.models import Count
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
import xlrd
from dateutil.relativedelta import relativedelta

import os

# Create your views here.

def index(request):

    if not request.session.get('is_login', None):
        return redirect('/myapp/login/')
    else:

        User_name = request.session['User_name']

        # 12月内排名前三区域故障展示
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        area_fb = models.Equipment_Downtime.objects.all().values('Area').annotate(count=Count('Area'))
        area_list = []
        for i in area_fb:
            temp_list = []
            temp_list.append(i['Area'])
            temp_list.append(i['count'])
            area_list.append(temp_list)

        def takesecond(elem):
            return elem[1]

        area_list.sort(key=takesecond, reverse=True)

        now = datetime.datetime.now()

        # area_dict = {}
        area_chart = [{}, {}, {}, {}, {}, {}, {}]
        area_time = []
        count = 0
        for a in area_list[1:8:1]:
            search_criteria = {}
            search_criteria['Area'] = a[0]

            area_data = []

            for m in range(0, 12):
                last_date = (now - relativedelta(months=m)).strftime("%Y-%m")

                search_criteria['From__year'] = last_date.split('-')[0]
                search_criteria['From__month'] = last_date.split('-')[1]

                a_count = models.Equipment_Downtime.objects.filter(**search_criteria).count()

                area_data.append(a_count)

            # area_dict['name'] = a[0]
            # area_dict['data'] = area_data
            #
            # area_chart.append(area_dict)

            area_chart[count]['name'] = a[0]
            area_chart[count]['data'] = area_data

            count += 1

            # print(area_chart)

        # print(area_chart)
        for m in range(0, 12):
            last_date = (now - relativedelta(months=m)).strftime("%Y-%m")
            area_time.append(last_date)


        # 区域分布占比数据
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        area_fb = models.Equipment_Downtime.objects.all().values('Area').annotate(count=Count('Area'))
        area_list = []
        for i in area_fb:
            temp_list = []
            temp_list.append(i['Area'])
            temp_list.append(i['count'])
            area_list.append(temp_list)

        def takesecond(elem):
            return elem[1]

        area_list.sort(key=takesecond,reverse=True)


        # 本日事故列表数据
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # now_date = datetime.datetime.now().strftime("%Y-%m-%d")
        now_date = "2020-07-14"
        e_downtime_all = models.Equipment_Downtime.objects.filter(From__date=now_date)

        downtime_p = Paginator(e_downtime_all, 10)
        num_pages = downtime_p.num_pages

        page_id = request.GET.get('page_id')

        if page_id:

            try:
                downtime_list = downtime_p.page(page_id)
            except PageNotAnInteger:
                downtime_list = downtime_p.page(1)
                page_id = 1
            except EmptyPage:
                downtime_list = downtime_p.page(1)
                page_id = 1

        else:
            downtime_list = downtime_p.page(1)
            page_id = 1

        # 用户数统计
        User_conut = models.User.objects.all().count()

        return render(request,'index.html', {'Equipment_Downtime': downtime_list, 'page_id': page_id, 'num_pages': num_pages,
                                             'area_list':area_list, 'User_name': User_name, 'User_count': User_conut,
                                             'area_chart':area_chart, 'area_time':area_time})

def A_t(request):
    pass

def login(request):

    if request.session.get('is_login', None):
        return redirect('/myapp/index/')
    else:
        return render(request, 'login.html')

def ulogin(request):

    if request.method == 'POST':
        Login_name = request.POST['Login_name']
        Pwd = request.POST['Pwd']

        if Login_name and Pwd:
            Login_name = Login_name.strip()

            try:
                User = models.User.objects.get(Login_name = Login_name)

                if Pwd == User.Pwd:
                    request.session['is_login'] = True
                    request.session['User_id'] = User.User_id
                    request.session['Login_name'] = User.Login_name
                    request.session['User_name'] = User.User_name

                    return redirect('/myapp/index/')

                else:
                    return render(request, 'login.html', {'msg':"密码错误或用户不存在", 'Login_name':Login_name})
            except:
                return render(request, 'login.html', {'msg':"登录错误", 'Login_name':Login_name})

def logout(request):

    if not request.session.get('is_login', None):
        return redirect('/myapp/login/')
    else:
        request.session.flush()
        return redirect('/myapp/login/')



def upload_file(request):

    if not request.session.get('is_login', None):
        return redirect('/myapp/login/')
    else:
        return  render(request, 'upload_file.html', {'action_msg':'/myapp/upload_file_option/'})

def upload_file_option(request):

    if not request.session.get('is_login', None):
        return redirect('/myapp/login/')
    else:

        t = datetime.datetime.now()
        t_str = t.strftime("%Y%m%d%H%M%S")


        if request.method == 'POST':

            my_File = request.FILES.get("my_file",None)


            if not my_File:
                return HttpResponse("no files for upload")

            my_File_name = t_str +"-" + my_File.name

            destination = open(os.path.join("excel/", my_File_name), 'wb+')
            for chunk in my_File.chunks():
                destination.write(chunk)

            destination.close()
            book = xlrd.open_workbook("excel/" + my_File_name)

            from myapp import models

            # 总览
            sheet = book.sheet_by_name("总览")
            for r in range(1, sheet.nrows):
                oid = sheet.cell(r, 0).value
                Maintenance_strategy_code = sheet.cell(r, 1).value
                Installation_position = sheet.cell(r,2).value
                Voltage_level = sheet.cell(r,3).value
                Device_type = sheet.cell(r,4).value
                Maintenance_level = sheet.cell(r,5).value
                Describe = sheet.cell(r,6).value

                from myapp import models
                models.Overview.objects.create(oid = oid, Maintenance_strategy_code = Maintenance_strategy_code,
                                                 Installation_position = Installation_position, Voltage_level = Voltage_level,
                                                 Device_type = Device_type, Maintenance_level = Maintenance_level, Describe = Describe)

            # 电机
            sheet = book.sheet_by_name("电机")
            for r in range(1, sheet.nrows):
                Voltage_level = sheet.cell(r, 0).value
                Polar_logarithm = sheet.cell(r, 1).value
                Power = sheet.cell(r,2).value

                models.ElectricMachinery.objects.create(Voltage_level = Voltage_level, Polar_logarithm = Polar_logarithm, Power = Power)

            # 电压等级
            sheet = book.sheet_by_name("电压等级")
            for r in range(1, sheet.nrows):
                Project = sheet.cell(r, 0).value
                Code = sheet.cell(r, 1).value

                models.VoltageLevel.objects.create(Project = Project, Code = Code)

            # 设备类型
            sheet = book.sheet_by_name("设备类型")
            for r in range(1, sheet.nrows):
                Name = sheet.cell(r, 0).value
                Type = sheet.cell(r, 1).value

                models.DeviceType.objects.create(Name=Name, Type=Type)

            # 设备型号
            # 设备号

            # 安装位置
            sheet = book.sheet_by_name("安装位置")
            for r in range(1, sheet.nrows):
                Installation_position = sheet.cell(r, 0).value
                Code = sheet.cell(r, 1).value
                Describe = sheet.cell(r,2).value

                models.InstallationPosition.objects.create(Installation_position = Installation_position,
                                                           Code = Code, Describe = Describe)

            # 维护等级
            sheet = book.sheet_by_name("维护等级")
            for r in range(1, sheet.nrows):
                Level = sheet.cell(r, 0).value
                Cycle = sheet.cell(r, 1).value
                Describe = sheet.cell(r, 2).value

                models.MaintenanceLevel.objects.create(Level = Level, Cycle = Cycle, Describe = Describe)

            # 检修内容
            sheet = book.sheet_by_name("检修内容")
            for r in range(1, sheet.nrows):
                Device_type = sheet.cell(r, 0).value
                Overhaul_contents_description = sheet.cell(r, 1).value

                models.OverhaulContents.objects.create(Device_type = Device_type,
                                                       Overhaul_contents_description = Overhaul_contents_description)

            # 检修类别
            sheet = book.sheet_by_name("检修类别")
            for r in range(1, sheet.nrows):
                Project_name = sheet.cell(r, 0).value
                Code = sheet.cell(r, 1).value

                models.OverhaulType.objects.create(Project_name = Project_name, Code = Code)

        return render(request, "upload_file.html", {"msg":"上传完成，到数据查询中查看！"})

def Delete_all_show(request):

    if not request.session.get('is_login', None):
        return redirect('/myapp/login/')
    else:
        return render(request, "delete-all-show.html",{"del_msg":"/myapp/delete_all_data/"})

# 清理所有表中的数据
def Delete_all_data(request):

    if not request.session.get('is_login', None):
        return redirect('/myapp/login/')
    else:

        if request.POST.get('del_C') == "ALL":

            from myapp import models

            models.Overview.objects.all().delete()
            models.ElectricMachinery.objects.all().delete()
            models.VoltageLevel.objects.all().delete()
            models.DeviceType.objects.all().delete()
            models.InstallationPosition.objects.all().delete()
            models.MaintenanceLevel.objects.all().delete()
            models.OverhaulContents.objects.all().delete()
            models.OverhaulType.objects.all().delete()

            return HttpResponse("删除成功！")
        else:

            return HttpResponse("确认失败，无法删除！")

def Show_data_Overview(request):

    if not request.session.get('is_login', None):
        return redirect('/myapp/login/')
    else:
        Overview = models.Overview.objects.all()
        return render(request, 'Show_Data_Overview.html', {'Overview':Overview})


def Show_data_ElectricMachinery(request):

    if not request.session.get('is_login', None):
        return redirect('/myapp/login/')
    else:
        ElectricMachinery = models.ElectricMachinery.objects.all()
        return render(request, 'Show_Data_ElectricMachinery.html', {'ElectricMachinery':ElectricMachinery})

def Show_data_VoltageLevel(request):

    if not request.session.get('is_login', None):
        return redirect('/myapp/login/')
    else:
        VoltageLevel = models.VoltageLevel.objects.all()
        return render(request, 'Show_Data_VoltageLevel.html', {'VoltageLevel':VoltageLevel})

def Show_data_DeviceType(request):

    if not request.session.get('is_login', None):
        return redirect('/myapp/login/')
    else:
        DeviceType = models.DeviceType.objects.all()
        return render(request, 'Show_Data_DeviceType.html', {'DeviceType':DeviceType})

def Show_data_InstallationPosition(request):

    if not request.session.get('is_login', None):
        return redirect('/myapp/login/')
    else:
        InstallationPosition = models.InstallationPosition.objects.all()
        return render(request, "Show_Data_InstallationPosition.html", {'InstallationPosition':InstallationPosition})

def Show_data_MaintenanceLevel(request):

    if not request.session.get('is_login', None):
        return redirect('/myapp/login/')
    else:
        MaintenanceLevel = models.MaintenanceLevel.objects.all()
        return render(request, "Show_Data_MaintenanceLevel.html", {'MaintenanceLevel':MaintenanceLevel})

def Show_data_OverhaulContents(request):

    if not request.session.get('is_login', None):
        return redirect('/myapp/login/')
    else:
        OverhaulContents = models.OverhaulContents.objects.all()
        return render(request, "Show_Data_OverhaulContents.html", {'OverhaulContents':OverhaulContents})

def Show_data_OverhaulType(request):

    if not request.session.get('is_login', None):
        return redirect('/myapp/login/')
    else:
        OverhaulType = models.OverhaulType.objects.all()
        return render(request, "Show_Data_OverhaulType.html", {'OverhaulType':OverhaulType})

def Logs_show(request):

    if not request.session.get('is_login', None):
        return redirect('/myapp/login/')
    else:
        return render(request, "logs-show.html")

def Documentation(request):

    if not request.session.get('is_login', None):
        return redirect('/myapp/login/')
    else:
        return render(request, "documentation.html")


def Show_add_user(request):

    if not request.session.get('is_login', None):
        return redirect('/myapp/login/')
    else:
        return render(request, 'add_user.html')

def Add_user(request):

    if not request.session.get('is_login', None):
        return redirect('/myapp/login/')
    else:
        import random
        User_id = ''.join(str(random.choice(range(6))) for _ in range(10))
        Login_name = request.POST.get('ips-loginname')
        UserName = request.POST.get('ips-username')
        Email = request.POST.get('ips-email')
        Pwd = request.POST.get('ips-password')
        C_Pwd = request.POST.get('ips-confirm-password')
        Describe = request.POST.get('ips-describe')

        if Pwd == C_Pwd:
            models.User.objects.create(User_id = User_id, Login_name = Login_name, User_name = UserName, Email = Email, Pwd = Pwd, Describe = Describe)
            return render(request, 'Show_User.html')
        else:
            return render(request, 'add_user.html', {'ERROR_info':"两次密码错误，重新输入！", 'Login_name':Login_name, 'Email':Email, 'UserName':UserName, 'Describe':Describe})

def Show_user(request):

    if not request.session.get('is_login', None):
        return redirect('/myapp/login/')
    else:
        User = models.User.objects.all()
        return render(request, 'Show_User.html', {'User':User})