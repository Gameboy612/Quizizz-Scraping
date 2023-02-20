import pyperclip as pyperclip
import json

def getAnswer(answer_data):
    answers = {}
    for index, item in enumerate(answer_data):
        if item[:-1].isnumeric() and index + 1 != len(answer_data) and not answer_data[index + 1][:-1].isnumeric():
            answers[item] = answer_data[index + 1]
    return answers

with open('input.txt', 'r', encoding='utf-8') as file:
    # * Note! This ANSWER_TEXT component is dependent on your quizizz language
    ANSWER_TEXT = "解答"
    
    data = file.read()


    # Obtain the answer data
    answer_data = data[data.rfind(ANSWER_TEXT):].split("\n")[1:]
    answers = getAnswer(answer_data)

    data_list = data.split('\n')
    curr_index = 0
    output = []
    for question in list(answers.keys()):
        q = {}
        while data_list[curr_index] != question:
            curr_index += 1
        q["question"] = data_list[curr_index + 1]
        
        q["other_options"] = [data_list[curr_index + 4], data_list[curr_index + 7], data_list[curr_index + 10], data_list[curr_index + 13]]
        if answers[question] == 'a':
            q["other_options"].remove(data_list[curr_index + 4])
            q["answer"] = [data_list[curr_index + 4]]
        if answers[question] == 'b':
            q["other_options"].remove(data_list[curr_index + 7])
            q["answer"] = [data_list[curr_index + 7]]
        if answers[question] == 'c':
            q["other_options"].remove(data_list[curr_index + 10])
            q["answer"] = [data_list[curr_index + 10]]
        if answers[question] == 'd':
            q["other_options"].remove(data_list[curr_index + 13])
            q["answer"] = [data_list[curr_index + 13]]
        q["feedback"] = [""]
        q["weight"] = 1000
        q["tag"] = ["中文", "卷一", ""]
        output.append(q)
    
    print(json.dumps(output, ensure_ascii=False))
    pyperclip.copy(json.dumps(output, ensure_ascii=False))
        
