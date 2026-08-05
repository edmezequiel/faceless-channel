$env:PYTHONUTF8="1"
$env:PYTHONPATH="."
Write-Host "Iniciando LangGraph Engine (Faceless Channel)..." -ForegroundColor Green
& ".\.venv\Scripts\python.exe" src/core/engine.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "Falha na execução do Engine." -ForegroundColor Red
} else {
    Write-Host "Execução finalizada com sucesso." -ForegroundColor Green
}
