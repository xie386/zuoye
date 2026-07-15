import time
from datetime import datetime
import threading

# ==================== 模型层 ====================

class AIModel():
    """AI模型基类，定义所有AI模型的统一接口。

    Attributes:
        name: 模型名称，如 "deepseek"
        model_type: 模型类型，如 "文本模型"
    """
    def __init__(self, name, model_type):
        """初始化模型实例。

        Args:
            name: 模型名称
            model_type: 模型类型描述
        """
        self.name = name
        self.model_type = model_type

    def predict(self, input_data):
        """抽象方法：执行推理预测，子类必须重写。

        若子类未重写此方法，调用时将抛出 NotImplementedError，
        强制子类实现预测逻辑，保证多态性。

        Args:
            input_data: 输入数据

        Raises:
            NotImplementedError: 子类未实现此方法时抛出
        """
        raise NotImplementedError("子类必须实现predict方法")


class TextModel(AIModel):
    """文本模型子类，模拟文本生成任务，推理休眠 1 秒。"""
    def predict(self, input_data):
        """执行文本推理，休眠 1 秒模拟 I/O 阻塞（如 API 调用）。

        Args:
            input_data: 输入文本数据

        Returns:
            tuple: (开始时间, 结束时间, 输入数据, 推理耗时)
        """
        start = datetime.now()
        print(f"文本模型{self.name}正在生成")
        time.sleep(1)
        end = datetime.now()
        return start, end, input_data, end - start


class ImageModel(AIModel):
    """图像模型子类，模拟图像识别任务，推理休眠 2 秒。"""
    def predict(self, input_data):
        """执行图像识别，休眠 2 秒模拟较长的 I/O 等待。

        Args:
            input_data: 输入图像数据

        Returns:
            tuple: (开始时间, 结束时间, 输入数据, 识别耗时)
        """
        start = datetime.now()
        print(f"图像模型{self.name}正在识别")
        time.sleep(2)
        end = datetime.now()
        return start, end, input_data, end - start


class AudioModel(AIModel):
    """语音模型子类，模拟语音识别任务，推理休眠 2 秒。"""
    def predict(self, input_data):
        """执行语音识别，休眠 2 秒模拟语音处理。

        Args:
            input_data: 输入语音数据

        Returns:
            tuple: (开始时间, 结束时间, 输入数据, 识别耗时)
        """
        start = datetime.now()
        print(f"语音模型{self.name}正在识别")
        time.sleep(2)
        end = datetime.now()
        return start, end, input_data, end - start

# ==================== 调度器 ====================

