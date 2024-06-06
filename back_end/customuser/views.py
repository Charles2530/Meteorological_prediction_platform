import json
import os
from datetime import datetime

from django.conf import settings
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied, ValidationError
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.paginator import Paginator
from django.core.validators import validate_email
from django.db.models.base import Model as Model
from django.http import HttpResponse, JsonResponse
from django.utils.deconstruct import deconstructible
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework import status, HTTP_HEADER_ENCODING
from rest_framework.authtoken.models import Token
from rest_framework.validators import ValidationError
from rest_framework_simplejwt.tokens import AccessToken

from .models import UserAvatar, UserCurrentCity


# Create your views here.
def index(request):
    return HttpResponse("User Homepage")


def validate_user_input(username, password, email, role):
    if not username or not isinstance(username, str):
        raise ValidationError("Invalid username format")
    if not password or not isinstance(password, str):
        raise ValidationError("Invalid password format")
    # 其他验证逻辑...


@csrf_exempt
@require_http_methods(["POST"])
def my_login(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return JsonResponse({"success": False, "reason": "需要用户名和密码"}, status=400)

        validate_user_input(username, password, None, None)  # 需要定义这个函数

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            info = {
                "token": str(AccessToken.for_user(user)),
                # "token": user.username,
                "userInfo": {
                    "username": user.username,
                    "avatar": "http://dummyimage.com/88x31",  # UserAvatar.objects.get(user=user).avatar, TODO
                    # "role": 2 if user.is_staff else 1,
                    "role": 2 if user.is_staff else 1,
                    "email": user.email
                }
            }
            return JsonResponse({"success": True, "info": info})
        else:
            return JsonResponse({"success": False, "reason": "用户名或密码错误，请重新输入"}, status=200)

    except ValidationError as e:
        return JsonResponse({"success": False, "reason": str(e)}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({"success": False, "reason": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"success": False, "reason": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def my_register(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        role = data.get('role', 1)

        if not username or not isinstance(username, str):
            return JsonResponse({"success": False, "reason": "Invalid username format"}, status=400)

        if not password or not isinstance(password, str):
            return JsonResponse({"success": False, "reason": "Invalid password format"}, status=400)

        # return JsonResponse({"success": True, "reason": "pass test"}, status=200)

        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({"success": False, "reason": "Invalid email format"}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({"success": False, "reason": "Username already exists"}, status=400)

        if role == 2:
            new_user = User.objects.create_superuser(username=username, password=password, email=email)
        else:
            new_user = User.objects.create_user(username=username, password=password, email=email)
        # new_user.save()
        user_current_city = UserCurrentCity(
            user=new_user,
            cityName='北京市',
            adm2='北京'
        )
        user_current_city.save()
        user_avatar = UserAvatar(
            user=new_user,
            avatar="http://dummyimage.com/88x31"
        )
        user_avatar.save()
        # authenticate(username=username, password=password)
        # login(request, user)

        info = {
            "token": str(AccessToken.for_user(new_user)),
            # "token": user.username,
            "userInfo": {
                "username": new_user.username,
                "avatar": UserAvatar.objects.get(user=new_user).avatar,
                "email": new_user.email,
                "role": role
            }
        }

        return JsonResponse({"success": True, "info": info}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({"success": False, "reason": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"success": False, "reason": str(e)}, status=500)


@csrf_exempt
@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def user_list(request):
    authorization = request.META.get("HTTP_AUTHORIZATION")
    if not authorization:
        return JsonResponse({"error": "Authorization header is required."}, status=401)

    try:
        data = json.loads(request.body)
        page = data.get('page')
        page_size = data.get('page_size')
        email = data.get('email')
        role = data.get('role')
        uid = data.get('id')
        username = data.get('username')
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format in request body."}, status=400)

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

    system_admin = ['ziwei']  # exclude django admin

    # 遍历当前页的用户，构造userlist
    for user in page_obj:
        if user.username in system_admin:
            continue
        user_data = {
            "uid": user.id,
            "username": user.username,
            "email": user.email,
            "avatar": "http://dummyimage.com/88x31",  # UserAvatar.objects.get(user=user).avatar, TODO
            "role": 2 if user.is_staff else 1,
            "last_login": user.last_login.strftime(
                '%Y-%m-%d %H:%M:%S') if user.last_login is not None else datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        response_json['userlist'].append(user_data)

    return JsonResponse(response_json, status=200)


@csrf_exempt
@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
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
        user = request.user
        if uid == user.id:  # 删除当前用户，不允许
            response_data = {
                "success": False,
                "reason": "不能删除当前用户"
            }
        else:
            target_user = User.objects.get(id=uid)
            target_user.delete()
            response_data = {"success": True}

        return JsonResponse(response_data, status=200)  # 返回200成功响应
    except User.DoesNotExist:
        # 如果用户不存在，设置success为False
        response_data = {"success": False}
        return JsonResponse(response_data, status=404)  # 返回404用户不存在


@csrf_exempt
@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def user_authorization(request):
    authorization = request.META.get("HTTP_AUTHORIZATION")
    if not authorization:
        return JsonResponse({"error": "Authorization header is required."}, status=401)

    # 从请求体中获取uid和role
    try:
        data = json.loads(request.body)
        uid = data.get('uid')
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
        # TODO: backend authorization
        user = User.objects.get(id=uid)
        if role == 1:
            user.is_staff = False
            user.is_superuser = False
        elif role == 2:
            user.is_staff = True
            user.is_superuser = True
        user.save()
        response_data = {"success": True}
        return JsonResponse(response_data, status=200)
    except User.DoesNotExist:
        response_data = {"success": False, "error": "User not found."}
        return JsonResponse(response_data, status=404)  # 返回404未找到
    except:
        # 如果用户存在但角色不匹配，返回403禁止
        response_data = {"success": False, "error": "Role does not match."}
        return JsonResponse(response_data, status=403)  # 返回403禁止


@csrf_exempt  # 禁用CSRF令牌检查，因为这是API视图
@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def update_user_email(request):
    authorization = request.META.get("HTTP_AUTHORIZATION")
    if not authorization:
        return JsonResponse({"success": False, "reason": "Authorization header is required."}, status=401)

    try:
        data = json.loads(request.body)
        user = request.user
        uid = data.get('uid')
        new_email = data.get('email')

        # 验证邮箱格式
        try:
            validate_email(new_email)
        except ValidationError:
            return JsonResponse({"success": False, "reason": "manage.user.operate.email.format"}, status=400)

        if not user.is_staff:
            raise PermissionDenied(
                "User does not have the permission to change email.")

        try:
            user = User.objects.get(id=uid)
        except User.DoesNotExist:
            return JsonResponse({"success": False, "reason": request.POST}, status=400)

        user.email = new_email
        user.save()

        return JsonResponse({"success": True}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"success": False, "reason": "Invalid JSON format in request body."}, status=400)
    except PermissionDenied as e:
        return JsonResponse({"success": False, "reason": str(e)}, status=403)
    except Exception as e:
        # 其他错误
        return JsonResponse({"success": False, "reason": "other user"}, status=400)


@csrf_exempt
# @login_required
# @user_passes_test(lambda u: u.is_staff or u.is_superuser)
def update_user_password(request):
    authorization = request.META.get("HTTP_AUTHORIZATION")

    data = json.loads(request.body)
    user = request.user
    uid = data.get('uid')
    password = data.get('password')

    if not user.is_staff or not user.is_superuser:
        return JsonResponse({"success": False, "reason": "当前用户无权限"}, status=403)

    try:
        target_user = User.objects.get(id=uid)
    except User.DoesNotExist:
        return JsonResponse({"success": False, "reason": "用户不存在"}, status=400)

    # check password
    # if not password or len(password) < 8:  # 假设密码至少8位
    #     return JsonResponse({"success": False, "reason": "manage.user.operate.password.format"}, status=400)

    # target_user.set_password(password)
    target_user.password = password
    target_user.save()

    return JsonResponse({"success": True}, status=200)


@csrf_exempt
@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def delete_data(request):
    pid = request.META.get("HTTP_PID")

    if not pid:
        return JsonResponse({"success": False}, status=400)

    try:
        item = User.objects.get(id=pid)
        item.delete()
        return JsonResponse({"success": True}, status=200)  # 如果删除成功，返回200成功
    except User.DoesNotExist:
        return JsonResponse({"success": False}, status=404)


@csrf_exempt
@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def user_info(request):
    auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    if not auth_header:
        return JsonResponse({'reason': '当前尚未登录'}, status=200)

    # try:
    #     auth_header = auth_header.decode(HTTP_HEADER_ENCODING)
    #     # token = auth_header.split(' ')[1]  # 假设token在Authorization头的'Bearer '之后
    # except (UnicodeDecodeError, AttributeError, IndexError):
    #     return JsonResponse({'reason': 'manage.invalid'}, status=400)

    # try:
    #     # 使用Django REST framework的token认证系统解析token
    #     user = Token.objects.get(key=token).user
    # except Token.DoesNotExist:
    #     return JsonResponse({'reason': 'Token not valid or expired.'}, status=401)
    user = request.user

    # 准备返回的用户信息
    user_list_json = {
        "username": user.username,
        "avatar": UserAvatar.objects.get(user=user).avatar,
        "role": 2 if user.is_staff else 1,
        "email": user.email
    }

    return JsonResponse(user_list_json)


@csrf_exempt
# @login_required
@require_http_methods(["POST"])
def update_current_user_password(request):
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

    user = request.user

    # 验证旧密码
    # if not user or not check_password(old_password, new_password):
    if not user:
        return JsonResponse({
            "success": False,
            "reason": _("userInfo.operate.password.auth")
        }, status=400)

    # # 验证新密码格式（例如，密码长度或复杂性要求）
    # if not new_password or len(new_password) < 8:  # 假设密码长度至少8位
    #     return JsonResponse({
    #         "success": False,
    #         "reason": _("userInfo.operate.password.format")
    #     }, status=400)

    # 更新用户密码
    try:
        # user.set_password(new_password)
        user.password = new_password
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


# @csrf_exempt
@login_required
@require_http_methods(["POST"])
def update_current_user_email(request):
    print(request)
    auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    data = json.loads(request.body)
    email = data.get('email')

    if not auth_header:
        return JsonResponse({
            "success": False,
            "reason": "Authorization header is missing"
        }, status=401)

    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse({
            "success": False,
            "reason": "manage.user.operate.email.format"
        }, status=400)

    user = request.user

    try:
        user.email = email
        user.save()
        return JsonResponse({
            "success": True,
            "reason": ""  # 成功时reason字段可以为空字符串
        })
    except Exception as e:
        return JsonResponse({
            "success": False,
            "reason": str(e)
        }, status=500)


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def update_current_user_avatar(request):
    auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    if not auth_header:
        return JsonResponse({
            "success": False,
            "reason": "Authorization header is missing"
        }, status=401)

    file = request.FILES.get('file')
    if not file:
        return JsonResponse({"success": False, "reason": "No file uploaded"}, status=400)

    user = request.user
    file_path = f'avatars/{user.id}/{file.name}'
    path = default_storage.save(file_path, ContentFile(file.read()))
    avatar_url = request.build_absolute_uri(settings.MEDIA_URL + path)

    try:
        user_avatar = UserAvatar.objects.get(user=user),
        print('-----', user_avatar, '-----')
        user_avatar.avatar = avatar_url
        user_avatar.save()

        return JsonResponse({
            "success": True,
            "avatar": user_avatar.avatar,
            "reason": "elit"
        })
    except Exception as e:
        return JsonResponse({
            "success": False,
            "reason": str(e),
        }, status=500)


@deconstructible
class OverwriteStorage(object):
    def __call__(self, name):
        if not name:
            raise ValueError("Storage path cannot be empty")
        return os.path.join(name)


@csrf_exempt
@login_required
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


@csrf_exempt
@login_required
def update_current_city(request):
    # auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    data = json.loads(request.body)
    new_current_city = data.get('city')

    city = new_current_city.split()[0]
    if new_current_city.find(' ') != -1:
        adm2 = new_current_city.split()[1]
        # if adm2.find('区') != -1:
        #     adm2 += '区'  # TODO fix area
    else:
        adm2 = ''
    user_current_city = UserCurrentCity.objects.get(user=request.user)
    user_current_city.cityName = city
    user_current_city.adm2 = adm2
    user_current_city.save()

    json_response = {
        "success": True,
        "reason": ""
    }

    return JsonResponse(json_response, status=200)
