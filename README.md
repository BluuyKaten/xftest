# Flask + Vue 全栈应用

这是一个使用 Flask 后端和 Vue.js 前端构建的现代化全栈应用。

## 项目结构

```
├── backend/                 # Flask 后端
│   ├── app.py              # 主应用文件
│   ├── requirements.txt    # Python 依赖
│   └── app.db             # SQLite 数据库（自动生成）
├── frontend/               # Vue.js 前端
│   ├── src/
│   │   ├── views/         # 页面组件
│   │   ├── api/           # API 服务
│   │   ├── router/        # 路由配置
│   │   ├── App.vue        # 主应用组件
│   │   └── main.js        # 应用入口
│   ├── package.json       # Node.js 依赖
│   ├── vite.config.js     # Vite 配置
│   └── index.html         # HTML 入口
└── README.md              # 项目说明
```

## 功能特性

- **用户管理**: 创建和管理用户账户
- **文章管理**: 发布和管理文章内容
- **RESTful API**: 提供完整的数据接口
- **响应式设计**: 适配各种设备屏幕
- **现代化UI**: 使用 Element Plus 组件库

## 技术栈

### 后端
- **Flask**: Python Web 框架
- **Flask-SQLAlchemy**: ORM 数据库操作
- **Flask-CORS**: 跨域资源共享
- **SQLite**: 轻量级数据库

### 前端
- **Vue 3**: 渐进式 JavaScript 框架
- **Vue Router**: 官方路由管理器
- **Element Plus**: Vue 3 组件库
- **Axios**: HTTP 客户端
- **Vite**: 现代化构建工具

## 安装和运行

### 1. 克隆项目

```bash
git clone <repository-url>
cd flask-vue-demo
```

### 2. 后端设置

```bash
# 进入后端目录
cd backend

# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt

# 运行后端服务
python app.py
```

后端服务将在 `http://localhost:5000` 启动。

### 3. 前端设置

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端应用将在 `http://localhost:3000` 启动。

### 4. 访问应用

打开浏览器访问 `http://localhost:3000` 即可使用应用。

## API 接口

### 用户管理
- `GET /api/users` - 获取用户列表
- `POST /api/users` - 创建新用户

### 文章管理
- `GET /api/posts` - 获取文章列表
- `POST /api/posts` - 创建新文章

### 健康检查
- `GET /api/health` - 检查API状态

## 开发说明

### 后端开发
- 修改 `backend/app.py` 添加新的API路由
- 在 `backend/requirements.txt` 中添加新的依赖
- 数据库模型在 `app.py` 中定义

### 前端开发
- 页面组件在 `frontend/src/views/` 目录
- API 服务在 `frontend/src/api/` 目录
- 路由配置在 `frontend/src/router/` 目录

### 数据库
- 使用 SQLite 数据库，文件为 `backend/app.db`
- 首次运行时会自动创建数据库表
- 可以通过修改模型来更新数据库结构

## 部署

### 后端部署
```bash
cd backend
pip install -r requirements.txt
python app.py
```

### 前端部署
```bash
cd frontend
npm install
npm run build
```

构建后的文件在 `frontend/dist/` 目录中。

## 注意事项

1. 确保后端服务在端口 5000 运行
2. 前端开发服务器配置了代理，会自动转发 API 请求到后端
3. 首次运行时会自动创建数据库和表结构
4. 这是一个演示项目，生产环境需要添加更多的安全措施

## 许可证

MIT License 