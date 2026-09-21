<#
.SYNOPSIS
  Commit and push this folder to GitHub; GitHub Actions then publishes site/ to Pages.

.DESCRIPTION
  This folder became its own git repository on 2026-09-21 at the owner's request (a child
  repository inside Code2, like NBG/website). The published page is built from site/ by
  .github/workflows/pages.yml on every push to main.

  Run from this folder:
      powershell -ExecutionPolicy Bypass -File .\deploy.ps1                       # commit + push
      powershell -ExecutionPolicy Bypass -File .\deploy.ps1 -Message "new prices"  # with a message
      powershell -ExecutionPolicy Bypass -File .\deploy.ps1 -DryRun                # show what would happen

  Requires: git and gh (logged in as vivian4fb).
  Live URL: https://vivian4fb.github.io/oxyniti-yield-calc/
#>
param(
    [string]$Owner    = "vivian4fb",
    [string]$RepoName = "oxyniti-yield-calc",
    [string]$Message  = "",
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$site = Join-Path $here "site"

if (-not (Test-Path $site)) { throw "site/ not found next to deploy.ps1 - nothing to publish." }

# Refuse to publish a build that still carries placeholder tokens (2_Business rule 4).
$bad = Get-ChildItem $site -Recurse -Include *.html,*.js,*.css,*.md |
    Where-Object { $_.FullName -notmatch "\\vendor\\" } |
    Select-String -Pattern "YOUR_|XXXXX|TODO|info@|\+91 98765" -List
if ($bad) {
    $bad | ForEach-Object { Write-Host ("PLACEHOLDER: {0}:{1}" -f $_.Path, $_.LineNumber) }
    throw "Placeholder tokens found in site/. Fix them before publishing."
}

if ($Message -eq "") { $Message = "update site $(Get-Date -Format 'yyyy-MM-dd HH:mm')" }

if ($DryRun) {
    Write-Host "DRY RUN - the real run would do:"
    Write-Host "  git -C `"$here`" add -A"
    Write-Host "  git -C `"$here`" commit -m `"$Message`""
    Write-Host "  git -C `"$here`" push origin main"
    Write-Host "  (GitHub Actions then deploys site/ to https://$Owner.github.io/$RepoName/)"
    exit 0
}

if (-not (Test-Path (Join-Path $here ".git"))) {
    throw "This folder is not a git repository. The initial repository was created on 2026-09-21; if it is gone, run: git init -b main; git remote add origin https://github.com/$Owner/$RepoName.git"
}

& git -C $here add -A
& git -C $here commit -m $Message
# exit 1 from commit means "nothing to commit" - acceptable; the push still runs.
& git -C $here push origin main
if ($LASTEXITCODE -ne 0) { throw "git push failed" }

Write-Host ""
Write-Host ("Pushed. GitHub Actions publishes site/ within about a minute: https://{0}.github.io/{1}/" -f $Owner, $RepoName)
Write-Host ("Watch the run: gh run list --repo {0}/{1} --limit 1" -f $Owner, $RepoName)
