from django.db import models

# Create your models here.

# 总览
class Overview(models.Model):
    # 序号
    oid = models.IntegerField()
    # 维护策略代码
    Maintenance_strategy_code = models.CharField(max_length=20)
    # 安装位置
    Installation_position = models.CharField(max_length=50)
    # 电压等级
    Voltage_level = models.IntegerField()
    # 设备类型
    Device_type = models.CharField(max_length=10)
    # 维修等级
    Maintenance_level = models.IntegerField()
    # 描述
    Describe = models.TextField()
    #添加时间
    Add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ips_Overview'

# 电机
class ElectricMachinery(models.Model):
    # 电压等级
    Voltage_level = models.IntegerField()
    # 极对数
    Polar_logarithm = models.IntegerField()
    # 功率
    Power = models.FloatField()
    # 添加时间
    Add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ips_ElectricMachinery'

# 电压等级
class VoltageLevel(models.Model):
    # 项目
    Project = models.CharField(max_length=10)
    # 代码
    Code = models.CharField(max_length=6)
    # 添加时间
    Add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ips_VoltageLevel'

# 设备类型
class DeviceType(models.Model):
    # 名称
    Name = models.CharField(max_length=20)
    # 类型
    Type = models.CharField(max_length=10)
    # 添加时间
    Add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ips_DeviceType'

# 设备型号 DeviceModel

# 设备号 DeviceNum

# 安装位置
class InstallationPosition(models.Model):
    # 安装位置
    Installation_position = models.CharField(max_length=20)
    # 代码
    Code = models.CharField(max_length=6)
    # 描述
    Describe = models.TextField()
    # 添加时间
    Add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ips_InstallationPosition'

# 维护等级(MaintenanceLevel)
class MaintenanceLevel(models.Model):
    # 等级
    Level = models.CharField(max_length=6)
    # 周期
    Cycle = models.IntegerField()
    # 描述
    Describe = models.TextField()
    # 添加时间
    Add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ips_MaintenanceLevel'

# 检修内容(OverhaulContents)
class OverhaulContents(models.Model):
    # 设备类型
    Device_type = models.CharField(max_length=20)
    # 检修内容描述
    Overhaul_contents_description = models.TextField()
    # 添加时间
    Add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ips_OverhaulContents'

# 检修类别(OverhaulType)
class OverhaulType(models.Model):
    # 项目
    Project_name = models.CharField(max_length=20)
    # 代码
    Code = models.CharField(max_length=6)
    # 添加时间
    Add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ips_OverhaulType'


# 用户表
class User(models.Model):
    User_id = models.CharField(max_length=32)
    Login_name = models.CharField(max_length=20)
    User_name = models.CharField(max_length=20)
    Pwd = models.CharField(max_length=32)
    Email = models.CharField(max_length=32)
    Describe = models.TextField()
    # 添加时间
    Add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ips_User'

# 日志表
class LogContext(models.Model):
    # 操作用户
    op_user = models.CharField(max_length=20)
    # 操作内容
    op = models.CharField(max_length=64)
    # 添加时间
    Add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ips_LogContext'

# 事故记录表
class Equipment_Downtime(models.Model):
    # 区域
    Area = models.CharField(max_length=20)
    # 设备编号
    Main_Equipment_ID = models.CharField(max_length=20)
    # 设备类型
    Fault_Equipment_Type = models.CharField(max_length=20)
    # 事故各类
    Fault_Type = models.CharField(max_length=20)
    # 事故子种类
    Sub_Fault_Type = models.CharField(max_length=64)
    # 描述
    Descriptions = models.CharField(max_length=2048)
    # 是否已维修
    Fixed = models.CharField(max_length=20)
    Line = models.CharField(max_length=20)
    # 导致停产
    Caused_New_Feed_Offline = models.CharField(max_length=20)
    From = models.DateTimeField()
    To = models.DateTimeField()
    Down_time = models.CharField(max_length=10)
    class Meta:
        db_table = 'ips_Equipment_Downtime'