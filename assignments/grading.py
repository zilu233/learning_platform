import subprocess

def grade_choice_question(submission):
    if submission.answer.strip() == submission.question.correct_answer.strip():
        submission.result = 'correct'
        submission.score = submission.question.score
    else:
        submission.result = 'wrong'
        submission.score = 0
    submission.save()

def grade_code_question(submission):
    passed_all = True
    total_score = 0
    question = submission.question
    for testcase in question.test_cases.all():
        try:
            result = subprocess.run(
                ['python3', '-c', submission.answer],
                input=testcase.input_data.encode(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=3
            )
            output = result.stdout.decode().strip()
            expected = testcase.expected_output.strip()
            if output == expected:
                total_score += question.score / question.test_cases.count()
            else:
                passed_all = False
        except Exception:
            passed_all = False
    submission.result = 'correct' if passed_all else 'wrong'
    submission.score = total_score
    submission.save()
