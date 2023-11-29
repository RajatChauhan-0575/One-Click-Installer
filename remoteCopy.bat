:: This file content is depricated
@echo off

set localParentPath=%1
set remotedirPath=%2
set ID=%3
set reponame=%4
set softwarename=%5

IF /i "%ID%"=="list_repos" goto list_repos
IF /i "%ID%"=="list_softwares" goto list_softwares
IF /i "%ID%"=="get_filesFromRemote" goto get_filesFromRemote

:list_repos 
dir %remotedirPath% /A:D /B
EXIT /B 0

:list_softwares:
set remoterepodirPath=%remotedirPath%\%reponame%
dir %remoterepodirPath% /A:D /B
EXIT /B 0

:get_filesFromRemote 
set remotePath=%remotedirPath%\%reponame%\%softwarename%
set localPath=%localParentPath%\%reponame%\%softwarename%
xcopy /S /I /E /Y /D %remotePath% %localPath%
EXIT /B 0
