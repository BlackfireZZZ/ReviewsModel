from typing import List, Dict

from flask import request, jsonify, send_file
from application import app
from application import llm
from google_maps import get_info
from ranked_model import model


@app.route('/ping', methods=['GET'])
def response_ping():
    return jsonify({"status": "ok"}), 200


@app.route('/apply', methods=['POST'])
def create_description() -> str:
    data = request.json
    hotel_services = []
    if 'hotel_services' in data:
        hotel_services = data['hotel_services']
    hotel_name = data['hotel_name']
    useful_info = model()
    address = data['address']
    count_rooms = data['count_rooms']
    style = data['style']
    geo_data = get_info(address)
    comment = data['comment']
    prompt = f'''
             Твоя единственная задача — создавать описания отелей на основе предоставленных данных. Описания должны быть привлекательными, информативными и структурированными. Избегай лишней информации и не отклоняйся от темы.:
             'Название отеля': {hotel_name},
             'Дополнительная информация об отеле': {useful_info},
             'Гео-данные': {geo_data},
             'Сервисы отеля': {hotel_services if hotel_services else "Нет информации о сервисах"}
             '''

    answer = llm.create_chat_completion(
        messages=[
            {"role": "system", "content": "You are an assistant who perfectly describes hotels."},
            {"role": "user", "content": prompt}])

    return answer['choices'][0]['message']['content']


@app.route('/correct', methods=['POST'])
def correct_description() -> str:
    data = request.json
    context: List[Dict] = data['context']
    comment = data['comment']
    '''
    Функция для корректировки описания отеля на основе контекста
    Данные:
    llm - модель
    context - текст, который нужно откорректировать
    '''
    last_user_message = context[-1]
    last_bot_message = context[-2]
    prompt = f'''
             Возьми описание и измени его, операясь на комментарий пользователя
             Контекст: {context}
             '''

    answer = llm.create_chat_completion(
        messages=[
            {"role": "system", "content": "You are an assistant who perfectly describes hotels."},
            {"role": "user", "content": prompt}])

    return answer['choices'][0]['message']['content']
