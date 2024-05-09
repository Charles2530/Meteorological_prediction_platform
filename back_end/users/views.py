# Django核心和框架相关的导入
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied, ValidationError
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.paginator import Paginator
from django.core.validators import validate_email
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

# Django REST framework相关的导入
from rest_framework import status, HTTP_HEADER_ENCODING
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny  # 允许所有用户访问
from rest_framework_simplejwt.tokens import RefreshToken

# Django HTTP相关的导入
from django.http import HttpResponse, JsonResponse

# 其他Python标准库导入
import json
import os
import re
from datetime import datetime

from users.models import UserCity


# Create your views here.
def index(request):
    return HttpResponse("User Homepage")


@csrf_exempt
def my_login(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')

    # 验证用户名格式
    if not username or not isinstance(username, str):
        return JsonResponse({
            "success": False,
            "reason": "login.error.format"
        }, status=400)

    # 验证用户名和密码
    user = authenticate(username=username, password=password)
    # user = User.objects.filter(username=username, password=password).first()
    if user is not None:
        # 登录成功
        # settings.CURRENT_UNAME = user.username
        login(request, user)

        # register current city
        if not UserCity.objects.filter(username=username).exists():
            user_city = UserCity(username=username, city='北京')
            user_city.save()

        info = {
            "token": "aliqua commodo Lorem",
            "userInfo": {
                "username": username,
                "avatar": "http://dummyimage.com/88x31",
                "role": 2,  # 这里根据实际情况设置用户的角色
                "email": user.email
            }
        }
        return JsonResponse({
            "success": True,
            "info": info
        })
    else:
        # 登录失败
        # settings.CURRENT_UNAME = None
        return JsonResponse({
            "success": False,
            "reason": "login.error.auth"
        }, status=401)


@csrf_exempt
@require_http_methods(["POST"])
def my_register(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    # 验证邮箱格式
    # try:
    #     validate_email(email)
    # except ValidationError:
    #     return JsonResponse({
    #         "success": False,
    #         "reason": "register.error.email"
    #     }, status=400)

    # 验证用户名和密码格式
    if not username or not isinstance(username, str):
        return JsonResponse({
            "success": False,
            "reason": "register.error.format"
        }, status=400)

    if not password or not isinstance(password, str):
        return JsonResponse({
            "success": False,
            "reason": "register.error.format"
        }, status=400)

    # 检查用户名是否已存在
    if User.objects.filter(username=username).exists():
        return JsonResponse({
            "success": False,
            "reason": "register.error.samename"
        }, status=400)

    # 创建用户
    new_user = User.objects.create_user(
        username=username, email=email, password=password)
    # authenticate(username=username, password=password)
    
    # settings.CURRENT_UNAME = new_user.username
 

    # 准备返回的信息
    info = {
        "token": str(RefreshToken.for_user(new_user)),
        "userInfo": {
            "username": new_user.username,
            "avatar": "",  # todo
            "email": new_user.email,
            "role": 2
        }
    }

    # 返回JSON响应
    return JsonResponse({
        "success": True,
        "info": info,
        "reason": ""  # 当成功时，reason字段可以为空字符串
    }, status=201)


@csrf_exempt
def user_list(request):
    # 从请求头中获取Authorization
    authorization = request.META.get("HTTP_AUTHORIZATION")  # 【1】
    if not authorization:
        # 返回401未授权错误
        return JsonResponse({"error": "Authorization header is required."}, status=401)

    # 从请求体中获取数据
    try:
        data = json.loads(request.body)  # 【2】
        page = data.get('page')
        page_size = data.get('page_size')
        email = data.get('email')
        role = data.get('role')
        uid = data.get('id')
        username = data.get('username')
    except json.JSONDecodeError:
        # 返回400错误，请求格式不正确
        return JsonResponse({"error": "Invalid JSON format in request body."}, status=400)
    
    # 获取用户数据
    users = User.objects.all()

    # 分页处理
    paginator = Paginator(users, page_size)
    # try:
    #     page_obj = paginator.page(page)
    # except PageNotAnInteger:
    #     page_obj = paginator.page(1)  # 如果页码不是整数，默认为第一页
    # except EmptyPage:
    #     page_obj = paginator.page(paginator.num_pages)  # 如果页码超出范围，默认为最后一页
    page_obj = paginator.page(page)

    # 构造响应数据
    response_json = {
        "all": users.count(),
        "now": page_obj.number,
        "page_total": paginator.num_pages,
        "page": page_obj.number,
        "userlist": []
    }

    # 遍历当前页的用户，构造userlist
    for user in page_obj:
        user_data = {
            "uid": user.id,
            "username": user.username,
            "email": user.email,
            "avatar": "https://charles2530.github.io/image/background/logo2.jpg",
            "role": 2,
            "last_login": user.last_login.strftime('%Y-%m-%d %H:%M:%S') if user.last_login != None else datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        response_json['userlist'].append(user_data)

    # 返回JSON格式的响应
    return JsonResponse(response_json)


@csrf_exempt
def delete_user(request):
    # 从请求头中获取Authorization
    authorization = request.META.get("HTTP_AUTHORIZATION")
    if not authorization:
        # 返回401未授权错误
        return JsonResponse({"error": "Authorization header is required."}, status=401)

    # 从请求体中获取uid
    try:
        data = json.loads(request.body)
        uid = data.get('uid')
    except json.JSONDecodeError:
        # 返回400错误，请求格式不正确
        return JsonResponse({"error": "Invalid JSON format in request body."}, status=400)

    if not uid:
        # 返回400错误，缺少UID参数
        return JsonResponse({"error": "UID parameter is required."}, status=400)

    # 添加业务逻辑，例如根据uid获取用户信息等
    # 假设这里仅检查User模型中是否存在对应的uid
    try:
        user = User.objects.get(id=uid)
        user.delete()
        # 如果用户存在，设置success为True

        response_data = {"success": True}
        return JsonResponse(response_data, status=200)  # 返回200成功响应
    except User.DoesNotExist:
        # 如果用户不存在，设置success为False
        response_data = {"success": False}
        return JsonResponse(response_data, status=404)  # 返回404用户不存在


@csrf_exempt  # 禁用CSRF令牌检查，因为这是API视图
def user_authorization(request):
    # 从请求头中获取Authorization
    authorization = request.META.get("HTTP_AUTHORIZATION")
    if not authorization:
        # 返回401未授权错误
        return JsonResponse({"error": "Authorization header is required."}, status=401)

    # 从请求体中获取uid和role
    try:
        data = json.loads(request.body)
        uid = data.get('id')
        role = data.get('role')
    except json.JSONDecodeError:
        # 返回400错误，请求格式不正确
        return JsonResponse({"error": "Invalid JSON format in request body."}, status=400)

    if not uid or not role:
        # 返回400错误，缺少必要参数
        return JsonResponse({"error": "UID and role parameters are required."}, status=400)

    # 在这里添加你的业务逻辑，例如验证用户权限等
    # 假设我们只是简单地检查User模型中是否存在对应的uid和role
    try:
        # TODO:
        # user = User.objects.get(id=uid, role=role)
        user = User.objects.get(id=uid)
        # 如果用户存在且角色匹配，设置success为True
        response_data = {"success": True}
        return JsonResponse(response_data, status=200)  # 返回200成功响应
    except User.DoesNotExist:
        # 如果用户不存在，返回404未找到
        response_data = {"success": False, "error": "User not found."}
        return JsonResponse(response_data, status=404)  # 返回404未找到
    except:
        # 如果用户存在但角色不匹配，返回403禁止
        response_data = {"success": False, "error": "Role does not match."}
        return JsonResponse(response_data, status=403)  # 返回403禁止


@csrf_exempt  # 禁用CSRF令牌检查，因为这是API视图
def update_user_email(request):
    # 从请求头中获取Authorization
    authorization = request.META.get("HTTP_AUTHORIZATION")
    if not authorization:
        return JsonResponse({"success": False, "reason": "Authorization header is required."}, status=401)

    try:
        # 从请求体中获取uid、role和email
        data = json.loads(request.body)
        uid = data.get('uid')
        role = data.get('role')
        new_email = data.get('email')

        # 验证邮箱格式
        try:
            validate_email(new_email)
        except ValidationError:
            return JsonResponse({"success": False, "reason": "manage.user.operate.email.format"}, status=400)

        # # 检查管理员权限
        # if role != 1:  # 假设role为1代表管理员
        #     raise PermissionDenied(
        #         "User does not have the permission to change email.")

        # 检查用户是否存在
        try:
            user = User.objects.get(id=uid)
        except User.DoesNotExist:
            return JsonResponse({"success": False, "reason": request.POST}, status=400)

        # 更新用户邮箱
        user.email = new_email
        user.save()

        # 操作成功，返回success为True
        return JsonResponse({"success": True}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"success": False, "reason": "Invalid JSON format in request body."}, status=400)
    except PermissionDenied as e:
        # 权限不足
        return JsonResponse({"success": False, "reason": str(e)}, status=403)
    except Exception as e:
        # 其他错误
        # 你需要在你的urls.py文件中添加URL配置，以便将请求映射到这个视图函数
        return JsonResponse({"success": False, "reason": "other user"}, status=400)


@csrf_exempt  # 禁用CSRF令牌检查，因为这是API视图
def update_user_password(request):
    # 从请求头中获取Authorization
    authorization = request.META.get("HTTP_AUTHORIZATION")

    # 从请求体中获取uid、role、password
    data = json.loads(request.body)
    uid = data.get('uid')
    role = data.get('role')
    password = data.get('password')

    # # 验证管理员权限
    # try:
    #     # 假设我们通过某种方式验证管理员的Authorization
    #     # 例如，使用Django的authenticate函数，或者自定义的验证逻辑
    #     admin_user = User.objects.get(id=uid)
    #     if not check_password(authorization, admin_user.password):
    #         raise PermissionDenied

    #     # 检查管理员角色
    #     if not admin_user.is_staff:  # 假设is_staff属性表示管理员
    #         raise PermissionDenied
    # except User.DoesNotExist:
    #     return JsonResponse({"success": False, "reason": "manage.invaild"}, status=400)
    # except PermissionDenied:
    #     return JsonResponse({"success": False, "reason": "You do not have permission to perform this action."}, status=403)

    # 检查用户是否存在
    try:
        user_to_update = User.objects.get(id=uid)
    except User.DoesNotExist:
        return JsonResponse({"success": False, "reason": "manage.invaild"}, status=400)

    # 验证密码格式
    if not password or len(password) < 8:  # 假设密码至少8位
        return JsonResponse({"success": False, "reason": "manage.user.operate.password.format"}, status=400)

    # 更新用户密码
    # user_to_update.password = make_password(password)
    user_to_update.password = password
    user_to_update.save()

    # 操作成功，返回success为True
    return JsonResponse({"success": True}, status=200)


@csrf_exempt
@login_required  # 确保用户已登录
# @user_passes_test(lambda u: u.is_staff)  # 确保用户是管理员
def delete_data(request):
    # 从请求头中获取pid
    pid = request.META.get("HTTP_PID")

    if not pid:
        # 如果缺少pid参数，返回400错误
        return JsonResponse({"success": False}, status=400)

    try:
        # 根据pid获取数据并删除
        item = User.objects.get(pid=pid)
        item.delete()
        return JsonResponse({"success": True}, status=200)  # 如果删除成功，返回200成功
    except User.DoesNotExist:
        return JsonResponse({"success": False}, status=404)  # 如果数据不存在，返回404错误
    except Exception as e:
        # 其他错误
        return JsonResponse({"success": False}, status=500)  # 返回500服务器错误

@csrf_exempt  # 禁用CSRF令牌检查，因为这是API视图
def user_info(request):
    auth_header = request.META.get('HTTP_AUTHORIZATION','')
    if not auth_header:
        return JsonResponse({'reason': 'manage.invalid'}, status=400)

    try:
        auth_header = auth_header.decode(HTTP_HEADER_ENCODING)
        token = auth_header.split(' ')[1]  # 假设token在Authorization头的'Bearer '之后
    except (UnicodeDecodeError, AttributeError, IndexError):
        return JsonResponse({'reason': 'manage.invalid'}, status=400)

    try:
        # 使用Django REST framework的token认证系统解析token
        user = Token.objects.get(key=token).user
    except Token.DoesNotExist:
        return JsonResponse({'reason': 'Token not valid or expired.'}, status=401)

    # 验证邮箱格式
    if not re.match(r"[^@]+@[^@]+\.[^@]+", user.email):
        return JsonResponse({'reason': 'manage.user.operate.email.format'}, status=400)

    # 准备返回的用户信息
    user_info = {
        "username": user.username,
        # 假设有一个profile模型关联了用户和头像
        "avatar": user.profile.avatar.url if user.profile and user.profile.avatar else "",
        "role": user.role,  # 假设用户模型有一个role字段
        "email": user.email
    }

    return JsonResponse(user_info)


@csrf_exempt  # 禁用CSRF令牌检查，因为这是API视图
@require_http_methods(["POST"])
def update_current_user_password(request):
    # 获取Authorization头中的token和请求体中的oldPassword和newPassword
    auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    data = json.loads(request.body)
    old_password = data.get('oldPassword')
    new_password = data.get('newPassword')

    # 验证Authorization头
    if not auth_header:
        return JsonResponse({
            "success": False,
            "reason": "Authorization header is missing"
        }, status=401)

    # user = User.objects.filter(username=settings.CURRENT_UNAME).first()
    # user = User.objects.filter(username=request.user.username).first()
    user= request.user

   
    # # 验证旧密码
    # if not user or not check_password(old_password, user.password):
    #     return JsonResponse({
    #         "success": False,
    #         "reason": _("userInfo.operate.password.auth")
    #     }, status=400)

    # # 验证新密码格式（例如，密码长度或复杂性要求）
    # if not new_password or len(new_password) < 8:  # 假设密码长度至少8位
    #     return JsonResponse({
    #         "success": False,
    #         "reason": _("userInfo.operate.password.format")
    #     }, status=400)

    # 更新用户密码
    try:
        user.password = new_password  # 使用Django内置的密码散列
        user.save()
        # 如果使用Django的session，更新session中的密码
        # update_session_auth_hash(request, user)

        # 返回成功响应
        return JsonResponse({
            "success": True
        })
    except Exception as e:
        # 处理其他可能的异常
        return JsonResponse({
            "success": False,
            "reason": str(e),
        }, status=500)


@csrf_exempt  # 禁用CSRF令牌检查，因为这是API视图
@require_http_methods(["POST"])
def update_current_user_email(request):
    # 获取Authorization头中的token和请求体中的邮箱
    auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    data = json.loads(request.body)
    email = data.get('email')

    # 验证Authorization头
    if not auth_header:
        return JsonResponse({
            "success": False,
            "reason": "Authorization header is missing"
        }, status=401)

    # 验证邮箱格式
    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse({
            "success": False,
            "reason": "manage.user.operate.email.format"
        }, status=400)

    # 假设你已经验证了token并获取了用户对象
    # user = User.objects.filter(username=settings.CURRENT_UNAME).first() # 获取当前认证的用户对象
    user=request.user

    # 更新用户的邮箱
    try:
        user.email = email
        user.save()
        return JsonResponse({
            "success": True,
            "reason": ""  # 成功时reason字段可以为空字符串
        })
    except Exception as e:
        # 处理其他可能的异常
        return JsonResponse({
            "success": False,
            "reason": str(e)
        }, status=500)


@deconstructible
class OverwriteStorage(object):
    def __call__(self, name):
        if not name:
            raise ValueError("Storage path cannot be empty")
        return os.path.join(name)


def upload_avatar(request):
    # 验证请求中是否包含文件
    if 'file' not in request.FILES:
        return JsonResponse({
            "success": False,
            "reason": "No file part found in the request"
        }, status=400)

    file = request.FILES['file']
    file_name, file_extension = os.path.splitext(file.name)
    allowed_extensions = ['.jpeg', '.jpg', '.png', '.gif']

    # 检查文件格式
    if not file_extension.lower() in allowed_extensions:
        return JsonResponse({
            "success": False,
            "reason": "userInfo.operate.avatar.type"
        }, status=400)

    # 检查文件大小
    if file.size > 2 * 1024 * 1024:  # 2MB
        return JsonResponse({
            "success": False,
            "reason": "userInfo.operate.avatar.size"
        }, status=400)

    # 保存文件
    try:
        # 使用Django的文件存储系统保存文件
        file_path = default_storage.save(file.name, ContentFile(file.read()))
        # 获取文件的URL
        avatar_url = default_storage.url(file_path)

        return JsonResponse({
            "success": True,
            "avatar": avatar_url
        })
    except Exception as e:
        # 处理其他可能的异常
        return JsonResponse({
            "success": False,
            "reason": str(e)
        }, status=500)
