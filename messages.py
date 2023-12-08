start_message = "Welcome to the Harry Potter quiz bot. This will evaluate you knowledge of HP universe."
help_message = ("The bot will send you 10 questions, each of which has 4 options, choose the right one. "
                "After completion your score and time will be displayed. To start the quiz just send "
                "/start_quiz command.")


def get_end_msg(score, questions, time):
    return f"Quiz completed!\nYour score: {score}/{questions}\nTime taken: {time} seconds"


def get_record_table(sorted_users):
    output_message = ""
    for user_id, (correct_answers_num, time_) in sorted_users:
        output_message += f"User ID: {user_id}\nCorrect Answers: {correct_answers_num}\nTime: {time_} seconds\n\n"
    return output_message
