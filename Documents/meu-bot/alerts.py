import praw
import re
import requests
import time
from colorama import Fore, Style, init
import prawcore

# Inicializar o Colorama para cores no Windows
init()

# Configuração do Reddit
reddit = praw.Reddit(
    client_id='OBCKMXQ5HYcLNBgfFfuedw',
    client_secret='qek7LU5cE9PE7s3f6MDzGI7UhPCsTQ',
    username='fernando1648',
    password='9qybc.Gf4*YX5Ki',
    user_agent='my_reddit_bot_v1.0 (by /fernando1648)'
)

# Subreddits a serem monitorados
subreddit = reddit.subreddit('HungryArtists+artcommissions+ArtSale+commissions+comissions+dndcommissions')

# Palavra-chave que queremos monitorar
keyword = 'hiring'

# Lista para evitar duplicatas
notified_posts = set()

# URL do webhook do Discord
webhook_url = 'https://discord.com/api/webhooks/1283091379626577970/7da7Pjuf1EUbAfq1Yb5RHq623mi1OcNg-tTdxdWL6lwSSUCf3syvyrULx_HRlNfB_4SK'

# Função para verificar se a palavra exata está presente
def contains_exact_word(text, word):
    # Usando \b para garantir que seja a palavra exata
    pattern = r'\b' + re.escape(word) + r'\b'
    return re.search(pattern, text, re.IGNORECASE) is not None

# Função para enviar mensagem ao Discord
def send_to_discord(title, url):
    data = {
        "content": f"📢 **Nova postagem encontrada!**\n**Título:** {title}\n🔗 [Link para a postagem]({url})"
    }
    try:
        response = requests.post(webhook_url, json=data)
        if response.status_code == 204:
            print(f"{Fore.GREEN}Mensagem enviada ao Discord com sucesso!{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Falha ao enviar mensagem ao Discord, status code: {response.status_code}{Style.RESET_ALL}")
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}Erro ao enviar mensagem ao Discord: {e}{Style.RESET_ALL}")

# Loop infinito para verificar continuamente
while True:
    try:
        for post in subreddit.new(limit=10):
            if post.id not in notified_posts:
                if contains_exact_word(post.title, keyword) or contains_exact_word(post.selftext, keyword):
                    post_url = f"https://www.reddit.com{post.permalink}"

                    # Exibe no console
                    print(f"{Fore.YELLOW}Nova postagem encontrada! Título: {post.title}{Style.RESET_ALL}")
                    print(f"{Fore.BLUE}Link: {post_url}{Style.RESET_ALL}")

                    # Enviar mensagem para o Discord
                    send_to_discord(post.title, post_url)

                    # Evita notificações duplicadas
                    notified_posts.add(post.id)

        # Aguarde 2 minutos antes de verificar novamente para evitar limites de requisição
        time.sleep(120)
    except prawcore.exceptions.TooManyRequests as e:
        print(f"{Fore.RED}Limite de requisições excedido. Aguardando {e.sleep_time} segundos...{Style.RESET_ALL}")
        time.sleep(e.sleep_time)  # Espera o tempo recomendado pela API
    except prawcore.exceptions.RequestException as e:
        print(f"{Fore.RED}Erro de conexão com o Reddit: {e}{Style.RESET_ALL}")
        time.sleep(60)  # Espera um minuto antes de tentar novamente
    except Exception as e:
        print(f"{Fore.RED}Erro inesperado: {e}{Style.RESET_ALL}")
        time.sleep(60)  # Espera um minuto antes de tentar novamente




