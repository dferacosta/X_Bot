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

# Nombre de usuario de la cuenta objetivo (reemplaza 'objetivo_usuario' con la cuenta que deseas monitorear)
usuario_objetivo = "objetivo_usuario"

# Función para simplificar el texto usando la API de OpenAI
def simplificar_texto(texto):
    respuesta = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Reescribe este texto con términos más simples: {texto}",
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return respuesta.choices[0].text.strip()

# Guardamos el ID del último tweet procesado para evitar duplicados
ultimo_tweet_id = None

while True:
    # Obtenemos los últimos tweets del usuario
    tweets = api.user_timeline(screen_name=usuario_objetivo, since_id=ultimo_tweet_id, tweet_mode="extended")
    
    for tweet in reversed(tweets):
        # Nos aseguramos de que el tweet solo contenga texto (sin imágenes o links)
        if not tweet.entities.get("media") and 'http' not in tweet.full_text:
            texto_simplificado = simplificar_texto(tweet.full_text)
            
            # Publicamos el tweet simplificado
            api.update_status(f"Simplificado: {texto_simplificado}")
            print(f"Publicado: {texto_simplificado}")
            
            # Actualizamos el ID del último tweet procesado
            ultimo_tweet_id = tweet.id
    
    # Esperamos antes de verificar nuevamente (por ejemplo, 60 segundos)
    time.sleep(60)