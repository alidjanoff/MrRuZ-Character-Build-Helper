import os
import shutil

dirs = ['ui', 'logic', 'core', 'assets', 'tests']
for d in dirs:
    os.makedirs(d, exist_ok=True)

if os.path.exists('images'):
    for item in os.listdir('images'):
        shutil.move(os.path.join('images', item), os.path.join('assets', item))
    os.rmdir('images')

moves = [
    ('locales.py', 'core/locales.py'),
    ('game_data.py', 'logic/game_data.py'),
    ('calc_engine.py', 'logic/build_engine.py'),
    ('ui.py', 'ui/app_ui.py'),
    ('test_verify.py', 'tests/test_verify.py')
]

for src, dst in moves:
    if os.path.exists(src):
        shutil.move(src, dst)

print("Refactor complete")
