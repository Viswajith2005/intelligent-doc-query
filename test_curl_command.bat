@echo off
echo Testing Intelligent Document Query API...
echo.

curl -X POST "http://localhost:8000/api/v1/hackrx/run" ^
-H "Content-Type: application/json" ^
-H "Authorization: Bearer acee50b025067ece530801f7901433430fae46c00beae83921306b8503bfb39a" ^
-d @test_request.json

echo.
echo Test completed!
pause 