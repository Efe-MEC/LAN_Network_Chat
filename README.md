It is a non-interface chat program that works in private networks.

How to Use

Download the repo.
Go to downloaded directory in terminal.
Install the python and pyDes library.
Run the Service_Announcer.py (python Service_Anouncer.py). Then, please enter your name.
Run the Peer_Discovery.py (Peer_Discovery.py).
Run the Chat_Initiator.py (python Chat_Initiator.py).
Run the Chat_Responder.py (python Chat_Responder.py).
Note: Do not close any program during execution, and run each one separately.
Go back to the Chat_Initiator.py terminal. You will see the menu for operations. Please enter the number (inside the parentheses) of what you want to do. Enter 1 to see the users on the Network. Enter 2 to start the chat. Enter 3 to view the logs or history. Enter 4 for exit the program.
If you want to chat, please first enter 1 to see the users. Then enter the 2 to start a chat.  After entering 2, the program will ask you to enter the name of the user you want to chat with. Please enter the username exactly as displayed. Then, the program will ask you to choose the chat type you prefer, which can be secure or unsecure. Enter 1 for secure and enter 2 for unsecure.
If you enter 1 (secure chat), the program will ask for a number to use for encrypting the message. Please enter a number. After the connection is established, the program will display a message. Then, enter your message.
If you enter 2 (unsecure chat), please enter your message.

Limitations

The program only works on Local Area Network (LAN).
Chat_Responder.py handles one incoming connection at a time and may block others during processing.
Do not send more than 980 characters using unsecure chat and 260 characters using secure chat.
