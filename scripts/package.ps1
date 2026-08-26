[CmdletBinding()]
param(
    [switch]$Release,
    [ValidatePattern('^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$')]
    [string]$Version
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$root = Split-Path -Parent $PSScriptRoot
$versionFile = Join-Path $root 'VERSION'
if (-not (Test-Path -LiteralPath $versionFile -PathType Leaf)) {
    throw 'VERSION is required for package naming.'
}
$sourceVersion = (Get-Content -LiteralPath $versionFile -Raw).Trim()
if ($sourceVersion -notmatch '^\d+\.\d+\.\d+$') {
    throw "VERSION must be stable SemVer: $sourceVersion"
}
$version = if ([string]::IsNullOrWhiteSpace($Version)) { $sourceVersion } else { $Version }
if ($Release -and $version -ne $sourceVersion) {
    throw "Release package version $version must match VERSION $sourceVersion."
}
$dist = Join-Path $root 'dist'
$stage = Join-Path $dist 'stage'
$skillName = "icarus-open-source-governance.skill"
$zipName = "icarus-open-source-governance-$version.zip"
$includes = @(
    'SKILL.md', 'README.md', 'README.zh-CN.md', 'LICENSE', 'CHANGELOG.md', 'CONTRIBUTING.md',
    'SECURITY.md', 'SUPPORT.md', 'CODE_OF_CONDUCT.md', 'compatibility.md', 'VERSION', '.icarus-open-source.example.yml',
    'assets', 'docs/brand', 'schemas', 'references', 'templates', 'scripts', 'evals', '.github'
)

$isDirty = [bool](git -C $root status --porcelain)
if ($Release -and $isDirty) {
    throw 'Release packaging requires a clean tracked working tree.'
}

New-Item -ItemType Directory -Force -Path $dist | Out-Null
Get-ChildItem -LiteralPath $dist -Filter 'icarus-open-source-governance-*.zip' -File -Force |
    Remove-Item -Force
if (Test-Path -LiteralPath $stage) {
    Remove-Item -LiteralPath $stage -Recurse -Force
}
New-Item -ItemType Directory -Force -Path $stage | Out-Null

foreach ($entry in $includes) {
    $source = Join-Path $root $entry
    if (-not (Test-Path -LiteralPath $source)) {
        throw "Required package source is missing: $entry"
    }
    if ((Get-Item -LiteralPath $source -Force).PSIsContainer) {
        Get-ChildItem -LiteralPath $source -File -Recurse -Force |
            Where-Object { $_.FullName -notmatch '[\\/](__pycache__|dist)[\\/]' } |
            ForEach-Object {
                $relative = [IO.Path]::GetRelativePath($root, $_.FullName)
                $target = Join-Path $stage $relative
                New-Item -ItemType Directory -Force -Path (Split-Path -Parent $target) | Out-Null
                Copy-Item -LiteralPath $_.FullName -Destination $target -Force
            }
    } else {
        Copy-Item -LiteralPath $source -Destination (Join-Path $stage $entry) -Force
    }
}

$skillPath = Join-Path $dist $skillName
$zipPath = Join-Path $dist $zipName
Remove-Item -LiteralPath $skillPath, $zipPath -Force -ErrorAction SilentlyContinue
Add-Type -AssemblyName System.IO.Compression.FileSystem
[IO.Compression.ZipFile]::CreateFromDirectory(
    $stage,
    $skillPath,
    [IO.Compression.CompressionLevel]::Optimal,
    $false
)
[IO.Compression.ZipFile]::CreateFromDirectory(
    $stage,
    $zipPath,
    [IO.Compression.CompressionLevel]::Optimal,
    $false
)

$artifacts = @($skillPath, $zipPath) | ForEach-Object {
    [ordered]@{
        name = [IO.Path]::GetFileName($_)
        sha256 = (Get-FileHash -LiteralPath $_ -Algorithm SHA256).Hash.ToLowerInvariant()
    }
}
$stagedFiles = Get-ChildItem -LiteralPath $stage -File -Recurse | Sort-Object FullName | ForEach-Object {
    [ordered]@{
        path = [IO.Path]::GetRelativePath($stage, $_.FullName).Replace('\', '/')
        sha256 = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
    }
}
$sourceCommit = (git -C $root rev-parse HEAD).Trim()
$manifest = [ordered]@{
    schemaVersion = 1
    version = $version
    sourceCommit = $sourceCommit
    sourceTree = $(if ($isDirty) { 'dirty' } else { 'clean' })
    artifacts = $artifacts
    stagedFiles = $stagedFiles
}
$manifestPath = Join-Path $dist 'manifest.json'
$manifest | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $manifestPath -Encoding utf8NoBOM
($artifacts | ForEach-Object { "{0}  {1}" -f $_.sha256, $_.name }) | Set-Content -LiteralPath (Join-Path $dist 'SHA256SUMS.txt') -Encoding utf8NoBOM
Write-Output "PASS: staged $($stagedFiles.Count) file(s) once"
Write-Output "PASS: created $skillName and $zipName from the same staged tree"
Write-Output "PASS: wrote manifest.json and SHA256SUMS.txt"
