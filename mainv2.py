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
        q = {"other_options":[]}

        while data_list[curr_index] != question:
            curr_index += 1
        
        # Find Question Location
        curr_index += 1
        Q_START = curr_index
        while data_list[curr_index] != 'A':
            curr_index += 1
        Q_END = curr_index

        # Join Question and put into list
        q["question"] = '\n'.join(data_list[Q_START:Q_END])
        
        # Find options
        current_answer = ord('A')

        # Loop until it is next question
        while ANSWER_TEXT != data_list[curr_index] and not(data_list[curr_index] == str(int(question[:-1]) + 1) + '.'):
            if data_list[curr_index] == chr(current_answer):
                q["other_options"].append("")
                current_answer += 1
            else:
                # # Append the current
                # isNextQuestion = (data_list[curr_index + 1] == str(int(question[:-1]) + 1) + '.')
                # isNextOption = (data_list[curr_index + 1] == chr(current_answer))
                
                # if (q["other_options"][current_answer - ord('A') - 1] == ""):
                #     q["other_options"][current_answer - ord('A') - 1] = f"{data_list[curr_index]}"
                # elif data_list[curr_index] == "" and (isNextQuestion or isNextOption):
                #     pass
                # else:
                #     q["other_options"][current_answer - ord('A') - 1] += f"\n{data_list[curr_index]}"

                
                # Append the current
                q["other_options"][current_answer - ord('A') - 1] += f"{data_list[curr_index]}\n"
            curr_index += 1

        q["question"] = q["question"].rstrip("\n")
        for index, item in enumerate(q["other_options"]):
            q["other_options"][index] = item.rstrip("\n")

        # Pop the answer from other_options and add to answer
        q["answer"] = q["other_options"].pop(ord(answers[question]) - ord('a'))

        q["feedback"] = [""]
        q["weight"] = 1000
        q["tag"] = ["中文", "卷一", "New"]
        output.append(q)
    
    out_text = json.dumps(output, ensure_ascii=False)


    print(out_text)
    pyperclip.copy(out_text)
        
