import pyperclip as pyperclip
import json

def getAnswer(answer_data):
    answers = {}
    for index, item in enumerate(answer_data):
        if item[:-1].isnumeric() and index + 1 != len(answer_data) and not answer_data[index + 1][:-1].isnumeric():
            answers[item] = answer_data[index + 1]
    return answers

with open('input.txt', 'r', encoding='utf-8') as file:
    data = file.read()

    def FindAnswerText(raw):
        search = raw.split("\n")
        search.reverse()

        def isAnswer(sus):
            if len(sus) > 1:
                return False
            ascii = ord(sus) - ord('a')

            # Quizizz can only have up to 5 answers
            return 0 <= ascii <= 4

        def isQuestionID(sus):
            if sus[-1] != '.':
                return False
            return sus[:-1].isnumeric()

        for item in search:
            if not(isAnswer(item) or isQuestionID(item)):
                return item
        raise Exception("Sorry, no answer_text is found.")
    
    # * Note! This ANSWER_TEXT component is dependent on your quizizz language
    ANSWER_TEXT = FindAnswerText(data)

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
        q["tag"] = ["??????", "??????", "New"]
        output.append(q)
    
    out_text = json.dumps(output, ensure_ascii=False)

    out_text = out_text.replace("\\\\n", "\\n")

    print(out_text)
    pyperclip.copy(out_text)
        
