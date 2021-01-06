from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
import datetime

from myapp import models
import xlrd

import os

def upload_file(request):
    if not request.session.get('is_login', None):
        return redirect('/myapp/login/')
    else:
        return  render(request, 'upload_file.html', {'action_msg':'/myapp/failure_upload_option/'})

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

            # 总览
            sheet = book.sheet_by_name("Equipment Downtime")
            for r in range(1, sheet.nrows):

                if str(sheet.cell(r, 0).value) == "":
                    Area = "-"
                else:
                    Area = str(sheet.cell(r, 0).value)

                if str(sheet.cell(r, 1).value) == "":
                    Main_Equipment_ID = "-"
                else:
                    Main_Equipment_ID = str(sheet.cell(r, 1).value)

                if str(sheet.cell(r,2).value) == "":
                    Fault_Equipment_Type = "-"
                else:
                    Fault_Equipment_Type = str(sheet.cell(r,2).value)

                if str(sheet.cell(r,3).value) == "":
                    Fault_Type = "-"
                else:
                    Fault_Type = str(sheet.cell(r,3).value)

                if str(sheet.cell(r,4).value) == "":
                    Sub_Fault_Type = "-"
                else:
                    Sub_Fault_Type = str(sheet.cell(r,4).value)

                if str(sheet.cell(r,5).value) == "":
                    Descriptions = "-"
                else:
                    Descriptions = str(sheet.cell(r,5).value)

                if str(sheet.cell(r,6).value) == "":
                    Fixed = "-"
                else:
                    Fixed = str(sheet.cell(r,6).value)

                if str(sheet.cell(r,7).value) == "":
                    Line = "-"
                else:
                    Line = str(sheet.cell(r,7).value)

                if str(sheet.cell(r,8).value) == "":
                    Caused_New_Feed_Offline = "-"
                else:
                    Caused_New_Feed_Offline = str(sheet.cell(r,8).value)

                # 日期时间的读取
                From = datetime.datetime(*xlrd.xldate_as_tuple(sheet.cell(r,9).value, 0))
                To = datetime.datetime(*xlrd.xldate_as_tuple(sheet.cell(r, 10).value, 0))

                if str(round(sheet.cell(r,11).value,2)) == "":
                    Down_time = "-"
                else:
                    Down_time = str(round(sheet.cell(r,11).value,2))

                try:
                    models.Equipment_Downtime.objects.create(Area = Area, Main_Equipment_ID = Main_Equipment_ID,
                                               Fault_Equipment_Type = Fault_Equipment_Type, Fault_Type = Fault_Type,
                                               Sub_Fault_Type = Sub_Fault_Type, Descriptions = Descriptions,
                                               Fixed = Fixed, Line = Line, Caused_New_Feed_Offline = Caused_New_Feed_Offline,
                                               From = From, To = To, Down_time = Down_time)
                except Exception as e:
                    print(Area, Main_Equipment_ID, Fault_Equipment_Type, Fault_Type, Sub_Fault_Type,
                          Descriptions, Fixed, Line, Caused_New_Feed_Offline, From, To, Down_time)
                    print(str(e))

        return render(request, "upload_file.html", {"msg":"上传完成，到数据查询中查看！"})


def Delete_all_show(request):

    if not request.session.get('is_login', None):
        return redirect('/myapp/login/')
    else:
        return render(request, "delete-all-show.html", {"del_msg": "/myapp/failure_delete_all_data/"})

def Delete_all_data(request):

    if not request.session.get('is_login', None):
        return redirect('/myapp/login/')
    else:

        if request.POST.get('del_C') == "ALL" :

            models.Equipment_Downtime.objects.all().delete()

            return render(request, "delete-all-show.html", {"return_msg": "删除成功！"})
        else:

            return render(request, "delete-all-show.html", {"return_msg": "确认失败，无法删除！"})

