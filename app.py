from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options


servico = Service(ChromeDriverManager().install())
chrome_options = Options()
chrome_options.add_argument("--mute-audio")
navegador = webdriver.Chrome(service=servico, options=chrome_options)

navegador.get("https://adm.fullarm.com/monitoramento#!/ocorrencias")

navegador.find_element(
    'xpath', '//*[@id="username"]').send_keys("alexsandro.luiz")
navegador.find_element('xpath', '//*[@id="password"]').send_keys("123456")
navegador.find_element('xpath', '//*[@id="btn_login"]').click()


permissao_lista = ['Armado', 'Desarmado', 'Teste Periódico', 'Restauração Falha de Keep alive', 'Restauração - Bateria principal baixa', 'Problema para comunicar evento', 'Armado fora de horário',
                   'Setor "ZONA 04 CAM 06 " desconectado', 'Falha de comunicação com o sensor', 'Restauração Bateria baixa do sensor sem fio ZONA 06 CORREDOR B G1', 'Reset da central', 'Problema sirene principal', 'Setor "ZONA 03 CAM 05" desconectado', 'Bateria principal ausente', 'Bateria principal baixa', 'Desarmado fora do horário', 'Desarmar', 'Bateria baixa do sensor sem fio ZONA 02 DOCAS', 'Bateria baixa do sensor sem fio ZONA 13 ESTOQUE', 'Restauração Falha de supervisão do sensor ZONA 01 ALMOXARIFADO 04', 'Setor inibido', 'Setor inibido Sala Cofre', 'Setor inibido 41', 'Restauração Bateria baixa do sensor sem fio 11', 'Restauração Bateria baixa do sensor sem fio ZONA 16 CORREDOR ESCRITORIO', 'Falha de supervisão do sensor ZONA 05 MONTAGEM 1', 'Bateria do sistema Baixa', 'Restauração Falha de corrente alternada na PGM 403', 'Bateria baixa do sensor sem fio ZONA 16 CORREDOR ESCRITORIO', 'Arme']
negacao_lista = ['Alarme de Furto', 'Não Desarmado',
                 'Bateria ausente', 'Falha de Keep a Live', 'Não Armado', 'Tamper do módulo de expansão']

ocorrencias_afinalizar = []
div_ocorrencia_item = WebDriverWait(navegador, 20).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "div.ocorrencia-item"))
)
div_ocorrencia_item = navegador.find_elements(
    By.CSS_SELECTOR, "div.ocorrencia-item")

for ocorrencia in div_ocorrencia_item:
    titulo = ocorrencia.find_element(
        By.CSS_SELECTOR, "p.evento_maior_prioridade_titulo").text
    if any(palavra_permitida.upper() in titulo.upper() for palavra_permitida in permissao_lista) and not any(palavra_negada.upper() in titulo.upper() for palavra_negada in negacao_lista):
        # if True:
        id_ocorrencia = ocorrencia.find_element(
            By.CSS_SELECTOR, "span.ng-binding").get_attribute("id")
        ocorrencias_afinalizar.append(id_ocorrencia)
