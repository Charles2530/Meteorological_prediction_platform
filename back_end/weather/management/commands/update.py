# import requests
# from myapp.models import MyModel

# # 发送HTTP请求
# response = requests.get('http://example.com/api/data')

# # 确保请求成功
# if response.status_code == 200:
#     # 接收响应数据
#     data = response.json()

#     # 序列化数据
#     for item in data:
#         # 假设我们有一个字段叫'name'和'value'
#         name = item.get('name')
#         value = item.get('value')

#         # 创建模型实例并存储数据
#         MyModel.objects.create(name=name, value=value)
# else:
#     print('Failed to fetch data:', response.status_code)
