# TransitHub 交通出行管理平台

TransitHub 面向交通运营企业管理者、司机和运维人员，覆盖车辆管理、充电桩管理、出行订单、维修记录、地图总览、运营大屏、RBAC 权限和操作审计日志。

## 功能概览

- 地图总览：高德地图封装组件，展示运营车辆和充电桩位置，支持无 Key 降级坐标清单。
- 车辆管理：车辆注册、审核、调度、维修、报废，车辆详情关联维修记录。
- 充电桩管理：桩位地图、状态筛选、故障报修、维护恢复、计费管理。
- 出行订单：订单列表、状态流转、支付、订单详情轨迹回放。
- 运营大屏：车辆在线数、今日订单、今日收入、充电桩利用率、趋势与分布统计。
- 安全与审计：JWT 登录、Driver/Operator/Admin 三角色 RBAC、司机数据范围过滤、写操作审计日志。

## 技术栈

| 层级 | 技术 |
|---|---|
| 前端 | Angular 17, TypeScript, Angular Material, SCSS |
| 后端 | Django 5, Django REST Framework, PyJWT |
| 数据库 | PostgreSQL 16 |
| 缓存/会话 | Redis 7, django-redis |
| 部署 | Docker Compose, Nginx, Gunicorn |
| 地图 | 高德地图 Web API，`AMAP_API_KEY` 环境变量注入 |

## 快速启动 Docker Compose

```bash
cp .env.example .env
# 编辑 .env，填入 AMAP_API_KEY 和生产密钥
docker compose up --build
```

访问地址：

- 前端：http://localhost:38403
- 后端：http://localhost:38503
- 健康检查：http://localhost:38503/health/

默认演示账号由 `python manage.py seed_demo` 创建：

- 管理员：`admin` / `admin123456`
- 司机：`driver01` / `driver123456`

## 本地开发

后端：

```bash
cd backend
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
USE_SQLITE=1 python manage.py migrate
USE_SQLITE=1 python manage.py seed_demo
USE_SQLITE=1 python manage.py runserver 127.0.0.1:38503
```

前端：

```bash
cd frontend
npm ci
npm run typecheck
npm run build
npm start
```

## 目录结构

```text
backend/
  apps/common/        枚举、权限、异常、审计日志、中间件
  apps/users/         自定义用户、JWT 登录
  apps/vehicles/      车辆模型、序列化器、服务、视图
  apps/charging/      充电桩模型、序列化器、服务、视图
  apps/orders/        出行订单模型、序列化器、服务、视图
  apps/maintenance/   维修记录模型、服务、状态联动
  apps/dashboard/     运营统计 API
frontend/
  src/app/shared/     枚举、模型、服务、组件、守卫、拦截器、指令
  src/app/map/        地图总览
  src/app/vehicles/   车辆管理
  src/app/charging/   充电桩管理
  src/app/orders/     出行订单
  src/app/dashboard/  运营大屏
database/
  init.sql
  seed.sql
```

## 环境变量

| 变量 | 说明 | 默认值 |
|---|---|---|
| `COMPOSE_PROJECT_NAME` | Compose 项目前缀 | `ldtransit` |
| `DJANGO_SECRET_KEY` | Django 密钥 | 需生产替换 |
| `DEBUG` | 调试模式 | `0` |
| `POSTGRES_DB` | 数据库名 | `transithub` |
| `POSTGRES_USER` | 数据库用户 | `transithub` |
| `POSTGRES_PASSWORD` | 数据库密码 | `transithub` |
| `REDIS_URL` | Redis 地址 | `redis://redis:6379/0` |
| `AMAP_API_KEY` | 高德地图 Web API Key | 空 |

## 共享枚举使用位置

1. `backend/apps/common/constants/enums.py` — 后端枚举定义
2. `frontend/src/app/shared/constants/enums.ts` — 前端枚举定义
3. `backend/apps/vehicles/models.py` — Vehicle 模型引用 VehicleStatus、VehicleType
4. `backend/apps/charging/models.py` — ChargingPile 模型引用 PileType、PileStatus
5. `backend/apps/orders/models.py` — TripOrder 模型引用 OrderStatus、PaymentStatus
6. `backend/apps/vehicles/serializers.py` — 车辆序列化器引用枚举字段
7. `backend/apps/charging/serializers.py` — 充电桩序列化器引用枚举字段
8. `backend/apps/orders/serializers.py` — 订单序列化器引用枚举字段
9. `backend/apps/vehicles/views.py` — 车辆状态校验和位置接口
10. `backend/apps/charging/views.py` — 充电桩状态接口
11. `backend/apps/orders/views.py` — 订单状态流转接口
12. `backend/apps/common/middleware/audit_middleware.py` — 写操作审计日志
13. `frontend/src/app/shared/models/vehicle.model.ts` — 车辆模型引用枚举
14. `frontend/src/app/shared/models/charging-pile.model.ts` — 充电桩模型引用枚举
15. `frontend/src/app/shared/models/trip-order.model.ts` — 订单模型引用枚举
16. `frontend/src/app/vehicles/vehicle-list/vehicle-list.component.ts` — 车辆筛选
17. `frontend/src/app/charging/charging-list/charging-list.component.ts` — 充电桩筛选
18. `frontend/src/app/orders/order-list/order-list.component.ts` — 订单筛选
19. `frontend/src/app/shared/components/status-tag/status-tag.component.ts` — 状态标签
20. `frontend/src/app/shared/guards/role.guard.ts` — 路由角色判断

## Docker 说明

`docker-compose.yml` 顶层声明 `name: ldtransit`，所有容器名使用 `${COMPOSE_PROJECT_NAME:-ldtransit}` 前缀。PostgreSQL 使用命名卷持久化，后端依赖数据库和 Redis 健康检查，前端 Nginx 将 `/api/` 反向代理到 `backend:38503`。

## License

MIT
