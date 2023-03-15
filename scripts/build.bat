pyinstaller main.spec
Xcopy "resources" "dist/main/resources" /E /H /C /I
Xcopy "config" "dist/main/config" /E /H /C /I
Xcopy "env" "dist/main/env"  /E /H /C /I
Xcopy "app" "dist/main/app"  /E /H /C /I