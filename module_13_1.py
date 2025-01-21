import asyncio

async def start_strongman(name, power):
        max_ball = 5
        current_ball = 0
        print(f"Силач {name} начал соревнования.")
        while current_ball < max_ball:
            await asyncio.sleep(1/power)
            print(f"Силач {name} поднял {current_ball+1} шар.")
            current_ball = current_ball + 1
        print(f"Силач {name} закончил соревнования.")

async def start_tournament():
        task1 = asyncio.create_task(start_strongman('SpiderMan', 3))
        task2 = asyncio.create_task(start_strongman('SlipperMan', 5))
        task3 = asyncio.create_task(start_strongman('Добрыня Никитич', 10))
        await task1
        await task2
        await task3

asyncio.run(start_tournament())
