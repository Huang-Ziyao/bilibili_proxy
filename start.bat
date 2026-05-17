@echo off
chcp 65001 >nul
echo ========================================
echo   Bilibili 代理数据获取启动脚本
echo ========================================
echo.

:: 获取用户输入的 BV 号
echo 请输入 BV 号 (例如：BV1xx411c7mD): 
set /p BV_ID=

if "%BV_ID%"=="" (
    echo [错误] BV 号不能为空！
    pause
    exit /b 1
)

echo.
echo [步骤 1/3] 正在自动获取最新代理列表...
echo.

:: 运行获取代理脚本
python get_proxy.py
if errorlevel 1 (
    echo [错误] 获取代理失败，请检查网络连接或 get_proxy.py 脚本
    pause
    exit /b 1
)

:: 检查 proxy.txt 是否存在且有内容
if not exist "proxy.txt" (
    echo [错误] 未找到 proxy.txt 文件
    pause
    exit /b 1
)

for /f %%a in ('findstr /n "^" proxy.txt ^| find /c ":"') do set PROXY_COUNT=%%a
if "%PROXY_COUNT%"=="0" (
    echo [警告] proxy.txt 为空，可能没有获取到可用代理
    echo 是否继续尝试运行？(Y/N)
    set /p CONTINUE=
    if /i not "%CONTINUE%"=="Y" (
        pause
        exit /b 1
    )
)

echo.
echo [步骤 2/3] 已获取 %PROXY_COUNT% 个代理
echo [步骤 3/3] 开始获取 BV 号 %BV_ID% 的数据...
echo.

:: 直接调用 bilibili_proxy.py 并传入 BV 号参数
python bilibili_proxy.py %BV_ID%

echo.
echo ========================================
echo   任务完成！
echo ========================================
pause
