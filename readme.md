Too easy to have a readme instruction for it LoL.

Just open md5.exe and enter the paths that the program prompts.

Note that you can drag a folder or file to the .exe and it can be considered as one of the compare object for convenience.

And on other platforms, you can run md5.py via the python interpreter. The .exe file is just a packaged executable, nothing more.

> BTW, this little script use emojis for a better command line UI, but some older device may have problem decoding them ... Not a big deal

```commandline
pyinstaller -F md5.py --icon="./icon.ico"
```