param(
  [string]$RepoUrl = "https://github.com/zeyuzhangzyz/open-source-hardening-skills.git",
  [string]$CloneDir = "$HOME\.claude\repos\open-source-hardening-skills",
  [string]$SkillsDir = "$HOME\.claude\skills"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
  throw "Missing required command: git"
}

$gitDir = Join-Path $CloneDir ".git"

if (Test-Path $gitDir) {
  & git -C $CloneDir remote set-url origin $RepoUrl | Out-Host
  & git -C $CloneDir pull --ff-only | Out-Host
} else {
  New-Item -ItemType Directory -Force -Path (Split-Path -Parent $CloneDir) | Out-Null
  & git clone $RepoUrl $CloneDir | Out-Host
}

New-Item -ItemType Directory -Force -Path $SkillsDir | Out-Null

# Only replace this pack's own skill directories — never touch unrelated entries
Get-ChildItem -Path (Join-Path $CloneDir "skills") -Directory | ForEach-Object {
  $targetDir = Join-Path $SkillsDir $_.Name
  if (Test-Path $targetDir) {
    Remove-Item -Recurse -Force $targetDir
  }
  Copy-Item -Recurse -Force $_.FullName $targetDir
}

$installedCount = (Get-ChildItem -Path (Join-Path $CloneDir "skills") -Directory).Count
Write-Host "Installed $installedCount skills to $SkillsDir"
Write-Host "Restart Claude Code or run /reload if the skills do not appear immediately."
