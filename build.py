import time
import subprocess
import ctypes
import os

def _run_build_process_timeout(cmd_list, timeout):
    powershell_script = [
        "$commands = @(",
        *[f'"{cmd}"' for cmd in cmd_list],
        ")",
        "",
        "foreach ($cmd in $commands) {",
        '    Write-Host "[Executing] $cmd" -ForegroundColor Cyan',
        '    $process = Start-Process -FilePath "$Env:ComSpec" -PassThru -NoNewWindow -Wait -ArgumentList "/c", $cmd',
        "    $exitCode = $process.ExitCode",
        "    if ($exitCode -ne 0) {",
        '        Write-Host "[Failed] Command exited with code: $exitCode - $cmd" -ForegroundColor Red',
        "        exit $exitCode",
        "    }",
        '    Write-Host "[Success] $cmd" -ForegroundColor Green',
        "}",
        "",
    ]

    with subprocess.Popen(
        (
            "powershell.exe",
            "-NoProfile",
            "-NonInteractive",
            "-Command",
            "-",
        ),
        encoding="utf-8",
        stdin=subprocess.PIPE,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
    ) as proc:
        proc.stdin.write("\n".join(powershell_script))
        proc.stdin.write("\n" * 30)
        proc.stdin.close()

        try:
            proc.wait(timeout)
            if proc.returncode != 0:
                print(f"Build failed! Last exit code: {proc.returncode}")
                exit(proc.returncode)
        except subprocess.TimeoutExpired:
            print("Sending keyboard interrupt")
            for _ in range(30):
                ctypes.windll.kernel32.GenerateConsoleCtrlEvent(1, proc.pid)
                time.sleep(1)
            try:
                proc.wait(10)
            except:
                proc.kill()
            raise KeyboardInterrupt

def main():
    try:
        build_commands = [
            "ninja -C out/nw nwjs",
            "ninja -C out/Release_x64 node",
            "ninja -C out/nw copy_node",
            "ninja -C out/nw dump",
            "ninja -C out/nw dist",
        ]
        _run_build_process_timeout(build_commands, timeout=3 * 60 * 60)
        open(os.environ["GITHUB_OUTPUT"], "w").write("finish=true")
    except KeyboardInterrupt as _:
        open(os.environ["GITHUB_OUTPUT"], "w").write("finish=false")
    except Exception as _:
        exit(1)


if __name__ == "__main__":
    main()
