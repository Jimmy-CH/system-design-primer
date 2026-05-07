import redis
import uuid
import time
import threading


class DistributedLock:
    def __init__(self, redis_client, key, timeout=10):
        """
        初始化分布式锁
        :param redis_client: Redis 客户端实例
        :param key: 锁的键（通常包含业务前缀和唯一ID，如 lock:pay:order_123）
        :param timeout: 锁的过期时间（秒），防止死锁
        """
        self.client = redis_client
        self.key = key
        self.timeout = timeout
        # 生成唯一的锁标识（UUID），用于区分不同的客户端/线程
        self.identifier = str(uuid.uuid4())

    def acquire(self):
        """
        尝试获取锁
        使用 SET NX PX 保证原子性
        """
        # set nx=True 表示只有键不存在时才设置
        # ex=self.timeout 设置过期时间
        return self.client.set(
            self.key,
            self.identifier,
            nx=True,
            ex=self.timeout
        )

    def release(self):
        """
        释放锁
        使用 Lua 脚本确保“检查标识”和“删除键”是原子操作
        防止误删其他线程刚获取到的锁
        """
        # Lua 脚本逻辑：
        # 如果当前锁的值等于我的 identifier，则删除它；否则什么都不做
        lua_script = """
        if redis.call("get", KEYS[1]) == ARGV[1] then
            return redis.call("del", KEYS[1])
        else
            return 0
        end
        """
        # 执行 Lua 脚本
        unlock_script = self.client.register_script(lua_script)
        try:
            unlock_script(keys=[self.key], args=[self.identifier])
        except redis.exceptions.RedisError as e:
            print(f"❌ 释放锁时发生错误: {e}")


def process_payment(order_id, amount):
    """模拟耗时的支付处理逻辑"""
    print(f"💰 正在连接银行网关处理订单 {order_id}，金额: {amount}...")
    time.sleep(2)  # 模拟网络耗时
    print(f"✅ 订单 {order_id} 支付成功！")


def pay_order(order_id, amount):
    """
    支付接口入口
    """
    # 1. 定义锁的 Key，建议格式：lock:业务类型:资源ID
    lock_key = f"lock:pay:{order_id}"

    # 2. 初始化锁
    # 假设 Redis 运行在本地，生产环境请配置 host/port/password
    redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
    lock = DistributedLock(redis_client, lock_key, timeout=10)

    # 3. 尝试获取锁
    if lock.acquire():
        try:
            # --- 临界区开始 ---
            # 拿到锁后，建议再次检查数据库状态（双重检查），防止锁过期期间已有数据变更
            print(f"🔒 [线程-{threading.current_thread().name}] 获取锁成功，开始处理支付")
            process_payment(order_id, amount)
            # --- 临界区结束 ---
        finally:
            # 4. 务必在 finally 块中释放锁，确保即使业务报错也能释放
            lock.release()
            print(f"🔓 [线程-{threading.current_thread().name}] 锁已释放")
    else:
        # 5. 获取锁失败，说明有重复请求正在处理
        print(f"⚠️ [线程-{threading.current_thread().name}] 系统繁忙，检测到重复支付请求，已拦截！")


# --- 模拟并发测试 ---
if __name__ == "__main__":
    order_id = "ORDER_20260506_001"
    threads = []

    # 模拟用户手抖，短时间内发起了 5 个相同的支付请求
    for i in range(5):
        t = threading.Thread(target=pay_order, args=(order_id, 100.00), name=f"{i + 1}")
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

