import itertools
import sys
import time



# Spinning Wheel:
# ======================================

def spinning_wheel(duration=5):
    spinner = itertools.cycle(['-', '/', '|', '\\'])
    end_time = time.time() + duration
    while time.time() < end_time:
        sys.stdout.write('\r' + next(spinner))
        sys.stdout.flush()
        time.sleep(0.1)

spinning_wheel(duration=5)


# Progress Bar:
# =================================

def progress_bar(duration=5, width=50):
    for i in range(width + 1):
        time.sleep(duration / width)
        percent = (i / width) * 100
        bar = '#' * i + '-' * (width - i)
        sys.stdout.write('\r[{0}] {1:.2f}%'.format(bar, percent))
        sys.stdout.flush()
    sys.stdout.write('\n')

progress_bar(duration=5)

#
# Dot Animation:
# ===============================================

def dot_animation(duration=5):
    end_time = time.time() + duration
    while time.time() < end_time:
        for i in range(4):
            sys.stdout.write('\r' + '.' * i + ' ' * (3 - i))
            sys.stdout.flush()
            time.sleep(0.5)

dot_animation(duration=5)



# Growing and Shrinking Line:
# ================================================

def line_animation(duration=5):
    max_length = 10
    direction = 1
    length = 0
    end_time = time.time() + duration
    while time.time() < end_time:
        length += direction
        if length == max_length or length == 0:
            direction *= -1
        sys.stdout.write('\r' + '=' * length)
        sys.stdout.flush()
        time.sleep(0.2)

line_animation(duration=5)
