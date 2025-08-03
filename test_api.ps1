# Test Intelligent Document Query API
Write-Host "Testing Intelligent Document Query API..." -ForegroundColor Green
Write-Host ""

# Test Health Check
Write-Host "1. Testing Health Check..." -ForegroundColor Yellow
try {
    $healthResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/health" -Method GET
    Write-Host "Health Check Response:" -ForegroundColor Green
    $healthResponse | ConvertTo-Json -Depth 10
} catch {
    Write-Host "Health Check Failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "2. Testing Main API Endpoint..." -ForegroundColor Yellow

# Headers
$headers = @{
    "Content-Type" = "application/json"
    "Authorization" = "Bearer acee50b025067ece530801f7901433430fae46c00beae83921306b8503bfb39a"
}

# Request Body
$body = @{
    documents = "https://hackrx.blob.core.windows.net/assets/Arogya%20Sanjeevani%20Policy%20-%20CIN%20-%20U10200WB1906GOI001713%201.pdf?sv=2023-01-03&st=2025-07-21T08%3A29%3A02Z&se=2025-09-22T08%3A29%3A00Z&sr=b&sp=r&sig=nzrz1K9Iurt%2BBXom%2FB%2BMPTFMFP3PRnIvEsipAX10Ig4%3D"
    questions = @(
        "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
        "What is the waiting period for pre-existing diseases (PED) to be covered?",
        "Does this policy cover maternity expenses, and what are the conditions?",
        "What is the waiting period for cataract surgery?",
        "Are the medical expenses for an organ donor covered under this policy?",
        "What is the No Claim Discount (NCD) offered in this policy?",
        "Is there a benefit for preventive health check-ups?",
        "How does the policy define a 'Hospital'?",
        "What is the extent of coverage for AYUSH treatments?",
        "Are there any sub-limits on room rent and ICU charges for Plan A?"
    )
}

# Convert to JSON
$jsonBody = $body | ConvertTo-Json -Depth 10

Write-Host "Request Body:" -ForegroundColor Cyan
Write-Host $jsonBody
Write-Host ""

# Make the API call
try {
    Write-Host "Sending request to API..." -ForegroundColor Yellow
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/hackrx/run" -Method POST -Headers $headers -Body $jsonBody
    
    Write-Host "API Response:" -ForegroundColor Green
    $response | ConvertTo-Json -Depth 10
    
    # Check if we got answers
    if ($response.answers) {
        Write-Host ""
        Write-Host "Number of answers received: $($response.answers.Count)" -ForegroundColor Green
        Write-Host "First answer: $($response.answers[0])" -ForegroundColor Cyan
    }
    
} catch {
    Write-Host "API Call Failed: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $responseBody = $reader.ReadToEnd()
        Write-Host "Error Response: $responseBody" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Test completed!" -ForegroundColor Green
Read-Host "Press Enter to continue..." 