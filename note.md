## 写项目流程

1. 创建项目，创建、注册app，配置静态文件、模板路径，
2. 配置数据库操作：[配置第三方模块连接数据库]，创建、连接数据库，编写models，定义数据库表，修改数据库配置，生成数据库表

    ```python
    python manage.py makemigrations
    python manage.py migrate
    ```

1. 业务模块编写
    1. 页面设计
    2. 配置url
    3. 编写对应视图函数，先不写具体功能，先把页面写出来。目标是要能看到页面，看到页面之后，再进行功能开发。
    4. 去对应视图中实现具体功能
    5. 优化，使用螺旋模型进行开发
2.

- 在 urls.py ，路由 （ URL 和 函数的对应关系）。

- 在views.py，视图函数，编写业务逻辑。

- templates目录，编写HTML模板（含有模板语法、继承、`{% static 'xx'%}`）

- ModelForm & Form组件，在我们开发增删改查功能。
  - 生成HTML标签（生成默认值）
  - 请求数据进行校验。
  - 保存到数据库（ModelForm）
  - 获取错误信息。

- Cookie和Session，用户登录信息保存起来。

- 中间件，基于中间件实现用户认证 ，基于：`process_request`。

- ORM操作

  ```
    models.User.objects.filter(id="xxx")
    models.User.objects.filter(id="xxx").order_by("-id")
  
    models.Order.objects.filter(id=orderId).first()#得到对象
    models.Order.objects.filter(id=orderId).values().first()#得到字典
  ```
  
- 分页组件。

## 捷径

1. 当设计ORM时出现了元组套元组的情况，可以使用object.get_字段名_display()来直接获得对应选项表示的字段

   ```python
   # django中定义的约束
    
    gender_choices = (
        (1, "男"),
        (2, "女")
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)
    
    
   ```

2. ORM设计时，外键数据以外键.id存储。可以以对象形式进行读取，可以用obj.字段自动跨表获取数据
3. 输出对象时，要想定义显示的内容，可以去定义__str__方法，返回字符串即可
4. 当定义了__init__方法时，实例化对象时要传入参数，否则会报错
5. 通过在model.py中对meta类添加widget字段，可以修改字段通过modelform渲染的样式
    1. 在实际生产中，更简便的方法是直接重写modelform的__init__方法，在__init__方法中传入对应的widget

   ```python
   
    class UserForm(forms.ModelForm):
           class Meta:
               model = User
               fields = ('name',)
       
           def __init__(self, *args, **kwargs):
               super().__init__(*args, **kwargs)
               self.fields['name'].widget = forms.TextInput(attrs={'class': 'custom-class'})

   ```

    2. 通过在meta类中编辑fields字段可以限制模板显示哪些字段。对应的还有参数exclude，用于排除哪些字段。

6. fields是一个字典，其中包含表单中的所有字段及其对应的FormField对象。这个字典的键是字段的名称（例如username，email和age），值是FormField对象。

   FormField对象是表单字段的实现。它表示表单中的一个字段，您可以使用它来创建表单实例并处理输入。FormField对象的主要属性有：

    1. name：字段的名称，用于在表单数据中引用它。
    2. label：字段的标签，用于在UI中显示给用户。
    3. required：一个布尔值，表示字段是否必填。
    4. widget：一个表示字段渲染方式的类，例如TextInput、Select等。
    5. help_text：一个用于显示在表单字段下方帮助文本。
    6. initial：字段的初始值。
    7. error_messages：一个字典，包含字段验证失败时显示的错误消息。
7. 可以向modelform中传入已提交的数据，字段会自动匹配。再通过is_valid方法进行校验，要是验证失败错误信息也会被添加进入form。通过字段.errors可以查看错误信息。

   ```python
   form = UserModelForm(request.POST)
   form.is_valid():
   ```

8. 通过在modelForm中重写字段可以自定义表单的校验规则
9. 针对数据库的表单操作用modelform，其余的用form
10. form.save()保存的是用户输入的所有信息，要想保存其他信息用form.instance.字段名=值
11. 钩子方法（Hook
    method）是在Django的ModelForm中用于在验证数据之前或之后执行自定义处理的函数。它允许你在校验数据之前或之后执行一些操作，例如添加自定义错误消息、修改数据值等。钩子方法的命名通常以`clean_`
    开头，例如`clean_mobile`。

在这个例子中，`clean_mobile`
方法通过对用户输入的手机号进行长度和格式验证，以及检查数据库中是否已经存在相同的手机号。如果验证通过，那么手机号将被返回，否则将抛出一个`ValidationError`
异常。

12. pk primaryKey 主键
13. 把一个操作抽象为工具类的流程
    1. 有需求，先在原位置把流程实现
    2. 写一个类，把流程封装起来
    3. 抽象流程，将流程逐渐转移到工具类中
    4. 逐步提升抽象等级，考虑更一般的情况，加强健壮性
    5. 调用类
14. request.GET.urlencode()方法可以将request对象中的GET参数转换为urlencoded格式的字符串。
15. model.ForeignKey() 设置外键 参数：to 对应的表 to_filed对应的字段
16. 通过AJAX的方式传递数据对比直接用ModelForm形式传递
    1.ajax是部分刷新。就实现来说，主要工程量在编写js代码，是通过js来控制提交表单的一种形式
    2.对于后端来说，所有的流程基本不变，只是多了一个前端js的代码
17. html中id选择器和类选择器的区别
    1. 类选择器是.class id选择器是#id
    2. 一个标签可以有多个类
    3. 类选择器优先级大于id选择器
    4. 与类不同，在一个 HTML 文档中，ID 选择器会且仅会使用一次。
18. json序列化只支持基本数据类型
19. 通过 ' pip freeze >xx.txt '来保存项目的包
20. 创建虚拟环境 python -m venv ENV_DIR
21. 激活环境 .\ENV_DIR\Scripts\activate
22. 退出环境 deactivate
23. Django中的静态文件只能放在static目录下，用户上传的文件应该放在media目录
24. 在Django中配置media目录
    1. 配置urls.py

        ```python
        re_path(r"media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),#配置用户上传文件目录
        ```

    2. 修改settings.py文件

        ```python
        MEDIA_ROOT = os.path.join(BASE_DIR, "media")#根目录下的media文件夹
        MEDIA_URL = "/media/"
        ```

    2.  

## 易错点

1. 模板语法中实例化对象不允许加括号，需要括号时会自动添加
2. 模板语法中格式化条件
   `{{obj.creat_time|date:"Y-m-d"}}`
3. 自定义中间件需要在settings.middleware中注册
    1. process_request
        1. process_request返回HttpResponse、render、redirect对象时，请求会停止传递,返回None时，请求会继续向下传递
4. .gitignore自定义要忽略文件的路径的规则
    - prj

    所有名字是prj的文件和文件夹都会被忽略，不管其目录的相对位置在哪。
    - /prj

    开头的/指定根目录。
    所以整体代表根目录下的prj（不管prj是文件夹还是文件）都会被忽略。
    - prj/

    所有名字是prj的文件夹里的所有内容都会被忽略。
    - /prj/*

    根目录下的prj文件夹里的所有都忽略掉。
    - *prj/*

    根目录下以prj结尾的文件夹里的所有内容都会被忽略。
    - *是通配符，替代一个或多个任意字符

        **表示任意层级目录
