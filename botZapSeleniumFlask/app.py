from flask import Flask, render_template, request, redirect, url_for
import openpyxl
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import urllib.parse

app = Flask(__name__, static_folder='static', template_folder='templates')


def send_message_to_number(number, message):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(
        'user-data-dir=/home/nb/.config/google-chrome/Default/WP')
    driver = webdriver.Chrome(options=chrome_options)

    texto = urllib.parse.quote(message)
    link = f'https://web.whatsapp.com/send?phone={number}&text={texto}'
    driver.get(link)

    while len(driver.find_elements(By.ID, 'side')) < 1:
        sleep(2)
    sleep(4)

    driver.find_element(
        By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span').click()
    sleep(5)

    driver.quit()


@app.route('/', methods=['GET', 'POST'])
def index():
    message = None
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            workbook = openpyxl.load_workbook(file)
            customer_page = workbook['folha']

            for row in customer_page.iter_rows(min_row=2):
                name = row[0].value
                movel = row[1].value
                date = row[2].value
                price = row[3].value

                text = f'Olá {name} seu pagamento vence no dia {date.strftime("%d/%m/%Y")}. Favor faça o pagamento dos {price}€'
                send_message_to_number(movel, text)

            message = 'Mensagens enviadas com sucesso!'

        elif 'number' in request.form and 'custom_message' in request.form:
            number = request.form['number']
            custom_message = request.form['custom_message']
            send_message_to_number(number, custom_message)
            message = f'Mensagem enviada com sucesso para {number}!'

    return render_template('index.html', message=message)


if __name__ == '__main__':
    app.run()
