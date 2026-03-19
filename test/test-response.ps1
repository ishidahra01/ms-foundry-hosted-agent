param(
    [string]$BaseUrl = "http://localhost:8088",
    [string]$Prompt = "How to deploy foundry hosted agents?",
    [switch]$ShowJson
)

$body = @{
    input = $Prompt
    stream = $false
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod `
        -Uri "$BaseUrl/responses" `
        -Method Post `
        -Body $body `
        -ContentType "application/json"
}
catch {
    Write-Error $_
    exit 1
}

if ($ShowJson) {
    Write-Host "=== Full response JSON ===" -ForegroundColor Cyan
    $response | ConvertTo-Json -Depth 30
    Write-Host ""
}

$textParts = @(
    foreach ($item in $response.output) {
        if ($item.type -ne "message") {
            continue
        }

        foreach ($content in $item.content) {
            if ($content.type -eq "output_text" -and $content.text) {
                $content.text
            }
        }
    }
)

if ($textParts.Count -gt 0) {
    Write-Host "=== Assistant text ===" -ForegroundColor Green
    $textParts -join "`n`n"
    exit 0
}

Write-Warning "No assistant output_text was found in response.output."
$response | ConvertTo-Json -Depth 30
exit 2