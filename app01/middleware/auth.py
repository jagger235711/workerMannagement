from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


class LoginRequiredMiddleware(MiddlewareMixin):
    """
    用户登录验证中间件

    注意吧不需要登陆验证的页面排除
    """

    def process_request(self, request):
        exception_list = [
            '/login/',
            '/verification_code/',
        ]
        # 获取当前相对路径
        if request.path in exception_list:
            return
        user_info = request.session.get("user_info", "")
        if user_info:
            return

        return redirect('/login/', )
