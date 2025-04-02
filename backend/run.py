from flask import send_from_directory
from app import create_app

# 创建 Flask 应用实例
app = create_app()

@app.route('/img/<path:filename>')
def serve_image(filename):
    return send_from_directory("static/img/", filename + ".png")

@app.route('/img/avator/<path:filename>')
def avator_image(filename):
    return send_from_directory("static/img/avatar/", filename + ".png")

if __name__ == '__main__':
    # 启动开发服务器
    app.run(debug=True, host='0.0.0.0', port=5000)