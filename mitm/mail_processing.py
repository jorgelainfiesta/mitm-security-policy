import requests

sentiment_endpoint = 'https://api.meaningcloud.com/sentiment-2.0'
sentiment_key = '70e1e864590e93d11d72fdc5a5313af0'
mitm_api_endpoint = 'http://mitm-api.herokuapp.com/'
#mitm_api_endpoint = 'http://localhost:8000/'

def sentiment_analysis(text):
    payload = {
        'key': sentiment_key,
        'model': 'auto',
        'txt': text,
        'egp': 'y',
    }
    r = requests.post(sentiment_endpoint, data=payload)
    response = r.json()
    if response['status']['code'] == '0':
        return response['score_tag']
    
def harassive_content(text):
    tags = ['rica', 'puta', 'miamor', 'sexo']
    for tag in tags:
        if tag.lower().strip() in text.lower().split():
            return True
    return False

def racist_content(text):
    tags = ['negro', 'indio', 'cholero', 'chino']
    for tag in tags:
        if tag.lower().strip() in text.lower().split():
            return True
    return False
    
def get_tags(text):
    r = requests.get(mitm_api_endpoint + 'tags/', params={'type': 2})
    response = r.json()
    tags = []
    for tag in [(tag['id'], tag['value']) for tag in response['tags']]:
        if tag[1].lower().strip() in text.lower().split():
            tags.append(tag[0])
    return tags
        
def recipient_is_new(address):
    r = requests.get(mitm_api_endpoint + 'recipients/', params={'address': address})
    return len(r.json()['recipients']) == 0

def recipient_is_not_in_domain(sender, recipient):
    rec_domain = recipient.split('@')[-1]
    sen_domain = sender.split('@')[-1]
    return rec_domain != sen_domain

def process_mail(sender, recipients, subject, body, api_url='http://localhost:8000'):
    """
    sender:     [string] correo de quien envía el correo
    recipients: [string list] lista de correos de los destinatarios del correo
    subject:    [string] asunto del correo
    body:       [string] cuerpo del correo
    return:     None
    Procesa la información del correo y envía los resultados al API definido.
    El método no retorna ningún valor.
    """
    
    mail_tags = []
    
    polarity = sentiment_analysis(body)
    if polarity == "P+":
        mail_tags.append(3)
    elif polarity == "P":
        mail_tags.append(4)
    elif polarity == "NEU":
        mail_tags.append(5)
    elif polarity == "N":
        mail_tags.append(6)
    elif polarity == "N+":
        mail_tags.append(7)
    elif polarity == "NONE":
        mail_tags.append(8)
    
    harassive = harassive_content("%s %s" % (subject, body))
    racist = racist_content("%s %s" % (subject, body))
    if harassive: mail_tags.append(9)
    if racist: mail_tags.append(10)
    
    mail_tags += get_tags("%s %s" % (subject, body))
    
    payload = {
        'mail': {
            'sender': sender,
            'subject': subject,
            'body': body,
            'tags': mail_tags,
        }
    }
    r = requests.post(mitm_api_endpoint + 'mails/', json=payload)
    if r.status_code == 201:
        email_id = r.json()['mail']['id']
    else:
        print(r.json())
        return False
    
    for recipient in recipients:
        r_tags = []
        
        is_new = recipient_is_new(recipient)
        is_out_of_domain = recipient_is_not_in_domain(sender, recipient)
        if is_new: r_tags.append(11)
        if is_out_of_domain: r_tags.append(12)
        
        payload = {
            'recipient': {
                'email': email_id,
                'address': recipient,
                'tags': r_tags,
            }
        }
        r = requests.post(mitm_api_endpoint + 'recipients/', json=payload)
        if r.status_code != 201:
            print(r.json())
            return False
    
    return True

if __name__ == "__main__":
    process_mail(
        'sender@example.com',
        ['recipient1@example.com', 'recipient2@other-example.com'],
        'El Cuervo de Edgar Allan Poe',
        """
Una vez, en una taciturna media noche,
mientras meditaba débil y fatigado,
sobre un curioso y extraño volumen
de sabiduría antigua,
mientras cabeceaba, soñoliento,
de repente algo sonó,
como el rumor de alguien llamando
suavemente a la puerta de mi habitación.
>> Es alguien que viene a visitarme - murmuré
y  llama a la puerta de mi habitación.
Sólo eso, nada más. <<
"""
    )