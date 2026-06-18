$envPath = Join-Path $PSScriptRoot ".env"

if (!(Test-Path -LiteralPath $envPath)) {
    throw "Missing .env file at $envPath"
}

foreach ($rawLine in Get-Content -LiteralPath $envPath) {
    $line = $rawLine.Trim()
    if ([string]::IsNullOrWhiteSpace($line) -or $line.StartsWith("#")) {
        continue
    }

    $separatorIndex = $line.IndexOf("=")
    if ($separatorIndex -lt 1) {
        continue
    }

    $name = $line.Substring(0, $separatorIndex).Trim()
    $value = $line.Substring($separatorIndex + 1).Trim()

    if (($value.StartsWith('"') -and $value.EndsWith('"')) -or ($value.StartsWith("'") -and $value.EndsWith("'"))) {
        $value = $value.Substring(1, $value.Length - 2)
    }

    [Environment]::SetEnvironmentVariable($name, $value, "Process")
    Write-Host "Loaded $name"
}

if ([string]::IsNullOrWhiteSpace($env:TF_VAR_hf_token)) {
    Write-Warning "TF_VAR_hf_token is empty. Paste your Hugging Face token into .env before running Terraform."
}
