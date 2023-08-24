"""
自定义的分页组件
"""
import copy

from django.utils.safestring import mark_safe


class Pagination(object):

    def __init__(self, request, queryset, page_param="page", page_size=8, plus=5, ):
        """
        实例化类时调用
        :param request:浏览器的request对象
        :param queryset:查询的数据集
        :param page_param: URL中页码的参数名
        :param page_size: 每页数据条数
        :param plus: 页码左右两边显示的页码数
        """
        self.query_dict = copy.deepcopy(request.GET)
        self.query_dict._mutable = True
        # self.query_dict.update({"q": 138})
        # print(self.query_dict)

        # self.query_url = request.GET.urlencode()
        self.page_param = page_param

        page = request.GET.get(page_param, "1")
        if page.isdecimal():
            page = int(page)
            # print(page, type(page))
        else:
            page = 1
        self.page = page
        self.page_size = page_size

        self.start = (page - 1) * page_size
        self.end = page * page_size
        self.page_queryset = queryset[self.start:self.end]

        # 数据总条数
        total_count = queryset.count()

        # 总页数
        # 计算总页数
        # 总页数 = 数据总条数 / 每页显示的数据条数
        # 向上取整
        total_page_count, div = divmod(total_count, page_size)
        if div:
            total_page_count += 1

        self.total_page_count = total_page_count
        self.plus = plus

    def gennerate_html(self):
        """
        生成分页的html
        :return: page_string  分页的html
        """
        # 向页面中生成页码
        page_str_list = []
        # 显示当前页面前和后plus页

        if self.total_page_count <= 2 * self.plus + 1:
            # 当总页数小于应显示的页数
            start_page = 1
            end_page = self.total_page_count
        else:
            start_page = self.page - self.plus
            end_page = self.page + self.plus
            # 当前或后不足五页时不改变起始和中止页
            if start_page < 1:
                start_page = 1
                end_page = 2 * self.plus + 1
            if end_page > self.total_page_count:
                start_page = self.total_page_count - 2 * self.plus
                end_page = self.total_page_count
        page_str_list.append(
            """
             <div style="display: flex; justify-content: center;">
               
                    <ul class="pagination">
            """
        )

        # 首页
        # self.query_dict.update({self.page_param: 1})
        # print(self.query_dict.urlencode())
        self.query_dict[self.page_param] = 1
        page_str_list.append(
            ' <li class="page-item"><a class="page-link" href="?{}">首页</a></li>'.format(self.query_dict.urlencode()))
        # 上一页
        if self.page > 1:
            # update_dict = {self.page_param: [str(self.page - 1)]}
            self.query_dict[self.page_param] = self.page - 1

        else:
            self.query_dict[self.page_param] = 1
        page_str_list.append(
            """
            <li class="page-item">
                <a class="page-link" href="?{}" aria-label="Previous">
                    <span aria-hidden="true">&laquo;</span>
                </a>
            </li>
            """.format(
                self.query_dict.urlencode()))

        # < li class ="page-item" > < a class ="page-link" href="#" > 2 < /a > < /li >
        # 展示前后五页

        for i in range(start_page, end_page + 1):
            self.query_dict[self.page_param] = i
            if i == self.page:
                ele = '<li class ="page-item active"><a class ="page-link" href="?{}">{}</a></li>'.format(
                    self.query_dict.urlencode(), i)
            else:
                ele = '<li class ="page-item"><a class ="page-link" href="?{}">{}</a></li>'.format(
                    self.query_dict.urlencode(), i)
            page_str_list.append(ele)

        # 下一页
        if self.page < self.total_page_count:
            self.query_dict[self.page_param] = self.page + 1
        else:
            self.query_dict[self.page_param] = self.total_page_count
        page_str_list.append(
            """
                <li class="page-item">
                    <a class="page-link" href="?{}" aria-label="Next">
                        <span aria-hidden="true">&raquo;</span>
                    </a>
                </li>
            """.format(
                self.query_dict.urlencode()))

        # 尾页
        self.query_dict[self.page_param] = self.total_page_count
        page_str_list.append(
            ' <li class="page-item"><a class="page-link" href="?{}">尾页</a></li>'.format(
                self.query_dict.urlencode()))

        page_str_list.append(
            """
                       </ul>
            </div>
            """
        )

        page_string = mark_safe("".join(page_str_list))  # 标记为安全才会被网页解析
        return page_string
