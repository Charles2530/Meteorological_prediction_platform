# 紫微气象（独角兽🦄）

大数据检测气象及地质数据

## 前端使用指南

前端使用 vite + vue3 + typescript 作为基本框架进行 web 开发，集成 ECharts 库，以便在应用程序中创建各种图表和数据可视化，使用 tailwind css 和 element plus 美化网页布局，实现网页布局和样式的一致性。

> 移动端启动方式相同，但是需要在移动端浏览器中打开网页F12调整为手机端设备预览。

- 启动命令:

```shell
cd front_end
# 安装相关依赖
npm install 
# 本地运行和云端运行二选一即可
    # 本地运行
    npm run dev
    # 云端运行
    npm run build
    npm run preview
```

## 后端使用指南

后端使用 Django5 作为基本框架，集成 rest_framework 和 rest_framework_simplejwt 的 Token 验证机制，使用 corsheaders 完成跨域。


- 启动命令：

```shell
cd back_end
pip install -r pip_env.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

