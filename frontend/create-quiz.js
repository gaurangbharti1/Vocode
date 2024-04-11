document.getElementById('add-question').addEventListener('click', addQuestion);

function addQuestion() {
    var questionNumber = document.querySelectorAll('.quiz-question').length + 1;
    var newQuestionDiv = document.createElement('div');
    newQuestionDiv.classList.add('quiz-question');
    newQuestionDiv.setAttribute('data-question-number', questionNumber);

    var label = document.createElement('label');
    label.innerHTML = 'Question ' + questionNumber + ':';
    label.setAttribute('for', 'question-' + questionNumber);

    var input = document.createElement('input');
    input.type = 'text';
    input.id = 'question-' + questionNumber;
    input.name = 'question-' + questionNumber;
    input.required = true;
    input.placeholder = 'Enter question text';

    var mcqOptionsDiv = document.createElement('div');
    mcqOptionsDiv.classList.add('mcq-options');
    mcqOptionsDiv.id = 'mcq-options-' + questionNumber;

    var addChoiceButton = document.createElement('button');
    addChoiceButton.type = 'button';
    addChoiceButton.classList.add('add-choice');
    addChoiceButton.innerHTML = 'Add Choice';
    addChoiceButton.onclick = function() { addChoice(questionNumber); };

    newQuestionDiv.appendChild(label);
    newQuestionDiv.appendChild(input);
    newQuestionDiv.appendChild(mcqOptionsDiv);
    newQuestionDiv.appendChild(addChoiceButton);

    document.getElementById('additional-questions').appendChild(newQuestionDiv);
}

function addChoice(questionNumber) {
    var mcqOptionsDiv = document.getElementById('mcq-options-' + questionNumber);
    var choice
