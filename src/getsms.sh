#!/bin/bash
( gnokii --config "$1" --getsms SM 0 END --append-file inbox.mbox --delete 
)2>>getsms.log
