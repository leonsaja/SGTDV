@echo off

start /D "%~dp0" /HIGH /WAIT pnputil -i -a  "%~dp0"MBI.inf
start /D "%~dp0" /HIGH /WAIT Setup.exe
