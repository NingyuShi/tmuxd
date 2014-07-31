#!/usr/bin/env python

import subprocess
import json

def runTmux(cmd):
    try:
        return subprocess.check_output('tmux ' + cmd, shell = True)
    except subprocess.CalledProcessError as e:
        return None

class TmuxClient:
    def __init__(self):
        self.sessions = {}
    def saveAll(self, obj):
        res = runTmux("list-sessions -F '#S'")
        sessions = res.splitlines()
        for session in sessions:
            if session == '':
                continue
            self.sessions[session] = TmuxSession(session)
            obj[session] = {}
            self.sessions[session].saveAll(obj[session])

class TmuxSession:
    def __init__(self, name):
        self.windows = []
        self.name = name
    def saveAll(self, obj):
        res = runTmux("list-windows -t {}".format(self.name) + " -F '#{window_index} #{window_name} #{pane_current_path}'")
        windows = res.splitlines()
        i = 0
        for win in windows:
            if win == '':
                continue
            tokens = win.strip().split(' ')
            obj[i] = {}
            self.windows.append(TmuxWindow(tokens[0], tokens[1], tokens[2], self.name))
            self.windows[i].save(obj[i])
            i += 1


class TmuxWindow:
    def __init__(self, index, name, workDir, session):
        self.index = index
        self.name = name
        self.workDir = workDir
        self.session = session
    def restore(self):
        cmd = 'new-window -c {} -t {}'.format(self.workDir, self.session)
        if not runTmux(cmd):
            return False
    def save(self, obj):
        obj['name'] = self.name
        obj['workDir'] = self.workDir
        obj['session'] = self.session
        obj['history'] = runTmux("capture-pane -p -S -32768 -t {}:{}".format(self.session, self.index))

def main():
    client = TmuxClient()
    obj = {}
    client.saveAll(obj)
    print json.dumps(obj, indent=2)

if __name__ == '__main__':
    main()
