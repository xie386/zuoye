import time
import asyncio
records=[]
lock=asyncio.Lock()
class AIModel():
    def __init__(self,name,model_type):
        self.name=name
        self.model_type=model_type
    async def predict(self,input_data):
        raise NotImplementedError("子类必须实现predict方法")
class TextModel(AIModel):
    async def predict(self,input_data):
        print(f"文本模型{self.name}正在生成")
        await asyncio.sleep(1)
        return f"生成文本结果{input_data}"
class ImageModel(AIModel):
     async def predict(self,input_data):
        print(f"图像模型{self.name}正在识别")
        await asyncio.sleep(2)
        return f"识别结果{input_data}"
async def user_request(user_name, model, input_data):
    start=time.time()
    await model.predict(input_data)
    end=time.time()
    cost=end-start
    records.append({"用户名":user_name,"调用模型":model.name,"耗时":cost,"输出结果":input_data})

async def main():
    start=time.time()
    async with lock:
        await asyncio.gather(
            user_request("Alice", TextModel("deepseek", "文本"), "你好"),
            user_request("Bob", ImageModel("deepseek-image", "图片"), "图片123"),
            user_request("Carol", TextModel("qwen", "文本"), "你好"),
            user_request("Diana",ImageModel("qwen-image", "图片"), "图片456")
        )
    print(records)
    end=time.time()
    print(f"耗时{end-start}秒")

asyncio.run(main())