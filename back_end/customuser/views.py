import json
import os
from datetime import datetime
from django.conf import settings
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied, ValidationError
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.paginator import Paginator
from django.core.validators import validate_email
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http import HttpResponse, JsonResponse
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.generic import DetailView
from rest_framework import status, HTTP_HEADER_ENCODING
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import AccessToken


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
            return JsonResponse({"success": False, "reason": "Username and password required"}, status=400)

        validate_user_input(username, password, None, None)  # 需要定义这个函数

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            info = {
                "token": str(AccessToken.for_user(user)),
                "userInfo": {
                    "username": user.username,
                    "avatar": 'http://dummyimage.com/88x31',
                    "role": 2 if user.is_staff else 1,
                    "email": user.email
                }
            }
            return JsonResponse({"success": True, "info": info})
        else:
            return JsonResponse({"success": False, "reason": "Authentication failed"}, status=401)

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
        role = data.get('role', 2)  # 默认值为2，如果role字段不存在

        if not username or not isinstance(username, str):
            return JsonResponse({"success": False, "reason": "Invalid username format"}, status=400)

        if not password or not isinstance(password, str):
            return JsonResponse({"success": False, "reason": "Invalid password format"}, status=400)

        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({"success": False, "reason": "Invalid email format"}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({"success": False, "reason": "Username already exists"}, status=400)

        if role == 2:
            user = User.objects.create_superuser(username=username, password=password, email=email)
        else:
            user = User.objects.create_user(username=username, password=password, email=email)
        user.save()
        authenticate(username=username, password=password)
        login(request, user)

        info = {
            "token": str(AccessToken.for_user(user)),
            "userInfo": {
                "username": user.username,
                "avatar": 'http://dummyimage.com/88x31',
                "email": user.email,
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
def user_list(request):
    # 从请求头中获取Authorization
    authorization = request.META.get("HTTP_AUTHORIZATION")
    if not authorization:
        # 返回401未授权错误
        return JsonResponse({"error": "Authorization header is required."}, status=401)

    # 从请求体中获取数据
    try:
        data = json.loads(request.body)
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
    customUsers = User.objects.all()

    # 分页处理
    paginator = Paginator(customUsers, page_size)
    # try:
    #     page_obj = paginator.page(page)
    # except PageNotAnInteger:
    #     page_obj = paginator.page(1)  # 如果页码不是整数，默认为第一页
    # except EmptyPage:
    #     page_obj = paginator.page(paginator.num_pages)  # 如果页码超出范围，默认为最后一页
    page_obj = paginator.page(page)

    # 构造响应数据
    response_json = {
        "all": customUsers.count(),
        "now": page_obj.number,
        "page_total": paginator.num_pages,
        "page": page_obj.number,
        "userlist": []
    }

    # 遍历当前页的用户，构造userlist
    for profile in page_obj:
        user_data = {
            "uid": profile.id,
            "username": profile.username,
            "email": profile.email,
            "avatar": 'http://dummyimage.com/88x31',
            "role": 1 if profile.is_staff == 2 else 2,
            "last_login": profile.last_login.strftime(
                '%Y-%m-%d %H:%M:%S') if profile.last_login is not None else datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        response_json['userlist'].append(user_data)

    # 返回JSON格式的响应
    return JsonResponse(response_json)


@csrf_exempt
@login_required
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
        if uid == user.uid:  # 删除当前用户，不允许
            response_data = {
                "success": False,
                "reason": "Cannot delete current user"
            }
        else:
            target_user = User.objects.get(id=uid)
            target_user.delete()
            # 如果用户存在，设置success为True
            response_data = {"success": True}

        return JsonResponse(response_data, status=200)  # 返回200成功响应
    except User.DoesNotExist:
        # 如果用户不存在，设置success为False
        response_data = {"success": False}
        return JsonResponse(response_data, status=404)  # 返回404用户不存在


@csrf_exempt  # 禁用CSRF令牌检查，因为这是API视图
@login_required
@user_passes_test(lambda u: u.is_staff)
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
        # profile = Profile.objects.get(id=uid)
        # profile.role = role
        # profile.save()
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
@login_required
@user_passes_test(lambda u: u.is_staff)
def update_user_email(request):
    # 从请求头中获取Authorization
    authorization = request.META.get("HTTP_AUTHORIZATION")
    if not authorization:
        return JsonResponse({"success": False, "reason": "Authorization header is required."}, status=401)

    try:
        # 从请求体中获取uid、role和email
        data = json.loads(request.body)
        uid = data.get('uid')
        # role = Profile.objects.get(username=request.user.username).get('role') # TODO
        new_email = data.get('email')

        # 验证邮箱格式
        try:
            validate_email(new_email)
        except ValidationError:
            return JsonResponse({"success": False, "reason": "manage.user.operate.email.format"}, status=400)

        # 检查管理员权限
        # TODO
        # if role != 2:  # 假设role为1代表管理员
        #     raise PermissionDenied(
        #         "User does not have the permission to change email.")

        # 检查用户是否存在
        try:
            user = User.objects.get(id=uid)
        except User.DoesNotExist:
            return JsonResponse({"success": False, "reason": request.POST}, status=400)

        # 更新用户邮箱
        user.set_email(new_email)

        # 操作成功，返回success为True
        return JsonResponse({"success": True}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"success": False, "reason": "Invalid JSON format in request body."}, status=400)
    except PermissionDenied as e:
        # 权限不足
        return JsonResponse({"success": False, "reason": str(e)}, status=403)
    except Exception as e:
        # 其他错误
        return JsonResponse({"success": False, "reason": "other user"}, status=400)


@csrf_exempt  # 禁用CSRF令牌检查，因为这是API视图
@login_required
def update_user_password(request):
    # 从请求头中获取Authorization
    authorization = request.META.get("HTTP_AUTHORIZATION")

    # 从请求体中获取uid、role、password
    data = json.loads(request.body)
    uid = data.get('uid')
    role = data.get('role')
    password = data.get('password')

    # 验证管理员权限
    if role != 2:  # 假设role为1代表管理员
        raise PermissionDenied(
            "User does not have the permission to change password.")
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
    #     return JsonResponse({"success": False, "reason": "manage.invalid"}, status=400)
    # except PermissionDenied:
    #     return JsonResponse({"success": False, "reason": "permission.denied"}, status=403)

    # 检查用户是否存在
    try:
        target_user = User.objects.get(id=uid)
    except User.DoesNotExist:
        return JsonResponse({"success": False, "reason": "manage.invalid"}, status=400)

    # 验证密码格式
    if not password or len(password) < 8:  # 假设密码至少8位
        return JsonResponse({"success": False, "reason": "manage.user.operate.password.format"}, status=400)

    target_user.set_password(password)

    # 操作成功，返回success为True
    return JsonResponse({"success": True}, status=200)


@csrf_exempt
@login_required  # 确保用户已登录
@user_passes_test(lambda u: u.is_staff)  # 确保用户是管理员
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
@login_required
@user_passes_test(lambda u: u.is_staff)
def user_info(request):
    auth_header = request.META.get('HTTP_AUTHORIZATION', '')
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

    # 准备返回的用户信息
    user_list_json = {
        "username": user.username,
        "avatar": user.profile.avatar.url if user.profile and user.profile.avatar else "",
        "role": user.role,
        "email": user.email
    }

    return JsonResponse(user_list_json)


@csrf_exempt  # 禁用CSRF令牌检查，因为这是API视图
@login_required
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

    user = request.user

    # 验证旧密码
    if not user or not check_password(old_password, user.password):
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
@login_required
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
    user = request.user

    # 更新用户的邮箱
    try:
        user.set_email(email)
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


@csrf_exempt  # 禁用CSRF令牌检查，因为这是API视图
@login_required
@require_http_methods(["POST"])
def update_current_user_avatar(request):
    # 获取Authorization头中的token和请求体中的oldPassword和newPassword
    auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    data = json.loads(request.body)
    file = data.get('file')

    # 验证Authorization头
    if not auth_header:
        return JsonResponse({
            "success": False,
            "reason": "Authorization header is missing"
        }, status=401)

    user = request.user

    # 更新用户头像
    try:
        user.avatar = file  # 使用Django内置的密码散列
        user.save()

        # 返回成功响应
        return JsonResponse({
            "success": True,
            "avatar": "http://dummyimage.com/100x100",
            "reason": "elit"
        })
    except Exception as e:
        # 处理其他可能的异常
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
