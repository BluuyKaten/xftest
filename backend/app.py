from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from speech_recognition import SpeechRecognition
from werkzeug.utils import secure_filename
import subprocess

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 文件上传配置
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'm4a', 'aac', 'flac', 'webm'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 创建上传目录
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 启用CORS以允许前端访问
CORS(app)

# 初始化数据库
db = SQLAlchemy(app)

# 科大讯飞语音识别配置
SPEECH_CONFIG = {
    'APPID': 'fd2e4312',
    'APIKey': '0c704fe4c2b9696f3194ffff37152b56',
    'APISecret': 'MzY1ZmQ2OTY2NGVhMzhjM2NmZjAzNDli'
}

# 初始化语音识别
speech_recognizer = SpeechRecognition(
    app_id=SPEECH_CONFIG['APPID'],
    api_key=SPEECH_CONFIG['APIKey'],
    api_secret=SPEECH_CONFIG['APISecret']
)

# 数据模型
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SpeechRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    audio_file = db.Column(db.String(500), nullable=False)
    recognized_text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# 创建数据库表
with app.app_context():
    db.create_all()

def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# API路由
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Flask API is running!'})

@app.route('/api/test', methods=['POST'])
def test_api():
    """测试API"""
    try:
        data = request.get_json()
        print(f"测试API接收到的数据: {data}")
        return jsonify({
            'success': True,
            'message': '测试API正常工作',
            'received_data': data
        })
    except Exception as e:
        print(f"测试API异常: {str(e)}")
        return jsonify({'error': f'测试API异常: {str(e)}'}), 500

@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'created_at': user.created_at.isoformat()
    } for user in users])

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('email'):
        return jsonify({'error': '用户名和邮箱是必需的'}), 400
    
    # 检查用户是否已存在
    existing_user = User.query.filter_by(username=data['username']).first()
    if existing_user:
        return jsonify({'error': '用户名已存在'}), 400
    
    new_user = User(username=data['username'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({
        'id': new_user.id,
        'username': new_user.username,
        'email': new_user.email,
        'created_at': new_user.created_at.isoformat()
    }), 201

@app.route('/api/posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    return jsonify([{
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'author_id': post.author_id,
        'created_at': post.created_at.isoformat()
    } for post in posts])