class Scheduler:
    """AI 推理任务调度器，支持串行和并发两种执行模式。

    Attributes:
        records: 任务记录表，存储每次调用的详细信息
        lock: 线程锁，保护 records 并发写入安全
    """
    records = []
    lock = threading.Lock()

    def __init__(self):
        """初始化调度器实例。"""
        pass

    def _run_one(self, user_name, model, input_data):
        """执行单次推理任务（线程安全），加锁写入记录。

        Args:
            user_name: 用户名
            model: AI 模型实例（AIModel 子类）
            input_data: 输入数据
        """
        _start = time.time()
        start, end, input_data, use_time = model.predict(input_data)

        self.lock.acquire()
        self.records.append({
            "用户名": user_name,
            "调用模型": model.name,
            "开始时间": start.strftime("%Y-%m-%d %H:%M:%S"),
            "结束时间": end.strftime("%Y-%m-%d %H:%M:%S"),
            "输出结果": input_data,
            "耗时": use_time.total_seconds()
        })
        self.lock.release()

        _use = time.time() - _start
        print("本次任务耗时:", _use)

    def run_serial(self, user_name, model_list, input_data_list):
        """串行依次执行所有推理任务。

        Args:
            user_name: 用户名
            model_list: 模型实例列表
            input_data_list: 输入数据列表（与 model_list 一一对应）

        Returns:
            float: 串行总耗时（秒），列表长度不匹配时返回 0
        """
        serial_start = time.time()
        if len(model_list) != len(input_data_list):
            print("模型列表与输入列表不匹配")
            return 0

        for i in range(len(model_list)):
            start, end, input_data, use_time = model_list[i].predict(input_data_list[i])
            self.lock.acquire()
            self.records.append({
                "用户名": user_name,
                "调用模型": model_list[i].name,
                "开始时间": start.strftime("%Y-%m-%d %H:%M:%S"),
                "结束时间": end.strftime("%Y-%m-%d %H:%M:%S"),
                "输出结果": input_data_list[i],
                "耗时": use_time.total_seconds()
            })
            self.lock.release()

        serial_use = time.time() - serial_start
        print("本次串行任务耗时:", serial_use)
        return serial_use

    def run_concurrent(self, user_name, model_list, input_data_list):
        """多线程并发执行所有推理任务（start + join 模式）。

        Args:
            user_name: 用户名
            model_list: 模型实例列表
            input_data_list: 输入数据列表（与 model_list 一一对应）

        Returns:
            float: 并发总耗时（秒），列表长度不匹配时返回 0
        """
        concurrent_start = time.time()
        if len(model_list) != len(input_data_list):
            print("模型列表与输入列表不匹配")
            return 0

        threads = []
        for model, data in zip(model_list, input_data_list):
            def task_warpper(m, d, uname):
                start, end, out_data, use_time = m.predict(d)
                with self.lock:
                    self.records.append({
                        "用户名": uname,
                        "调用模型": m.name,
                        "开始时间": start.strftime("%Y-%m-%d %H:%M:%S"),
                        "结束时间": end.strftime("%Y-%m-%d %H:%M:%S"),
                        "输出结果": out_data,
                        "耗时": use_time.total_seconds()
                    })
            t = threading.Thread(target=task_warpper, args=(model, data, user_name))
            threads.append(t)

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        concurrent_use = time.time() - concurrent_start
        print("本次并行任务耗时:", concurrent_use)
        return concurrent_use

    def report(self):
        """格式化打印所有任务记录的详细信息。"""
        for record in self.records:
            print(record)

    def compare(self, user_name, model_list, input_data_list):
        """串行与并发性能对比，生成报表写入 report.txt。

        Args:
            user_name: 用户名
            model_list: 模型实例列表
            input_data_list: 输入数据列表

        Returns:
            tuple: (串行耗时, 并发耗时, 加速比)
        """
        Scheduler.records.clear()

        serial_cost = self.run_serial(user_name + "_串行", model_list, input_data_list)

        Scheduler.records.clear()

        concurrent_cost = self.run_concurrent(user_name + "_并行", model_list, input_data_list)

        speedup = serial_cost / concurrent_cost if concurrent_cost != 0 else 0

        report_content = []
        report_content.append("=" * 60)
        report_content.append(f"调度模式性能对比报告 - 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_content.append("=" * 60)
        report_content.append(f"测试用户：{user_name}")
        report_content.append(f"测试模型数量：{len(model_list)}")
        report_content.append(f"串行总耗时：{serial_cost:.4f} 秒")
        report_content.append(f"并发总耗时：{concurrent_cost:.4f} 秒")
        report_content.append(f"节省时长：{serial_cost - concurrent_cost:.4f} 秒")
        report_content.append(f"加速比：{speedup:.2f}x")
        report_content.append(f"当前系统时间：{datetime.now()}")
        report_content.append("-" * 60)
        report_content.append("说明：加速比越大，多线程并发提升越明显")
        report_content.append("=" * 60 + "\n")

        with open("report.txt", "a", encoding="utf-8") as f:
            f.write("\n".join(report_content))
            f.write("\n\n")
        print("对比报表已写入 report.txt")
        return serial_cost, concurrent_cost, speedup

# ==================== 主程序 ====================

def main():
    """主程序入口：创建模型与调度器，执行串行/并发对比测试并输出报表。"""
    start = datetime.now()

    deepseek = TextModel("deepseek", "文本模型")
    qwen = ImageModel("qwen", "图像模型")
    doubao = AudioModel("doubao", "语音模型")

    sc = Scheduler()

    sc.compare("A", [deepseek, qwen, doubao, deepseek, qwen, doubao],
               ["你好", "识别图片内容", "识别语音", "再见", "生成一张图片", "说一句话"])

    sc.report()

    end = datetime.now()
    total_use = end - start
    print(f"总耗时{total_use}")

if __name__ == "__main__":
    main()