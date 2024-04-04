document.addEventListener('DOMContentLoaded', function() {
    initializeConfirmButtonEvents();
    initializeCopyButtonEvents();
    initializeCleanButtonEvents();
    initializeFileUploadEvent();
});

function initializeConfirmButtonEvents() {
    document.querySelectorAll('.confirm-btn').forEach((button, index) => {
        button.addEventListener('click', (event) => {
            event.stopPropagation();

            const successMessage = button.parentNode.querySelector('.success-message');
            if (successMessage) {
                successMessage.style.display = 'inline';
                setTimeout(() => {
                    successMessage.style.display = 'none';
                }, 3000);
            }

            if (index === 0) return;

            const dropdownSection = button.closest('.dropdown-section');
            const visualizationCheckbox = dropdownSection.querySelector(`input[name="visualization${index}"]`);
            const logOutputCheckbox = dropdownSection.querySelector(`input[name="logOutput${index}"]`);

            if (visualizationCheckbox && visualizationCheckbox.checked) {
                const visualizationContent = document.querySelector('#visualizationContent');
                visualizationContent.innerHTML = `<img src="${index}.png" alt="Visualization ${index}">`;
                setTimeout(() => {
                    visualizationContent.querySelector('img').classList.add('show');
                }, 100);
                uncheckAllExcept(visualizationCheckbox, 'visualization');
            }

            if (logOutputCheckbox && logOutputCheckbox.checked) {
                const logContents = [
                    "Content of 1.txt",
                    "Content of 2.txt",
                    "Content of 3.txt",
                    "Content of 4.txt",
                    "Content of 5.txt"
                ];

                const logOutputContent = document.querySelector('#logOutputContent');
                logOutputContent.innerHTML = `<pre>${logContents[index - 1]}</pre>`;
                uncheckAllExcept(logOutputCheckbox, 'logOutput');
            }
        });
    });
}

function uncheckAllExcept(checkbox, name) {
    document.querySelectorAll(`input[name^="${name}"]`).forEach(cb => {
        if (cb !== checkbox) cb.checked = false;
    });
}

function initializeCopyButtonEvents() {
    document.querySelector('#download-visualization-btn').addEventListener('click', (event) => {
        event.preventDefault();
        const visualizationImage = document.querySelector('#visualizationContent img');
        if (visualizationImage) {
            const link = document.createElement('a');
            link.href = visualizationImage.src;
            link.download = `visualization_${visualizationImage.alt}.png`;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        } else {
            alert('No visualization image available for download.');
        }
    });

    document.querySelector('#copy-log-btn').addEventListener('click', () => {
        const logOutput = document.querySelector('#logOutputContent');
        navigator.clipboard.writeText(logOutput.textContent).then(() => {
            console.log('Text copied to clipboard');
        }).catch(err => {
            console.error('Could not copy text: ', err);
        });
    });
}

function initializeCleanButtonEvents() {
    document.querySelectorAll('.clean-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const sectionTitle = btn.closest('.section').querySelector('.section-header').textContent;
            if (sectionTitle === 'Visualization') {
                document.querySelector('#visualizationContent').innerHTML = '';
            } else {
                document.querySelector('#logOutputContent').innerHTML = '';
            }
        });
    });
}

function initializeFileUploadEvent() {
    const fileUpload = document.querySelector('.file-upload');
    const uploadFeedback = document.querySelector('.upload-feedback');
    const confirmButton = document.querySelector('#file-upload-confirm');

    fileUpload.addEventListener('change', () => {
        if (fileUpload.files.length > 0) {
            uploadFeedback.style.display = 'block';
        } else {
            uploadFeedback.style.display = 'none';
        }
    });

    confirmButton.addEventListener('click', () => {
        const successMessage = confirmButton.nextElementSibling;
        successMessage.style.display = 'inline';
        setTimeout(() => {
            successMessage.style.display = 'none';
        }, 3000);
    });
}