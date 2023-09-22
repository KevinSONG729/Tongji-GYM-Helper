# 优雅的错误处理
def suppress_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"The error in {func.__name__}: {e}")
    return wrapper

# 计时
def timer(func):
  import time
  def wrapper(*args, **kwargs):
      start_time = time.time()
      result = func(*args, **kwargs)
      end_time = time.time()
      print(f"{func.__name__} took {end_time - start_time:.2f} seconds to execute.")
      return result
  return wrapper

# 缓存过去函数结果（高频调用且输入值经常重复）
def memoize(func):
    cache = {}
    def wrapper(*args):
        if args in cache:
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result
    return wrapper

# 验证输入类型正确性
def validate_input(func):
    def wrapper(*args, **kwargs):
        valid_data = True
        # here is the validate logic
        if valid_data:
            return func(*args, **kwargs)
        else:
            raise ValueError('Invalid data.Please check your inputs')
    return wrapper

# 记录函数结果
def log_results(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        with open("results.log", "a") as f:
            f.write(f"{func.__name__} - Result:{result}\n")
        return result
    return wrapper

# 函数报错自动重试
def retry(max_attempts, delay):
    import time
    def decorator(func):
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Attempts {attempts+1} failed. Retrying in {delay} seconds.")
                    attempts += 1
                    time.sleep(delay)
            raise Exception("Max retry attempts exceeded.")
        return wrapper
    return decorator

# 函数结果可视化
def visualize_results(func):
    import matplotlib.pyplot as plt
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        plt.figure()
        # visualization code here
        plt.show()
        return result
    return wrapper

# 输出函数参数信息
def debug(func):
    def wrapper(*args, **kwargs):
        print(f"Debugging {func.__name__} - args: {args}, kwargs: {kwargs}")
        return func(*args, **kwargs)
    return wrapper

# 函数废弃提醒
def deprecated(func):
    import warnings
    def wrapper(*args, **kwargs):
        warnings.warn(f"{func.__name__} is deprecated and will be removed in future versions.", DeprecationWarning)
        return func(*args, **kwargs)
    return wrapper