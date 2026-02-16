Write-Host 'Running flake8 with "wemake-python-styleguide (WPS)" plugin'
flake8 . --select=WPS

Write-Host 'Running mypy'
mypy --exclude-gitignore .
