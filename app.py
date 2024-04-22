import logging
import os
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from werkzeug.utils import secure_filename
import subprocess
import threading
import logging
from flask_cors import CORS

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="http://localhost:5173")
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

# 配置日志记录器
logging.basicConfig(level=logging.INFO)

# WebSocket 服务器端处理函数
@socketio.on('connect')
def handle_connect():
    # 向客户端发送日志消息
    pass

# 后台执行脚本的函数
def run_script():
    try:
        # 执行脚本并获取输出
        process = subprocess.Popen(['python', 'excel_reader.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        # 逐行读取输出并发送到前端
        for line in process.stdout:
            socketio.emit('log_message', line.strip())
    except Exception as e:
        # 发生异常时发送错误消息到前端
        socketio.emit('log_message', f'Error: {e}')

# 执行脚本的路由
@app.route('/run_script')
def run_script_route():
    # 在新线程中执行脚本
    threading.Thread(target=run_script).start()
    return 'Script started'

@app.route('/')
def index():
    return render_template('index.html')

# 设置文件上传目录
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 文件上传接口
@app.route('/upload', methods=['POST'])
def upload_file():
    # 检查请求中是否包含文件
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    
    # 检查文件名是否为空
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    # 保存文件到指定目录
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'message': 'File uploaded successfully'})

if __name__ == '__main__':
    socketio.run(app)
