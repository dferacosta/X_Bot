import tweepy
import openai
import time

# Configura tus credenciales de Twitter
twitter_api_key = "TU_API_KEY"
twitter_api_secret = "TU_API_SECRET"
twitter_access_token = "TU_ACCESS_TOKEN"
twitter_access_secret = "TU_ACCESS_SECRET"

# Configura tu API Key de OpenAI
openai.api_key = "TU_OPENAI_API_KEY"

# Autenticación en Twitter
auth = tweepy.OAuthHandler(twitter_api_key, twitter_api_secret)
auth.set_access_token(twitter_access_token, twitter_access_secret)
api = tweepy.API(auth)

# Lista de cuentas a monitorear
usuarios_objetivo = [
    "daily_cripto",
    "Dionysus_crypto",
    "SCryptowhale",
    "its_airdrop",
    "AlphaInsiders",
    "Airdrop_Adv",
    "bitcoinmagazine"
]

# Función para traducir y simplificar el texto usando la API de OpenAI
def traducir_y_simplificar_texto(texto):
    # Primero traducimos el texto al inglés
    traduccion = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Traduce este texto al inglés: {texto}",
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7,
    )
    texto_en_ingles = traduccion.choices[0].text.strip()
    
    # Luego simplificamos el texto traducido
    simplificacion = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Reescribe este texto en inglés con términos más simples: {texto_en_ingles}",
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7,
    )
    texto_simplificado = simplificacion.choices[0].text.strip()

    # Aseguramos que el texto no exceda los 250 caracteres
    return texto_simplificado[:250]

# Guardamos el ID del último tweet procesado para evitar duplicados
ultimo_tweet_id = None

while True:
    for usuario_objetivo in usuarios_objetivo:
        # Obtenemos los últimos tweets del usuario
        tweets = api.user_timeline(screen_name=usuario_objetivo, since_id=ultimo_tweet_id, tweet_mode="extended")
        
        for tweet in reversed(tweets):
            # Nos aseguramos de que el tweet solo contenga texto (sin imágenes o links)
            if not tweet.entities.get("media") and 'http' not in tweet.full_text:
                # Traducir y simplificar el texto del tweet
                texto_simplificado = traducir_y_simplificar_texto(tweet.full_text)
                
                # Publicamos el tweet simplificado
                api.update_status(f"Simplified: {texto_simplificado}")
                print(f"Posted: {texto_simplificado}")
                
                # Actualizamos el ID del último tweet procesado
                ultimo_tweet_id = tweet.id
    
    # Esperamos antes de verificar nuevamente (por ejemplo, 60 segundos)
    time.sleep(60)
