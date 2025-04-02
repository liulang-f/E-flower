import atexit
import subprocess

# 启动 Redis
redis_process = None
def start_redis():
    # 检查 Redis 是否已经运行
    global redis_process
    try:
        subprocess.run(["redis-cli", "ping"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Redis 已经运行了！")
    except subprocess.CalledProcessError:
        # 如果 Redis 未运行，启动它
        print("启动 Redis 中")
        redis_process = subprocess.Popen(["redis-server"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        atexit.register(stop_redis)
        print("Redis 启动！")
# 关闭 Redis
def stop_redis():
    print("关闭 Redis...")
    redis_process.kill()  # 使用 SIGKILL 强制终止进程
    redis_process.wait()