from microbit import *
import radio
import music

# initial configuration
radio.on()
radio.config(group=99, power=5)
key = "BROOKS"
milk = 0
biberon = Image("19991:" "09090:" "92229:" "09290:" "09290")

# crypt
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

def send_packet(key, type, content):
    """
    Envoie de données fournie en paramètres
    Cette fonction permet de construire, de chiffrer puis d'envoyer un paquet via l'interface radio du micro:bit

    :param (str) key:       Clé de chiffrement
           (str) type:      Type du paquet à envoyer
           (str) content:   Données à envoyer
	:return none
    """
    radio.on()
    radio.config(group=99)
    packet="{} | {} | {}".format(type,len(content),content)
    radio.send(vigenere(packet,key))

def unpack_data(encrypted_packet, key):
    """
    Déballe et déchiffre les paquets reçus via l'interface radio du micro:bit
    Cette fonction renvoie les différents champs du message passé en paramètre.

    :param (str) encrypted_packet: Paquet reçu
           (str) key:              Clé de chiffrement
    :return: (str) type:          Type de paquet
             (int) length:        Longueur de la donnée en caractères
             (str) message:       Données reçues
    """
    try:
        decrypted_packet = vigenere(encrypted_packet, key, decryption=True)
        packet_type, length, value = decrypted_packet.split(" | ")
        if len(value) == int(length):
            return packet_type, int(length), value
        else:
            return None

    except Exception as e:
        print(f"Erreur lors du décryptage ou du traitement du paquet: {e}")
        return None

# challenge 

def calculate_challenge_response(challenge):
    """
    Calcule la réponse au challenge initial de connection avec l'autre micro:bit

    :param (str) challenge:            Challenge reçu
	:return (srt)challenge_response:   Réponse au challenge
    """
    while True:
        challenge = radio.receive()
        if challenge:
            display.scroll("Nu:"+ challenge)
            challenge = int(challenge)
            response = challenge * 2
            display.scroll("R:"+str(response))
            radio.send(str(response))
        
def establish_connexion(key):
    """
    Etablissement de la connexion avec l'autre micro:bit
    Si il y a une erreur, la valeur de retour est vide

    :param (str) key:                  Clé de chiffrement
	:return (srt)challenge_response:   Réponse au challenge
    """
    challenge=str(key)
    send_packet(key, "2" , challenge)
    while True:
         incoming= radio.receive()
         if incoming:
            dencrypted =vigenere(incoming , key , decryption=True)
            if  dencrypted==hashing(challenge):
                 send_packet(key, "2" , "accepted")
                 return "connected"


# milk quantity gestion
def milk_quantity(milk):
    max_milk = 10
    min_milk = 0
    for _ in range(5):
        if button_a.is_pressed() and button_b.is_pressed():
            milk = 0
            send_packet(key, "milk", str(milk))
            display.show(milk)
            sleep(1000)
        elif button_a.get_presses():
            if milk > min_milk:
                milk -= 1
                send_packet(key, "milk", str(milk))
                display.show(milk)
                sleep(1000)
        elif button_b.get_presses():
            if milk < max_milk:
                milk += 1
                send_packet(key, "milk", str(milk))
                display.show(milk)
                sleep(1000)
            else:
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
    last_message = ""
    while True:
        data = radio.receive()
        message = unpack_data(data, key)
        
        if pin_logo.is_touched():
            return False

        if button_a.get_presses():
            send_packet(key, "command", "berceuse")
        elif button_b.get_presses():
            send_packet(key, "command", "alarme")

        if message:
            if message == "Agité" and last_message != "Agité":
                display.show(Image.SMILE)
                music.play(music.BA_DING, wait=False)
                last_message = "Agité"
            elif message == "Trés_agité":
                display.show(Image.CONFUSED)
                music.play(music.POWER_DOWN, wait=False)
                last_message = "Trés_agité"
            elif message == "Endormi":
                display.show("Z")
            elif message == "chaud":
                display.show(Image("90909:" "09990:" "99999:" "09990:" "90909"))
                for _ in range(5):
                    music.play(["C6:2", "C6:2", "G5:2", "G5:2"])
                sleep(100)
            elif message == "froid":
                display.show(Image("90909:" "09090:" "90909:" "09090:" "90909"))
                for _ in range(5):
                    music.play(["C6:2", "C6:2", "G5:2", "G5:2"])
                sleep(100)
            else:
                display.scroll("UNKNOWN")
        sleep(100)

# initial display
display.show(Image.HEART)
sleep(800)

# main loop
while True:
    if pin_logo.is_touched():
        milk = milk_quantity(milk)
    else:
        alerting()
