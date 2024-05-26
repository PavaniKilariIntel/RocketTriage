import time
import sys

def animate_rocket_loading():
    countdown = 10
    rocket = ['      ',
              '      ',
              '      ',
              '      ',
              '      ',
              '      ',
              '      ',
              '      ',
              '      ',
              '      ',
              '      ',
              '      ',
              '   |   ',
              '  /_\\  ',
              '  |_|  ',
              ' /___\\ ',
              ' |___| ',
              '  /_\\  ',
              '  |_|  ',
              ' /___\\ ',
              ' |___| ',
              '  /_\\  ',
              '  |_|  ',
              ' /___\\ ',
              ' |___| ',
              '  /_\\  ',
              '  |_|  ',
              ' /___\\ ',
              ' |___| ',
              '  /_\\  ',
              '  |_|  ',
              ' /___\\ ',
              ' |___| ',
              '-------']

    while countdown > 0:
        sys.stdout.write('\r')
        sys.stdout.write("\n".join(rocket))
        sys.stdout.write('\nT-minus {} seconds'.format(countdown))
        sys.stdout.flush()
        rocket.pop(0)
        rocket.insert(0, '      ')
        countdown -= 1
        time.sleep(1)

    sys.stdout.write('\r')
    sys.stdout.write("\n".join(rocket))
    sys.stdout.write('\nLift off!\n')
    sys.stdout.flush()

if __name__ == "__main__":
    animate_rocket_loading()
