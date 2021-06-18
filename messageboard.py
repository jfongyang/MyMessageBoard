# coding: utf-8

import shelve
from datetime import datetime

from flask import Flask, render_template, request, redirect,escape,Markup

# 创建实例
app = Flask(__name__)

# 数据文件
DATA_FILE = 'messengers'


# 数据保存
def save_data(name, comment, create_at):
    # 打开数据文件
    database = shelve.open(DATA_FILE)
    # 如果数据库中没有 greeting_list，就新建一个表
    if 'greeting_list' not in database:
        greeting_list = []
    else:
        # 从数据库获取数据
        greeting_list = database['greeting_list']
    # 将提交的数据添加到表头
    greeting_list.insert(0, {
        'name': name,
        'comment': comment,
        'create_at': create_at,
    })

    # 更新数据库
    database['greeting_list'] = greeting_list
    # 关闭数据库文件
    database.close()

# 数据获取
def load_data():
    # 打开数据文件
    database = shelve.open(DATA_FILE)
    # 返回greeting_list，没有则返回空
    greeting_list = database.get('greeting_list', [])
    database.close()
    return greeting_list

# 定义首页路由
@app.route('/')
def index():
    # 读取数据
    greeting_list = load_data()
    return render_template('index.html', greeting_list=greeting_list)

# 定义数据提交路由
@app.route('/post',methods=['POST'])
def post():
    name = request.form.get('name')
    comment = request.form.get('comment')
    create_at =  datetime.now()
    # 保存数据
    save_data(name,comment,create_at)
    return redirect('/')


# 定义模板过滤器
# 换行符转成br标签
@app.template_filter('nl2br')
def nl2br_filter(s):
    return escape(s).replace('\n',Markup('<br />'))
# 时间格式化输入
@app.template_filter('format_time')
def format_time_filter(dt):
    return dt.strftime('%Y/%m/%d %H:%M:%S')




if __name__ == '__main__':
    app.run()
