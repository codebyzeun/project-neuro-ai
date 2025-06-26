@echo off
echo Building Discord Bot Executable...
echo.

echo Installing requirements...
pip install -r requirements.txt

echo.
echo Building executable...
python setup.py build

echo.
echo Build complete! Check the 'build' folder for your executable.
pause

echo "Building YiXuan Discord Bot Executable..."
echo

echo "Installing requirements..."
pip install -r requirements.txt

echo
echo "Building executable..."
python setup.py build

echo
echo "Build complete! Check the 'build' folder for your executable."
read -p "Press Enter to continue..."
