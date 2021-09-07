1. Sync and Async interfaces for callbacks' storage and emitting
2. Example of usage:

```python
import asyncio
import time
from python_bz_ballbacks import SyncCallbacks, AsyncCallbacks


def sync_test():
    cbs = SyncCallbacks()
    cbs.add(lambda: print('Second'), '2')
    cbs.add(lambda: print('First'), '1')
    cbs.add(lambda: print('Third'), '3')    
    cbs.fire()
    print(f'SYNC FIRE DONE')

    
async def async_test():
    cbs = AsyncCallbacks()

    async def first():
        await asyncio.sleep(1)
        print('First')

    async def second():
        await asyncio.sleep(2)
        print('Second')

    async def third():
        await asyncio.sleep(3)
        print('Third')

    await cbs.add(third)
    await cbs.add(first)
    await cbs.add(second)
    start = time.time()
    await cbs.fire()
    print(f'ASYNC FIRE DONE IN {time.time()-start} seconds')

    
def test():
    sync_test()
    asyncio.run(async_test())

    
test()
```