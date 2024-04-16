from flask import Flask, render_template, request
import openpyxl
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import urllib.parse

app = Flask(__name__, static_folder='static', template_folder='templates')


@app.route('/', methods=['GET', 'POST'])
def index():
    message = None
    if request.method == 'POST':
        file = request.files['file']
        workbook = openpyxl.load_workbook(file)
        pagina_cliente = workbook['folha']

        chrome_options = webdriver.ChromeOptions()

        chrome_options.add_argument(
            'user-data-dir=/home/nb/.config/google-chrome/Default/WP')
        navegador = webdriver.Chrome(options=chrome_options)

        for linha in pagina_cliente.iter_rows(min_row=2):
            nome = linha[0].value
            movel = linha[1].value
            data = linha[2].value
            valor = linha[3].value

            texto = f'Olá {nome} seu pagamento vence no dia {data.strftime("%d/%m/%Y")}. Favor faça o pagamento dos {valor}€'
            texto = urllib.parse.quote(texto)

            link = f'https://web.whatsapp.com/send?phone={movel}&text={texto}'
            navegador.get(link)

            while len(navegador.find_elements(By.ID, 'side')) < 1:
                sleep(2)
            sleep(4)

            navegador.find_element(
                By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span').click()
            sleep(5)

        navegador.quit()

        message = 'Mensagens enviadas com sucesso!'

    return render_template('index.html', message=message)


if __name__ == '__main__':
    app.run(debug=True)
