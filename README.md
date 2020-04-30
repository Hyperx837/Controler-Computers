# Control Computer

## what can this script do?
it can control a keyboard of a computer with another computer
eg:- type windows key in my computer and it will be pressed in another computer

control.py:- run in the computer that you use (for now let's call it server)
client.py :- run in the computer that you want to control (client)

## How to run this script
if you have python3 and pip installed you can run **pip install -r requirements.txt** in both computers
**if you get an error you might have an error in python installation**

and then you have to change the keyword argument ip in client.py to the server's ip address get the client.py and change the ip variable in the @connect decorator to your computers ip address (the computer you use).

run the python script as you normally do **python3 script.py** for unix and **python script.py** for windows
*first run the control.py script*

*Do not run the both scripts same time in your own computer because it will be stuck in an infinite loop because when you type a key client.py will type the same key and then server.py will detect the key that client.py pressed and it will think that you typed that and then it will continue non-stop*
