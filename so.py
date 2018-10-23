#! python

from stackapi import StackAPI
import sys


def get_top_question(N, tag):
    SITE = StackAPI('stackoverflow')
    SITE.max_pages = 1 + (N // 100)
    SITE.page_size = int(N/SITE.max_pages)

    data = SITE.fetch('questions', tagged=tag, sort='votes')
    questions = data['items']

    result = ''

    for question in questions:
        question_id = question['question_id']

        answers = SITE.fetch('questions/{}/answers'.
                             format(question_id), sort='votes')
        answer_id = answers['items'][0]['answer_id']
        top_answer_link = 'https://stackoverflow.com/a/{}'.format(answer_id)

        result += 'Title: {}\nThe highest voted answer link: {}\n\n'.\
            format(question['title'], top_answer_link)

    return result


def main():
    try:
        N, tag = int(sys.argv[1]), sys.argv[2]
        result = get_top_question(N, tag)
        if not result:
            print('There is no question with tag {}'.format(tag))
        else:
            return result
        print(result)
    except IndexError as e:
        print(e)


if __name__ == '__main__':
    main()
