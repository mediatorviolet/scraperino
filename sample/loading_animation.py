import sys
import time


def load_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='■'):
    percent = ('{0:.' + str(decimals) + 'f}').format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '□' * (length - filled_length)
    sys.stdout.write(f'\r{prefix} |{bar}| {percent}% {suffix}')
    sys.stdout.flush()
    if iteration == total:
        print('\n')


if __name__ == '__main__':
    items = list(range(0, 30))
    length = len(items)

    load_bar(0, length, prefix='Progress:', suffix='Done', length=length)
    for i, items in enumerate(items):
        time.sleep(0.5)
        load_bar(i + 1, length, prefix='Progress:', suffix='Done', length=length)
