$ErrorActionPreference = 'Stop'

# 1) 配置代理（如无代理可注释掉）
$env:https_proxy = "http://127.0.0.1:7890"
$env:http_proxy  = "http://127.0.0.1:7890"
$env:all_proxy   = "socks5://127.0.0.1:7890"

# 2) 验证代理变量
Write-Host "https_proxy = $env:https_proxy"

# 进入脚本所在目录（项目根）
Set-Location -Path (Split-Path -Parent $MyInvocation.MyCommand.Path)

# 确保存在 README 文件
$readme = Join-Path (Get-Location) 'readme.md'
if (-not (Test-Path $readme)) { "# Project" | Out-File -FilePath $readme -Encoding utf8 -Append }

# 3) 循环提交 5 次
for ($i = 1; $i -le 5; $i++) {
    $line = "Auto update $i at $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    Add-Content -Path $readme -Value $line -Encoding utf8

    git add ./
    git commit -m "update $i"
    git push

    Start-Sleep -Seconds 1
}

Write-Host "All commits done."


