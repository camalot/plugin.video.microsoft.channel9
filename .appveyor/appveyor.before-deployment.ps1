$commitMessageRegex = "^\[deploy\:(pre-release|draft|release)\]$";
if ( $env:APPVEYOR_REPO_BRANCH -eq "master" ) {
  $env:CI_DEPLOY_GITHUB = $true;
  # FTP hangs on the build server and never completes.
  $env:CI_DEPLOY_FTP = $false;
} else {
  # Do not assign a release number or deploy
  $env:CI_DEPLOY_GITHUB = $false;
  $env:CI_DEPLOY_FTP = $false;
}