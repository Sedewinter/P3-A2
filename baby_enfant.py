from microbit import *
import radio
import music
import urandom

##################
# Initialisation #
##################

radio.on()
radio.config(group=99)
key = "BROOKS"
milk = 0

biberon = Image("19991:""09090:""92229:""09290:""09290")

musique_berceuse = [    
    "G4:4", "A4", "G4", "E4",
    "G4:4", "C5", "B4:8",
    "A4:4", "G4", "F4", "D4",
    "G4:4", "A4", "G4:8",
    "C5:4", "D5", "C5", "B4", 
    "G4:4", "A4", "G4:8" 
]

musique_alarme = [
    "C6:2", "G5:2", "C6:2", "G5:2",
    "F5:2", "A5:2", "F5:2", "A5:2",
    "C6:2", "G5:2", "C6:2", "G5:2",
    "E5:2", "C5:2", "E5:2", "C5:2"
]


###########################
# Crypthography functions #
###########################

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

def send_packet(key, type_packet, content):
    """
    Envoie de données fournie en paramètres
    Cette fonction permet de construire, de chiffrer puis d'envoyer un paquet via l'interface radio du micro:bit

    :param (str) key:       Clé de chiffrement
           (str) type:      Type du paquet à envoyer
           (str) content:   Données à envoyer
	:return none
    """
    content = str(content)
    packet="{} | {} | {}".format(type_packet,len(content),content)
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
            return packet_type, value
        else:
            return None, None

    except Exception:
        return None, None

#######################
# Challenge functions #
#######################

def calculate_challenge(bits=32):
    """
    Calcule un nombre pseudo-aléatoire
    
	:return (int) nombre aléatoire:  challenge à envoyer
	"""
    return urandom.getrandbits(bits)

def expected_hashed_response(challenge):
    """
    Calcule la réponse au challenge initial de connection avec l'autre micro:bit

    :param (str) challenge:            Challenge reçu
	:return (str) challenge_response:   Réponse au challenge
    """
    response=hashing(str(challenge*2))
    return response


def establish_connexion(key):
    """
    Etablissement de la connexion avec l'autre micro:bit
    Si il y a une erreur, la valeur de retour est vide.
    Le be:bi enfant est celui qui initie la connexion,
    càd qu'il envoye le challenge initial.

    :param (str) key:                  Clé de chiffrement
	:return (srt) connexion_status:   Réponse au challenge
    """
    incoming = None
    while True:
        print("yes")
        challenge=calculate_challenge()                              # Choose a random number as the challenge
        while not incoming:
            send_packet(key, "2" , challenge)                        # Send challenge
            print(send_packet(key, "2" , challenge))
            sleep(1000)
            incoming = radio.receive()                               # Listen to communications
        if incoming:                                                 # Listen for challenge answer
            print(incoming)
            packet_type, decrypted = unpack_data(str(incoming), key) #Put the packet value (content) into decrypted
            print(str(decrypted) + " decrypted")
            print(expected_hashed_response(decrypted) + " attendu")
            if decrypted == expected_hashed_response(challenge):
                 send_packet(key, "2" , "accepted")
                 key=challenge
                 return "connected"
            sleep(1000)
        else:
            sleep(500)

#######################
# Main loop functions #
#######################

def signal():
    signal1 = Image("00000:""00000:""00000:""00000:""00000")
    signal2 = Image("00000:""00000:""00600:""00000:""00000")
    signal3 = Image("00000:""00700:""07770:""00700:""00000")
    signal4 = Image("00800:""08980:""89998:""08980:""00800")
    signal5 = Image("00000:""00700:""07770:""00700:""00000")
    signal6 = Image("00000:""00000:""00600:""00000:""00000")
    frames = [signal1, signal2, signal3, signal4, signal5, signal6]
    for frame in frames:
        display.show(frame)
        sleep(350)

