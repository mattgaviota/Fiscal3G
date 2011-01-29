#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from os import path
from subprocess import call
from tempfile import mkstemp
import os
import shlex
import shutil
import time

CONFIG_DIR = path.abspath("configs")
INBOX = path.abspath("inbox.mbox")
TO_DB = path.abspath("to_db")
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
        print("  %s, %d" % (path.split(config_file)[-1], get_sms(config_file)))


    print("Procesando mensajes:")
    try:
        inbox = open(INBOX).read()
    except IOError:
        inbox = ""

    if inbox:
        with open(INBOX_ARCHIVE, "a") as file:
            file.write(inbox)

        os.remove(INBOX)

        temp_files = []
        messages = (message for message in inbox.split("\n\nFrom") if message)
        for message in messages:
            lines = message.splitlines()

            h_from = lines[0].split("@")[0][-10:]
            h_time = lines[0].split()[-2]
            body = "\n".join(message.split("\n\n")[1:]).strip()

            content = (
                "%s %s\n"
                "%s %s\n"
                "%s\n"
                "%s\n" % (
                    time.strftime("%Y-%m-%d"), h_time,
                    time.strftime("%Y-%m-%d"), time.strftime("%T"),
                    h_from,
                    body,
                    ))

            print("  >> %s %s %s" % (h_time, h_from, body))

            temp_fd, temp_name = mkstemp(".to_query", "", TO_DB)
            with os.fdopen(temp_fd, "w") as file:
                file.write(content)

#        print("Impactando en la base de datos:")
#        for file in temp_files:
#            execute("python src/query.py %s" % file)

    else:
        print("No hay novedades de momento...")


if __name__ == "__main__":
    exit(main())
