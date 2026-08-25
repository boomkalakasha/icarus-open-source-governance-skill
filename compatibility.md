# Compatibility

The local validator, scanner, eval checker, and package script are verified with Python 3.12+ and PowerShell 7 on Windows. They use the Python standard library, Git for `--history`, and PowerShell's built-in archive/hash commands.

The generated `.skill` and `.zip` files are local artifacts; installation behavior in a particular coding host is `NOT_VERIFIED` unless that host's documented installer is run separately. GitHub Actions, CodeQL, rulesets, and release pages are remote evidence gates and cannot be confirmed from this repository alone.
