@echo off

set path1=/touch_thing_externalApp/touch_thing_browserApp.html
set path2=/external_mock/jigglerMock.html

start "" %cd%%path1% >nul 2>nul
start "" %cd%%path2% >nul 2>nul


