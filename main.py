#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Madhav (https://github.com/madhav-mknc)


from os import system as cmd

COMMAND = "python app.py"
# COMMAND = "python3 app.py"

# run app.py
def main():
    from app import start_chat_server
    print("[CHATBOT GOING ONLINE...]")
    start_chat_server()

# install dependencies
def install():
    print("[*] Installing the Requirements")
    cmd("pip install -r requirements.txt")
    
# mains
if __name__ == "__main__":
    try:
        main()
    except ModuleNotFoundError as e:
        print(e)
        install()
        main()
    except KeyboardInterrupt:
        print("\n[exitted]")



        

