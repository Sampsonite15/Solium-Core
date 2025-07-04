@echo off

REM Use default dates if none are provided
set START=%1
set END=%2

if "%START%"=="" set START=2025-06-21
if "%END%"=="" set END=2025-07-03

echo Running backfill with start=%START% and end=%END%
python "C:\Users\andy\PycharmProjects\Solium\versions\v5.2.3\backfill_logger.py" --start %START% --end %END%
pause

@echo off
echo Running backfill with start=%1 and end=%2
python "C:\Users\andy\PycharmProjects\Solium\versions\v5.2.3\backfill_logger.py" --start %1 --end %2
pause

@echo off
python "C:\Users\andy\PycharmProjects\Solium\versions\v5.2.3\backfill_logger.py" --start %1 --end %2