document.addEventListener('DOMContentLoaded', function() {
    // Submit button
    let submit = document.getElementById('submit');

    submit.addEventListener('click', function() {
        let ans1 = document.querySelector('input[name="q1Radio"]:checked');
        let ans2 = document.querySelector('input[name="q2Btn"]:checked');
        let ans3 = document.querySelector('#q3 input');
        let ans4 = document.querySelector('#q4 input');

        let errorMessage = '';

        if (!ans1) {
            errorMessage += 'Answer for question 1 is missing.\n';
        }

        if (!ans2) {
            errorMessage += 'Answer for question 2 is missing.\n';
        }

        if (ans3.value.trim() === '') {
            errorMessage += 'Answer for question 3 is missing.\n';
        }

        if (ans4.value.trim() === '') {
            errorMessage += 'Answer for question 4 is missing.\n';
        }

        if (errorMessage !== '') {
            alert(errorMessage);
            return;
        }

        let counter = 0;

        if (ans1.id === 'opt4') {
            counter++;
        }

        if (ans2.id === '2opt3') {
            counter++;
        }

        if (ans3.value.trim().toLowerCase() === 'whale shark') {
            counter++;
        }

        if (ans4.value.trim().toLowerCase() === 'giraffe') {
            counter++;
        }

        alert('You have ' + counter + ' of 4 answers correct.');
    });
});