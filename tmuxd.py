#!/usr/bin/env python

import subprocess

def runTmux(cmd):
    try:
        return subprocess.check_output('tmux ' + cmd, shell = True)
    except subprocess.CalledProcessError as e:
        return None

class TmuxClient:
    def __init__(self):
        self.sessions = {}
    def saveAll(self):
        res = runTmux("list-sessions -F '#S'")
        sessions = res.split('\n')
        for session in sessions:
            if session == '':
                continue
            self.sessions[session] = TmuxSession(session)
            self.sessions[session].saveAll()

class TmuxSession:
    def __init__(self, name):
        self.windows = []
        self.name = name
    def saveAll(self):
        res = runTmux("list-windows -t {}".format(self.name) + " -F '#{window_name} #{pane_current_path}'")
        print res

class TmuxWindow:
    def __init__(self):
        self.workDir = None
        self.session = None
    def restore(self):
        cmd = 'new-window -c {} -t {}'.format(self.workDir, self.session)
        if not runTmux(cmd):
            return False

def main():
    client = TmuxClient()
    client.saveAll()

if __name__ == '__main__':
    main()
