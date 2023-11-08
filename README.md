# douyin tool Bot



## 配置环境
### 安装依赖
> nonebot相关依赖请自行查阅nonebot文档

```shell
pip3 install aiohttp
nb adapter install telegram
nb driver install fastapi
nb driver install httpx
```
## 快速使用
```shell
git clone https://github.com/CherryTomatoMedia/toolBot.git
cd toolBot
echo "ENVIRONMENT=prod" > .env
nb run
```
如果想要持久化运行，可以使用宝塔面板中提供的Supervisor进程监控程序