def saut_mouton():
    mouton1 = Image("00000:""00000:""00000:""00000:""00807")
    mouton2 = Image("00000:""00000:""00000:""00070:""00800")
    mouton3 = Image("00000:""00000:""00700:""00000:""00800")
    mouton4 = Image("00000:""00000:""00000:""07000:""00800")
    mouton5 = Image("00000:""00000:""00000:""00000:""70800")
    mouton6 = Image("00000:""00000:""00000:""00000:""00800")
    frames = [mouton1, mouton2, mouton3, mouton4, mouton5, mouton6]
    for frame in frames:
        display.show(frame)
        sleep(700)

def berceuse():
    """
    Play a lullaby with the moving image that goes with it for three times.
    """
    for _ in range(3):
        music.play(musique_berceuse, wait=False)
        saut_mouton()
        saut_mouton()
    return None

def alarme():
    """
    Play an alarm with the moving image that goes with it for five times.
    """
    for _ in range(5):
        music.play(musique_alarme, wait=False)
        signal()
        signal()
    return None
    
def distance_baby():
    """
    Send a message so the other micro:bit can verify if they are getting too far
    away from each other.
    """
    radio.send('1')
    sleep(200)
        
def milk_quantity(milk):
    """
    Display the milk quantity drinked by the child.
    
    :param (str) milk:                  milk quantity
    """
    for _ in range(5):
        display.show(milk)
        sleep(1000)
        display.show(biberon)
        sleep(1000)

def movement():
    """
    Main mode. It contains the accelerometer but also the thermometer, proximity, alarm and lullaby.
    """
    last_state = None
    start_immobile = None
    endormi_compt = 30000                                            # Timer for the sleep mode
    state = "Endormi"                                                # Starts as asleep
    while True:
        distance_baby()                                              # Verif if the other micro:bit isn't too far
        tem=temperature()                                            # Mesure the temperature
        data = radio.receive()
        message_type, message = unpack_data(data, key)               # Receive and decrypt the last message             
        
        if pin_logo.is_touched():                                    # If the pin logo is touched, go in the other mode (milk)
            break
            
        if message == "berceuse":                                    # Look if the last message is a the lullaby, alarm or a milk quantity
            berceuse()
        elif message == "alarme":
            alarme()
        elif message_type == "milk":
            return message

        if tem>36:                                                   # If the thermometer is too high or cold, send an alerte to the parent
            send_packet(key, "temp", "chaud")
        elif tem<17:
            send_packet(key, "temp", "froid")
            
        x = accelerometer.get_x()
        y = accelerometer.get_y()
        z = accelerometer.get_z()
        movement_intensite = (x**2 + y**2 + z**2)*0.5                # Calculate the movement of the baby and attribuate each valeur to a state, sent to the parent
         
        if movement_intensite < 1000000:
            if start_immobile is None:
                start_immobile = running_time()
            elif running_time() - start_immobile >= endormi_compt:
                state = "Endormi"
        elif 1000000 <= movement_intensite < 2000000:
            state = "Agité"
            start_immobile = None
        elif movement_intensite >= 2000000 or accelerometer.was_gesture('freefall'):
            state = "Trés_agité"
            start_immobile = None

        if state=="Endormi":
            display.show(Image.SMILE)
        elif state=="Agité":
            display.show(Image.SILLY)
        elif state=="Trés_agité":
            display.show(Image("99999:""99999:""99999:""99999:""99999"))
            
        if last_state != state:
            send_packet(key, "state", state)
            
        last_state = state
        sleep(100)

###############################
# Initial display & challenge #
###############################

connexion_status = establish_connexion(key)
if connexion_status == "connected":                                  # Send a challenge to the other micro:bit and display a heart if the connexion is done right
    display.show(Image.HEART_SMALL)
    sleep(700)
else:
    display.scroll("ERROR")

#############
# Main loop #
#############

while True:                                                          # The loop goes to one mode to an other via the pin logo and register each new milk quantity
    message = radio.receive()
    try:
        if message is not None:
            milk = str(message)
    except TypeError:
        pass
    
    if pin_logo.is_touched():
        milk_quantity(milk)
    else:
        is_it_milk = movement()                                      # Verify if the function ended because the message was a milk quantity: if yes, get registered as the new one
        if is_it_milk != None:
            milk = is_it_milk
            