def Downtime_listing(request):

    if not request.session.get('is_login', None):
        return redirect('/myapp/login/')
    else:

        # 定义一个空字典
        search_criteria = {}

        # 如果查询条件不为空，把查询条件添加到字典中

        if request.GET.get('Area'):
            search_criteria['Area'] = request.GET.get('Area')

        if request.GET.get('Main_Equipment_ID'):
            search_criteria['Main_Equipment_ID'] = request.GET.get('Main_Equipment_ID')

        if request.GET.get('Fault_Equipment_Type'):
            search_criteria['Fault_Equipment_Type'] = request.GET.get('Fault_Equipment_Type')

        if request.GET.get('Fault_Type'):
            search_criteria['Fault_Type'] = request.GET.get('Fault_Type')

        if request.GET.get('Fixed'):
            search_criteria['Fixed'] = request.GET.get('Fixed')

        if request.GET.get('Caused_New_Feed_Offline'):
            search_criteria['Caused_New_Feed_Offline'] = request.GET.get('Caused_New_Feed_Offline')

        # 日期时间字段比较特殊，网页用date标签提交日期，数据库字段的格式为'%Y-%m-%d %H:%M:%S'
        # 查询的时候，需要模糊查询，忽略时间，只查当天的所有事故
        if request.GET.get('From'):

            _From = request.GET.get('From')

            search_criteria['From__date__gte'] = _From
            print("from：", _From)


        if request.GET.get('From_time'):
            _From_time = request.GET.get('From_time')
            search_criteria['From__time__gte'] = _From_time

            print("From_time:",_From_time)

        if request.GET.get('To'):
            _To = request.GET.get('To')
            search_criteria['From__date__lte'] = _To
            print("To:",_To)

        if request.GET.get('To_time'):
            _To_time = request.GET.get('To_time')
            search_criteria['From__time__lte'] = _To_time
            print("To_time",_To_time)

        if len(search_criteria) == 0:
            e_downtime_all = models.Equipment_Downtime.objects.all().order_by("-From")
        else:
            e_downtime_all = models.Equipment_Downtime.objects.filter(**search_criteria).order_by("-From")


        downtime_p = Paginator(e_downtime_all, 15)
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

        return render(request, 'Show_Data_Equipment_Downtime.html', {'Equipment_Downtime': downtime_list,
                                                                     'page_id': page_id, 'num_pages': num_pages,})

def Add_Equipment_Downtime(request):

    if not request.session.get('is_login', None):
        return redirect('/myapp/login/')
    else:
        return render(request, "add_equipment_downtime.html")

def Add_Equipment_Downtime_option(request):

    if not request.session.get('is_login', None):
        return redirect('/myapp/login/')
    else:
        Area = request.POST.get("Failure-Area")
        Main_Equipment_ID = request.POST.get("Failure-Main_Equipment_ID")
        Fault_Equipment_Type = request.POST.get("Fault-Equipment_Type")
        Fault_Type = request.POST.get("Fault-Type")
        Sub_Fault_Type = request.POST.get("Fault-Sub_Type")
        Descriptions = request.POST.get("Descriptions")
        Fixed = request.POST.get("Fault-Fixed")
        Line = request.POST.get("Fault-Line")
        Caused_New_Feed_Offline = request.POST.get("Fault-Caused_New_Feed_Offline")
        From = request.POST.get("Fault-From_date") + " " + request.POST.get("Fault-From_time") + ":00"
        To = request.POST.get("Fault-To_date") + " " + request.POST.get("Fault-To_time") + ":00"

        print(From,To)

        From = datetime.datetime.strptime(From, "%Y-%m-%d %H:%M:%S")
        To = datetime.datetime.strptime(To, "%Y-%m-%d %H:%M:%S")

        Down_time = (To - From).total_seconds()/60/60

        Down_time = str(round(Down_time, 2))

        print(Area, Main_Equipment_ID, Fault_Equipment_Type, Fault_Type,
              Sub_Fault_Type, Descriptions, Fixed, Line, Caused_New_Feed_Offline,
              From, To, Down_time)

        models.Equipment_Downtime.objects.create(Area=Area, Main_Equipment_ID=Main_Equipment_ID, Fault_Equipment_Type=Fault_Equipment_Type,
                                                 Fault_Type=Fault_Type, Sub_Fault_Type=Sub_Fault_Type, Descriptions=Descriptions,
                                                 Fixed=Fixed, Line=Line, Caused_New_Feed_Offline=Caused_New_Feed_Offline, From=From,
                                                 To=To, Down_time=Down_time)

        return render(request, "add_equipment_downtime.html", {"msg":"添加完成！"})


