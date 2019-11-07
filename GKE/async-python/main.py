import concurrent
import asyncio
import time


async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)
    return delay


async def main():
    
    print(f"started at {time.strftime('%X')}")
    '''
    task1 = asyncio.create_task(
        say_after(1, 'hello'))

    task2 = asyncio.create_task(
        say_after(2, 'world'))
    
    task3 = asyncio.create_task(
        say_after(2, 'world'))
    '''
    res1 = asyncio.create_task(asyncio.wait_for(say_after(2, 'world'), timeout=1.))
    res2 = asyncio.create_task(asyncio.wait_for(say_after(2, 'world'), timeout=5.))
    res3 = asyncio.create_task(asyncio.wait_for(say_after(2, 'world'), timeout=5.))

    res = [res1, res2, res3]
    
    tmps = []
    for i in res: 
        try: 
            tmp = await i 
            tmps.append(tmp)
        except asyncio.TimeoutError:
            print ('time out')

    print (tmps)
    print(f"finished at {time.strftime('%X')}")

asyncio.run(main())
