function submitEssay() {
    var essayQuestion = document.getElementById('essay-question').value.trim();
    if (!essayQuestion) {
        alert('Please enter the essay question.');
        return false;
    }

    // Here you would typically send the question to your server
    // For demonstration, we'll just log to the console and return false to prevent form submission

    console.log('Essay question:', essayQuestion);
    alert('Essay assignment submitted for review.');
    
    // Replace false with your form submission logic
    return false;
}