@app.route('/api/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    
    if not data or not data.get('title') or not data.get('content') or not data.get('author_id'):
        return jsonify({'error': '标题、内容和作者ID是必需的'}), 400
    
    new_post = Post(
        title=data['title'],
        content=data['content'],
        author_id=data['author_id']
    )
    db.session.add(new_post)
    db.session.commit()
    
    return jsonify({
        'id': new_post.id,
        'title': new_post.title,
        'content': new_post.content,
        'author_id': new_post.author_id,
        'created_at': new_post.created_at.isoformat()
    }), 201

# 文件上传API
@app.route('/api/upload/audio', methods=['POST'])
def upload_audio():
    """上传音频文件"""
    try:
        if 'audio_file' not in request.files:
            return jsonify({'error': '没有选择文件'}), 400
        
        file = request.files['audio_file']
        if file.filename == '' or file.filename is None:
            return jsonify({'error': '没有选择文件'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename or '')
            # 添加时间戳避免文件名冲突
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{timestamp}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            return jsonify({
                'success': True,
                'filename': filename,
                'filepath': filepath
            })
        else:
            return jsonify({'error': '不支持的文件格式'}), 400
            
    except Exception as e:
        return jsonify({'error': f'文件上传失败: {str(e)}'}), 500

# 语音识别相关API
@app.route('/api/speech/recognize', methods=['POST'])
def recognize_speech():
    """语音识别API"""
    try:
        print("=== 语音识别API被调用 ===")
        data = request.get_json()
        print(f"接收到的数据: {data}")
        
        audio_file_path = data.get('audio_file_path')
        user_id = data.get('user_id')
        is_realtime = data.get('is_realtime', False)
        
        print(f"音频文件路径: {audio_file_path}")
        print(f"用户ID: {user_id}")
        print(f"是否实时录音: {is_realtime}")
        
        if not audio_file_path:
            print("错误: 音频文件路径是必需的")
            return jsonify({'error': '音频文件路径是必需的'}), 400
        
        # 检查文件是否存在
        print(f"检查文件是否存在: {audio_file_path}")
        if not os.path.exists(audio_file_path):
            print(f"文件不存在，尝试在uploads目录中查找")
            # 尝试在uploads目录中查找
            uploads_path = os.path.join(app.config['UPLOAD_FOLDER'], os.path.basename(audio_file_path))
            print(f"uploads路径: {uploads_path}")
            if os.path.exists(uploads_path):
                audio_file_path = uploads_path
                print(f"在uploads目录中找到文件: {audio_file_path}")
            else:
                print(f"文件在uploads目录中也不存在")
                return jsonify({'error': f'音频文件不存在: {audio_file_path}'}), 404
        
        # 自动转码为16kHz/16bit/单声道wav
        ext = os.path.splitext(audio_file_path)[1].lower()
        if ext != '.wav':
            wav_path = audio_file_path + '.wav'
            print(f"自动转码: {audio_file_path} -> {wav_path}")
            try:
                convert_to_wav(audio_file_path, wav_path)
                audio_file_path = wav_path
            except Exception as e:
                print(f"音频转码失败: {str(e)}")
                return jsonify({'error': f'音频转码失败: {str(e)}'}), 500
        else:
            print("音频已为wav格式，无需转码")
        
        # 输出音频参数日志
        try:
            import wave
            with wave.open(audio_file_path, 'rb') as wf:
                print(f"音频参数: nchannels={wf.getnchannels()}, sampwidth={wf.getsampwidth()}, framerate={wf.getframerate()}, nframes={wf.getnframes()}, duration={wf.getnframes()/wf.getframerate():.2f}s")
        except Exception as e:
            print(f"无法读取音频参数: {str(e)}")
        
        print(f"开始语音识别: {audio_file_path}")
        
        # 执行语音识别
        result = speech_recognizer.recognize_audio_file(audio_file_path)
        
        print(f"识别结果: {result}")
        
        if result['success']:
            # 保存识别记录到数据库
            speech_record = SpeechRecord(
                audio_file=audio_file_path,
                recognized_text=result['text'],
                user_id=user_id
            )
            db.session.add(speech_record)
            db.session.commit()
            
            print("识别成功，记录已保存")
            return jsonify({
                'success': True,
                'text': result['text'],
                'record_id': speech_record.id,
                'is_realtime': is_realtime
            })
        else:
            # 增强错误提示
            error_msg = result['error'] or '识别结果为空，可能音频内容无效或格式不兼容。请上传16kHz/16bit/单声道wav音频。'
            print(f"识别失败: {error_msg}")
            return jsonify({
                'success': False,
                'error': error_msg,
                'is_realtime': is_realtime
            }), 400
            
    except Exception as e:
        print(f"语音识别异常: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'语音识别失败: {str(e)}'}), 500

@app.route('/api/speech/records', methods=['GET'])
def get_speech_records():
    """获取语音识别记录"""
    records = SpeechRecord.query.order_by(SpeechRecord.created_at.desc()).all()
    return jsonify([{
        'id': record.id,
        'audio_file': record.audio_file,
        'recognized_text': record.recognized_text,
        'user_id': record.user_id,
        'created_at': record.created_at.isoformat()
    } for record in records])

@app.route('/api/speech/records/<int:record_id>', methods=['GET'])
def get_speech_record(record_id):
    """获取单个语音识别记录"""
    record = SpeechRecord.query.get(record_id)
    if not record:
        return jsonify({'error': '记录不存在'}), 404
    
    return jsonify({
        'id': record.id,
        'audio_file': record.audio_file,
        'recognized_text': record.recognized_text,
        'user_id': record.user_id,
        'created_at': record.created_at.isoformat()
    })

def convert_to_wav(input_path, output_path):
    ffmpeg_path = r'F:\development\ffmpeg-7.0.2-essentials_build\bin\ffmpeg.exe'
    cmd = [
        ffmpeg_path, '-y', '-i', input_path,
        '-ar', '16000', '-ac', '1', '-sample_fmt', 's16',
        output_path
    ]
    subprocess.run(cmd, check=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 