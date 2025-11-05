import multiprocessing
import queue
import argparse

resolution = 0.1


def check_memory(q):
    import psutil
    import time

    results = []

    pself = psutil.Process()
    pparent = pself.parent()
    t0 = time.time()
    try:
        while True:
            mem = pparent.memory_full_info().rss
            for child in pparent.children():
                if child.pid != pself.pid:
                    try:
                        mem += child.memory_full_info().rss
                    except psutil.NoSuchProcess:
                        pass

            t = time.time() - t0
            print(' '*90 + f'Memory: {mem/1e6} MB\r', end='', flush=True)
            results.append((t, mem))

            time.sleep(resolution)

            # Check for poison pill
            try:
                if q.get_nowait() is None:
                    break
            except queue.Empty:
                pass

        # Place results on queue
        q.put(results)

    except KeyboardInterrupt:
        pparent.kill()


def measure(func, *args, **kwargs):
    print('Setting up queue')
    # Set up queue and worker to keep track of memory
    q = multiprocessing.Queue()
    worker = multiprocessing.Process(
        target=check_memory,
        args=(q,),
        daemon=True
    )

    # Run specified function while measuring memory
    print('Starting')
    worker.start()
    func(*args, **kwargs)

    # Send poison pill to worker
    print('Done, send poison pill')
    q.put(None)
    worker.join()

    # Get results from queue
    return q.get()


if __name__ == '__main__':
    import openmc

    parser = argparse.ArgumentParser()
    parser.add_argument('input_file')
    args = parser.parse_args()

    results = measure(openmc.run, path_input=args.input_file)
