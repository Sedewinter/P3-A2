#Code pour le be:bi parent
#Importing the modules needed
from microbit import *
import radio
import music
import urandom # type: ignore #this module choose the best available seed for cryptographically secure PRNG.
# initial configuration
radio.on()
radio.config(group=99, power=5)
key = "BROOKS"
challenge=""
milk = 0
biberon = Image("19991:" "09090:" "92229:" "09290:" "09290")

#Cryptage
#Hashing: this is the default hashing
def hashing(string):
	"""
	Hachage d'une chaîne de caractères fournie en paramètre.
	Le résultat est une chaîne de caractères.
	Attention : cette technique de hachage n'est pas suffisante (hachage dit cryptographique) pour une utilisation en dehors du cours.

	:param (str) string: la chaîne de caractères à hacher
	:return (str): le résultat du hachage
	"""
	def to_32(value):
		"""
		Fonction interne utilisée par hashing.
		Convertit une valeur en un entier signé de 32 bits.
		Si 'value' est un entier plus grand que 2 ** 31, il sera tronqué.

		:param (int) value: valeur du caractère transformé par la valeur de hachage de cette itération
		:return (int): entier signé de 32 bits représentant 'value'
		"""
		value = value % (2 ** 32)
		if value >= 2**31:
			value = value - 2 ** 32
		value = int(value)
		return value

	if string:
		x = ord(string[0]) << 7
		m = 1000003
		for c in string:
			x = to_32((x*m) ^ ord(c))
		x ^= len(string)
		if x == -1:
			x = -2
		return str(x)
	return ""
#Vigenere 'encryption'
def vigenere(message, key, decryption=False):
    text = ""
    key_length = len(key)
    key_as_int = [ord(k) for k in key]

    for i, char in enumerate(str(message)):
        key_index = i % key_length
        #Letters encryption/decryption
        if char.isalpha():
            if decryption:
                modified_char = chr((ord(char.upper()) - key_as_int[key_index] + 26) % 26 + ord('A'))
            else : 
                modified_char = chr((ord(char.upper()) + key_as_int[key_index] - 26) % 26 + ord('A'))
            #Put back in lower case if it was
            if char.islower():
                modified_char = modified_char.lower()
            text += modified_char
        #Digits encryption/decryption
        elif char.isdigit():
            if decryption:
                modified_char = str((int(char) - key_as_int[key_index]) % 10)
            else:  
                modified_char = str((int(char) + key_as_int[key_index]) % 10)
            text += modified_char
        else:
            text += char
    return text
#We send the packet in the Type Length Value format using vigenere encryption
def send_packet(key, packet_type, content):
    """
    Envoie de données fournie en paramètres
    Cette fonction permet de construire, de chiffrer puis d'envoyer un paquet via l'interface radio du micro:bit

    :param (str) key:           Clé de chiffrement
           (str) packet_type:   Type du paquet à envoyer
           (str) content:       Données à envoyer
	:return none
    """
    radio.on()
    radio.config(group=99)
    packet="{} | {} | {}".format(packet_type,len(content),content)
    radio.send(vigenere(packet, key)) #Send the message with encryption with the key

def unpack_data(encrypted_packet, key):
    """
    Déballe et déchiffre les paquets reçus via l'interface radio du micro:bit
    Cette fonction renvoie les différents champs du message passé en paramètre.

    :param (str) encrypted_packet: Paquet reçu
           (str) key:              Clé de chiffrement
    :return: (str) packet_type:   Type de paquet
             (int) length:        Longueur de la donnée en caractères
             (str) message:       Données reçues
    """
    try:
        decrypted_packet = vigenere(encrypted_packet, key, decryption=True) #Decrypt the packet with Vigenere
        packet_type, length, value = decrypted_packet.split(" | ") #Split the string in 3 to separate TLV into a list
        if len(value) == int(length): #check if the Length in TLV is identical to the message lenght.
            return packet_type, int(length), value #If so, it returns the values
        else:
            return None, None, None
    except ValueError:
        return None, None, None
    except Exception as e:
        print("Erreur lors du décryptage ou du traitement du paquet: {}".format(e))
        return None, None,None

# challenge 
def calculate_challenge(bits=32):
    return urandom.getrandbits(bits)

def calculate_challenge_response(challenge):
    """
    Calcule la réponse au challenge initial de connection avec l'autre micro:bit

    :param (str) challenge:            Challenge reçu
	:return (srt)challenge_response:   Réponse au challenge
    """
    challenge = int(challenge) #Make sure the challenge is converted into integers
    response = str(challenge * 2) #We multiply the challenge by 2 as a security measure
    return response
        
