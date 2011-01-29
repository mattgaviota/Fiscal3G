#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from os import path
import os
import shlex
import shutil
from subprocess import call

CONFIG_DIR = path.abspath("configs")
INBOX = path.abspath("inbox.mbox")
INBOX_ARCHIVE = path.abspath("inbox_archive.mbox")

def execute(command):
    error = call(shlex.split(command))
    return error

def get_config_files():
    config_files = [path.join(CONFIG_DIR, file) for file in os.listdir(CONFIG_DIR)]
    config_files = [file for file in config_files if path.isfile(file)]
    return config_files

def get_sms(config_file):
    error = execute("src/getsms.sh %s" % config_file)
    return error

def main():
    config_files = get_config_files()

    print("Revisando mensajes:")
    for config_file in config_files:
        print("  %s" % path.split(config_file)[-1])
        print("    %d" % get_sms(config_file))

    print("Procesando mensajes:")
    inbox = open(INBOX).read()

    messages = (message for message in inbox.split("\n\nFrom") if message)
    for message in messages:
        lines = message.splitlines()
        print(lines[0])

        h_from = lines[0].split("@")[0][-10:]
        print("From: %s" % h_from)
        h_time = lines[0].split()[-2]
        print("Time: %s" % h_time)

        body = "\n".join(message.split("\n\n")[1:]).strip()
        print(body)

if __name__ == "__main__":
    exit(main())