for ocorrencia_afinalizar in ocorrencias_afinalizar:
    aguardando_atendimento = '//*[@id="status_ocorrencia_container"]/div[1]'
    aguardando_atendimento = WebDriverWait(navegador, 20).until(
        EC.element_to_be_clickable((By.XPATH, aguardando_atendimento))
    )

    aguardando_atendimento.click()

    ocorrencia = WebDriverWait(navegador, 20).until(
        EC.element_to_be_clickable((By.ID, ocorrencia_afinalizar))
    )
    navegador.execute_script("arguments[0].scrollIntoView(true);", ocorrencia)

    navegador.find_element(By.ID, ocorrencia_afinalizar).click()

    historico_eventos_xpath = '//*[@id="tab_historico"]/a'
    historico_eventos = WebDriverWait(navegador, 20).until(
        EC.element_to_be_clickable((By.XPATH, historico_eventos_xpath))
    )

    historico_eventos.click()

    primeira_ocorrencia_css = '#tableHistoricoResponsive tr:nth-of-type(2)'
    primeira_ocorrencia = WebDriverWait(navegador, 20).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, primeira_ocorrencia_css))
    )
    data_hora = primeira_ocorrencia.find_elements(By.TAG_NAME, "td")[4].text
    descricao = primeira_ocorrencia.find_elements(By.TAG_NAME, "td")[3].text
    texto_primeira_ocorrencia = f"{descricao} {data_hora}"

    gerar_comentario_css = 'div.occurrence-comment-container textarea'
    gerar_comentario = WebDriverWait(navegador, 30).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, gerar_comentario_css))
    )

    gerar_comentario.click()
    gerar_comentario.send_keys(texto_primeira_ocorrencia)

    botao_gerar_comentario_css = 'div.button-and-contact-message-container button:nth-of-type(1)'
    botao_gerar_comentario = WebDriverWait(navegador, 30).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, botao_gerar_comentario_css))
    )

    botao_gerar_comentario.click()

    finalizar_ocorrencia_css = 'div.observe-or-close-the-occurrence button:nth-of-type(2)'
    finalizar_ocorrencia = WebDriverWait(navegador, 30).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, finalizar_ocorrencia_css))
    )

    finalizar_ocorrencia.click()

    finalizar_ocorrencia_novamente_id = 'btnFinalizarMotivoAlarme'
    finalizar_ocorrencia_novamente = WebDriverWait(navegador, 30).until(
        EC.visibility_of_element_located(
            (By.ID, finalizar_ocorrencia_novamente_id))
    )

    finalizar_ocorrencia_novamente.click()


# notificacao_ocorrencia = '//*[@id="66c2aed52f2df84ce183747e"]/div/div/div'
# notificacao = WebDriverWait(navegador, 20).until(
#     EC.presence_of_element_located((By.XPATH, notificacao_ocorrencia)))
# notificacao.click()

# historico_eventos_xpath = '//*[@id="tab_historico"]/a'
# historico_eventos = WebDriverWait(navegador, 20).until(
#     EC.visibility_of_element_located((By.XPATH, historico_eventos_xpath))
# )
# historico_eventos.click()

# primeira_ocorrencia_xpath = '//*[@id="tableHistoricoResponsive"]/table/tbody/tr[2]'
# primeira_ocorrencia = WebDriverWait(navegador, 20).until(
#     EC.visibility_of_element_located((By.XPATH, primeira_ocorrencia_xpath))
# )
# texto_primeira_ocorrencia = primeira_ocorrencia.get_attribute(
#     "textContent").strip()

# campo_comentario = '/html/body/main/div/div[2]/div[6]/div[1]/div/div[2]/textarea'
# campo_comentario = WebDriverWait(navegador, 30).until(
#     EC.visibility_of_element_located((By.XPATH, campo_comentario))
# )
# campo_comentario.click()
# campo_comentario.send_keys(texto_primeira_ocorrencia)

# gerar_comentario = '/html/body/main/div/div[2]/div[6]/div[1]/div/div[4]/button/span'
# gerar_comentario = WebDriverWait(navegador, 30).until(
#     EC.visibility_of_element_located((By.XPATH, gerar_comentario))
# )
# gerar_comentario.click()
# time.sleep(5)

# finalizar_ocorrencia = '/html/body/main/div/div[2]/div[7]/div/div/div[2]/button[2]'
# finalizar_ocorrencia = WebDriverWait(navegador, 30).until(
#     EC.visibility_of_element_located((By.XPATH, finalizar_ocorrencia))
# )
# finalizar_ocorrencia.click()
# time.sleep(5)

# finalizar_ocorrencia_novamente = 'btnFinalizarMotivoAlarme'
# finalizar_ocorrencia_novamente = WebDriverWait(navegador, 30).until(
#     EC.visibility_of_element_located(
#         (By.XPATH, finalizar_ocorrencia_novamente))
# )
# finalizar_ocorrencia_novamente.click()
# time.sleep(5)


# aguardando_atendimento = '//*[@id="status_ocorrencia_container"]/div[1]'
# aguardando_atendimento = WebDriverWait(navegador, 20).until(
#     EC.visibility_of_element_located((By.XPATH, aguardando_atendimento))
# )
# aguardando_atendimento.click()
# time.sleep(5)
#
