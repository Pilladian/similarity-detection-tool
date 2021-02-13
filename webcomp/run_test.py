# Python3.8

import os


def run(file_pairs):

    for desc, file1, file2 in file_pairs:
        print(f'Test running: {desc}')
        os.system(f'python3 image.py {file1} {file2}')
        print('\n')


if __name__ == '__main__':
    root_path = 'testbench/'

    files = [
        ('Logo Color', 'facebook_logo_different_color.png', 'facebook_logo_original.png'),
        ('Zoomed', 'facebook_screenshot.png', 'facebook_screenshot_zoomed_out.png'),
        ('Regular Website 1', 'facebook_screenshot.png', 'ragular_screenshot_1.png'),
        ('Regular Website 2', 'facebook_screenshot.png', 'regular_screenshot_2.png'),
        ('Regular Website 3', 'facebook_screenshot.png', 'regular_screenshot_3.png')
    ]

    files = [(d, root_path + f1, root_path + f2) for d, f1, f2 in files]

    os.system('clear')
    run(files)
