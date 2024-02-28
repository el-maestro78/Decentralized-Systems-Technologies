import subprocess
import sys


def user_input():
    print('Type 0 for Pastry or 1 for Chord')
    sys.stdout.flush()
    while True:
        demo = input()
        try:
            demo = int(demo)
            if demo == 1:
                script_path = './chord/demo.py'
                break
            elif demo == 0:
                script_path = './pastry/demo.py'
                break
            else:
                print('Invalid choice. Please try again.')
        except ValueError:
            print('Invalid choice. Please enter a number.')
    return script_path


def main():
    script_path = user_input()
    subprocess.run(['python', script_path], stdin=sys.stdin, stdout=sys.stdout)


if __name__ == '__main__':
    main()
