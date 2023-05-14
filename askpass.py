from sys import argv
from os import environ

print(argv)
if 'username' in argv[1].lower():
    print("1")
    print(environ['GIT_USERNAME'])
    exit()

if 'Password' in argv[1].lower():
    print("2")
    print(environ['GIT_PASSWORD'])
    exit()

exit(1)