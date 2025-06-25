from cx_Freeze import setup, Executable
import sys

build_options = {
    'packages': ['discord', 'ctransformers', 'customtkinter', 'tkinter', 'asyncio', 'threading'],
    'excludes': ['test', 'unittest'],
    'include_files': [
        ('cogs/', 'cogs/'),
        ('utils/', 'utils/'),
        ('models/', 'models/'),
        ('config.py', 'config.py'),
        ('bot.py', 'bot.py'),
        ('.env', '.env')
    ]
}

base = 'Win32GUI' if sys.platform == 'win32' else None

executables = [
    Executable(
        'gui_launcher.py',
        base=base,
        target_name='YiXuan_Bot_Launcher',
        icon='icon.ico'
    )
]

setup(
    name='YiXuan Discord Bot',
    version='1.0',
    description='Sassy AI Discord Bot with GUI Launcher',
    options={'build_exe': build_options},
    executables=executables
)