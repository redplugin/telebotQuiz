# Student: Darmen Tuyakayev
# Course: Python developer 14
# Homework: Telebot quiz project

import telebot
import time
import os
from dotenv import load_dotenv
from quiz_data import quiz_questions
from messages import *

load_dotenv()
API_TOKEN = os.environ.get('API_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

# Dictionary to store user responses like this: {57748352: ['Answer 1', 'Answer 2', 'Answer 3', etc.]}
user_responses = {}

# Dictionary to store user's results like this: {57748352: (correct_answers_num, time)}
users_chart = {}

start_time = {}


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, start_message)


@bot.message_handler(commands=['help'])
def get_help(message):
    bot.send_message(message.chat.id, help_message)


@bot.message_handler(commands=['record_table'])
def show_record_table(message):
    # sort the users_chart dict so those who have most correct answers showed first and if there are several people
    # with equal score, those who finished fasted are shown first.
    sorted_users = sorted(users_chart.items(), key=lambda x: (-x[1][0], x[1][1]))

    bot.send_message(message.chat.id, get_record_table(sorted_users))


@bot.message_handler(commands=['start_quiz'])
def start_quiz(message):
    user_id = message.chat.id
    user_responses[user_id] = []
    start_time[user_id] = time.time()
    send_question(user_id)


def send_question(user_id):
    current_question_number = len(user_responses[user_id])
    if current_question_number < len(quiz_questions):
        question = quiz_questions[current_question_number]["question"]
        options = quiz_questions[current_question_number]["options"]

        markup = telebot.types.InlineKeyboardMarkup()
        for option in options:
            button = telebot.types.InlineKeyboardButton(text=option, callback_data=option)
            markup.add(button)

        bot.send_message(user_id, f"Question {current_question_number + 1}: {question}", reply_markup=markup)
    else:
        end_quiz(user_id)


def end_quiz(user_id):
    end_time = time.time()
    elapsed_time = round(end_time - start_time[user_id], 2)  # calculate how much it took to finish the quiz
    score = calculate_score(user_id)

    # save user's score and time to the table
    users_chart[user_id] = (score, elapsed_time)

    bot.send_message(user_id, get_end_msg(score, len(quiz_questions), elapsed_time))


def calculate_score(user_id):
    score = 0
    for id_, response in enumerate(user_responses[user_id]):
        if response == quiz_questions[id_]["correct_option"]:
            score += 1
    return score


@bot.callback_query_handler(func=lambda call: True)
def handle_answer(call):
    user_id = call.message.chat.id
    user_responses[user_id].append(call.data)
    send_question(user_id)


bot.polling()