def send_hashed_response(response):
    print("Received",response)
    hashed_response=hashing(response) #We hash the number. Since the sender already has the initial number, sending a hash is no problem.
    print("R: {}".format((response)))
    send_packet(key, "2", str(hashed_response)) #Sending the hashed number
    return hashed_response
def establish_connexion(key):
    """
    Etablissement de la connexion avec l'autre micro:bit
    Si il y a une erreur, la valeur de retour est vide

    :param (str) key:                  Clé de chiffrement
	:return (srt)challenge_response:   Réponse au challenge
    """
    sent=0
    display.scroll("co") #Display co for letting know the user the connexion process has started
    print ("Co Init")
    while True:
        message= radio.receive() #Listen for messages
        if message:
            packet_type, length, value = unpack_data(message,key)
            if str(value).isdigit(): #Check if the message is a number, in which case it is likely a challenge.
                challenge_response=calculate_challenge_response(value)
                print(challenge_response)
                send_hashed_response(challenge_response)
            if value=="accepted":
                key=challenge
                return "connected"

def distance():
    """
    Mesurer la distance entre les deux microbits, et alerter si elle est trop grande.
    pre:/
    post: Fait sonner une alarme et affiche "FAR"
    """
    too_far = -78 #Signal strength treshold
    message = radio.receive_full() #We receive in the full format, meaning we also receive signal strength.
    if message:
        print(message)
        signal = message[1]  #Get the strength part of the message
        if signal < too_far:  #Check if signal is lower than treshold 
            print("Too far detected")
            music.play(music.BA_DING)
            display.show('FAR!')
            sleep(1000)#Sleep is so we don't spam
        else: 
            sleep(500)
            




# milk quantity gestion
def milk_quantity(milk):
    """
    Permettre aux parents d'enregister les doses de lait quotidiennes, les stocker et les afficher sur les be:bi.
    Les doses de lait sont synchronisés.
    pre: milk var to stock it across sessions
    post: Displays, sync, and allow reset by pressing both buttons.
    """
    max_milk = 10 #Max recommended daily milk quantity for a baby
    min_milk = 0
    for _ in range(5): #We loop 5 times before exiting
        if button_a.is_pressed() and button_b.is_pressed(): #Reset buttons
            milk = 0
            send_packet(key, "milk", str(milk))
            display.show(milk)
            sleep(1000)
        elif button_a.get_presses(): #Left button removes milk
            if milk > min_milk:
                milk -= 1
                send_packet(key, "milk", str(milk))
                display.show(milk)
                sleep(1000)
        elif button_b.get_presses():#Right button adds milk
            if milk < max_milk:
                milk += 1
                send_packet(key, "milk", str(milk))
                display.show(milk)
                sleep(1000)
            else: #Max milk quantity reached
                display.show("MAX!")
                music.play(music.WAWAWAWAA, wait=False)
        sleep(100)
        display.show(milk)
        sleep(1000)
        display.show(biberon)
        sleep(1000)
    return milk

# alertes 
def alerting():
    """
    Une des deux fonctions principales. Elle alerte les parents sur l'état
    du bébé. Notamment, l'état d'agitement ou de repos, et la température de la pièce.
    """
    last_message = ""
    while True:
        data = radio.receive()
        packet_type, length, message = unpack_data(data, key)
        distance() #Call the distance function
        if pin_logo.is_touched():
            return False
        #Sending  instructions to the baby be:bi
        if button_a.get_presses():
            send_packet(key, "command", "berceuse")
        elif button_b.get_presses():
            send_packet(key, "command", "alarme")
        #We interpret the message we receive from the baby.
        if message:
            if message == "Agité":
                display.show(Image.SMILE)
                music.play(music.BA_DING, wait=False)
            elif message == "Trés_agité":
                display.show(Image.CONFUSED)
                music.play(music.POWER_DOWN, wait=False)
            elif message == "chaud":
                #We show an image and play music
                display.show(Image("90909:" "09990:" "99999:" "09990:" "90909")) 
                for _ in range(5):
                    music.play(["C6:2", "C6:2", "G5:2", "G5:2"])
                sleep(100)
            elif message == "froid":
                display.show(Image("90909:" "09090:" "90909:" "09090:" "90909"))
                for _ in range(5):
                    music.play(["C6:2", "C6:2", "G5:2", "G5:2"])
                sleep(100)
            elif message == "Endormi":
                display.show("Z")
            else: #Just ignore any other message
                continue
        sleep(100)

# initial secure connection
connexion_status = establish_connexion(key)
if connexion_status == "connected":
    display.show(Image.HEART)#Displays a BIG heart, as opposed to a small heart for the baby
    sleep(500)

# main loop
while True:
    if pin_logo.is_touched(): #Switch to milk mode on pressing 'Home'buttom
        milk = milk_quantity(milk)
    else: #Default to alerting mode
        alerting()
