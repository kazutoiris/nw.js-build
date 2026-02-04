#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import subprocess
import ctypes
import os

def _run_build_process_timeout(cmd_input, timeout):
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
        cmd_input = []
        cmd_input.append("ninja -C out/nw nwjs")
        cmd_input.append("ninja -C out/Release_x64 node")
        cmd_input.append("ninja -C out/nw copy_node")
        cmd_input.append("ninja -C out/nw dist")
        _run_build_process_timeout(cmd_input, timeout=4*60*60)
        open(os.environ["GITHUB_OUTPUT"],"w").write("finish=true")
    except KeyboardInterrupt as e:
        open(os.environ["GITHUB_OUTPUT"],"w").write("finish=false")
    except Exception as e:
        open(os.environ["GITHUB_OUTPUT"],"w").write("finish=true")
        exit(1)
if __name__ == '__main__':
    main()
