from socket import *
import sys
import threading
import _thread

JAIL_RESPONSE = "You got {} years of jail time!"
FREE_RESPONSE = "You are free!"
WELCOME = "You are Prisoner {}."

clients = []

serverPort = int(sys.argv[-1])
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
game_thread = None

def game_func():

    global clients

    clientA = clients[0][0]
    clientB = clients[1][0]

    clientA.send("Let's begin!".encode())
    clientB.send("Let's begin!".encode())

    answerA = clientA.recv(1024).decode()
    answerB = clientB.recv(1024).decode()

    print("Prisoner 1 said {}".format(answerA))
    print("Prisoner 2 said {}".format(answerB))

    if answerA == answerB:
        if answerA == 'C':
            clientA.send(JAIL_RESPONSE.format(1).encode())
            clientB.send(JAIL_RESPONSE.format(1).encode())
            print("Both prisoners cooperated and received 1 year!")
        else:
            clientA.send(JAIL_RESPONSE.format(2).encode())
            clientB.send(JAIL_RESPONSE.format(2).encode())
            print("Both prisoners betrayed and received 2 years!")
    else:
        if answerA == 'C':
            clientA.send(JAIL_RESPONSE.format(3).encode())
            clientB.send(FREE_RESPONSE.encode())
            print("Prisoner 2 betrayed Prisoner 1 and went free, Prisoner 1 received 3 years!")
        else:
            clientA.send(FREE_RESPONSE.encode())
            clientB.send(JAIL_RESPONSE.format(3).encode())
            print("Prisoner 1 betrayed Prisoner 1 and went free, Prisoner 2 received 3 years!")

    clientA.close()
    clientB.close()

    clients = []

    return

def start_game():
    global game_thread
    game_thread = threading.Thread(target=game_func)
    game_thread.start()
    print("New Interrogation Thread spawned")

def deny_connection(clientSocket, clientAddr):
    clientSocket.send("Server is busy with an interrogation. Try to connect again later.".encode())
    clientSocket.close()

def check_game_thread():
    global game_thread
    if game_thread:
        game_thread.join(0)
        if not game_thread.is_alive():
            game_thread = None

while True:
    client, addr = serverSocket.accept()

    print("A new prisoner is trying to connect to the Jailer server on {}:{}".format(addr[0], addr[1]))

    check_game_thread()

    if game_thread:
        print("Two players are already being interrogated. Can't start a new interrogation.")
        deny_connection(client, addr)
        continue
    
    clients.append((client, addr))

    print("Current number of available prisoners is {}".format(len(clients)))

    welcome_message = WELCOME.format(len(clients))

    if len(clients) == 1:
        welcome_message += "\nWaiting for a second prisoner to join."
        print("One prisoner joined, waiting for another prisoner to join.")

    client.send(welcome_message.encode())

    if len(clients) == 2:
        print("Two prisoners available, let's begin!")
        start_game()
    
