#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import subprocess
import ctypes
import os

def _run_build_process_timeout(*args, timeout):
    cmd_input = []
    cmd_input.append(' '.join(map('"{}"'.format, args)))
    cmd_input.append('exit\n')
    with subprocess.Popen(('cmd.exe', '/k'), encoding='utf-8', stdin=subprocess.PIPE, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP) as proc:
        proc.stdin.write('\n'.join(cmd_input))
        proc.stdin.close()
        try:
            proc.wait(timeout)
            if proc.returncode != 0:
                raise RuntimeError('Build failed!')
        except subprocess.TimeoutExpired:
            print('Sending keyboard interrupt')
            for _ in range(3):
                ctypes.windll.kernel32.GenerateConsoleCtrlEvent(1, proc.pid)
                time.sleep(1)
            try:
                proc.wait(10)
            except:
                proc.kill()
            raise KeyboardInterrupt

def main():
    try:
        _run_build_process_timeout("ping 127.0.0.1 -t && ping 127.0.0.1 -t",
                                    timeout=30)
        open(os.environ["GITHUB_OUTPUT"],"w").write("finish=true")
    except KeyboardInterrupt as e:
        open(os.environ["GITHUB_OUTPUT"],"w").write("finish=false")

if __name__ == '__main__':
    main()