import os
import requests
from bs4 import BeautifulSoup

def get_html(url):
    response=None
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("HTML recuperato correttamente")
            return response.text
        else:
            print(f"Errore {response.status_code} durante il recupero della pagina")
            return None
    except Exception as e:
        print(f"Si è verificato un errore: {e}")
        return None
    
def estrai_prezzo(riga_elab):
    contenuto_html = get_html(url=riga_elab)
    
    if contenuto_html is None:
        return "Errore nel recupero del contenuto HTML"
    
    try:
        soup = BeautifulSoup(contenuto_html, 'html.parser')
        
        # Cerca il div con la classe specificata (cambiare il div a seconda della pagina da analizzare es sotto è il prezzo di amazon)
        div_out = soup.find('div', class_='a-section a-spacing-none aok-align-center aok-relative')
        
        if div_out is None:
            # Salva il contenuto HTML nel file brokenXXX.txt
            html_file = f"brokenHTML/nodiv{len(os.listdir('brokenHTML'))}.txt"
            os.makedirs(os.path.dirname(html_file), exist_ok=True)
            with open(html_file, "w") as file:
                file.write(riga_elab)
            return f"Errore: Div con la classe specificata non trovato. HTML salvato in {html_file}"
        
        # Cerca lo span all'interno del div trovato
        tag_out = div_out.find('span', class_='a-price-whole')
        
        if tag_out is None:
            html_file = f"brokenHTML/nulldiv{len(os.listdir('brokenHTML'))}.txt"
            os.makedirs(os.path.dirname(html_file), exist_ok=True)
            with open(html_file, "w") as file:
                file.write(contenuto_html)
            return "Errore contenuto trovato all'interno del div"
        
        # Estrai il testo dal tag span e restituisci il prezzo
        extracted_text = tag_out.text.strip()
        print(extracted_text)
        
        return extracted_text
    except Exception as e:
        return "Errore durante l'estrazione : {}".format(e)
    
estrai_prezzo("inserisci qui la pagina HTML")