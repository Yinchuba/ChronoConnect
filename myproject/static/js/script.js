document.addEventListener('DOMContentLoaded', function() {
    initializeConfirmButtonEvents();
    initializeCopyButtonEvents();
    initializeCleanButtonEvents();
    initializeAddFileButtonEvent();
});

function initializeConfirmButtonEvents() {
    document.querySelectorAll('.confirm-btn').forEach(button => {
        button.addEventListener('click', () => {
            const successMessage = button.parentNode.nextElementSibling;
            successMessage.textContent = "Success";
            successMessage.style.display = "inline";

            setTimeout(() => {
                successMessage.style.display = "none";
            }, 3000);

            const dropdownSection = button.closest('.dropdown-section');
            const visualizationCheckbox = dropdownSection.querySelector('input[name^="visualization"]');
            const logOutputCheckbox = dropdownSection.querySelector('input[name^="logOutput"]');

            if (visualizationCheckbox && visualizationCheckbox.checked) {
                const visualizationNumber = visualizationCheckbox.name.slice(-1);
                const visualizationContent = document.querySelector('#visualizationContent');
                // TODO: Update the image source URL based on the server-generated URL
                visualizationContent.innerHTML = `<img src="path/to/image/${visualizationNumber}.jpg" alt="Visualization ${visualizationNumber}">`;
            }

            if (logOutputCheckbox && logOutputCheckbox.checked) {
                const logOutputNumber = logOutputCheckbox.name.slice(-1);
                const logOutputContent = document.querySelector('#logOutputContent');
                // TODO: Fetch the log output from the server and update the content
                logOutputContent.textContent += `Log Output ${logOutputNumber}\n`;
            }
        });
    });
}

function initializeCopyButtonEvents() {
    document.querySelectorAll('.copy-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const sectionTitle = btn.closest('.section').querySelector('.section-title').textContent;
            if (sectionTitle.includes('Visualization')) {
                // TODO: Implement image download functionality
                alert('Downloading images is not yet supported. Please manually save the image.');
            } else {
                const logOutput = document.querySelector('#logOutputContent');
                navigator.clipboard.writeText(logOutput.textContent).then(() => {
                    console.log('Text copied to clipboard');
                }).catch(err => {
                    console.error('Could not copy text: ', err);
                });
            }
        });
    });
}

function initializeCleanButtonEvents() {
    document.querySelectorAll('.clean-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const sectionTitle = btn.closest('.section').querySelector('.section-title').textContent;
            if (sectionTitle.includes('Visualization')) {
                document.querySelector('#visualizationContent').innerHTML = '';
            } else {
                document.querySelector('#logOutputContent').textContent = '';
            }
        });
    });
}

function initializeAddFileButtonEvent() {
    document.querySelector('#add-file-btn').addEventListener('click', () => {
        const fileUploadContainer = document.querySelector('.file-upload-container');
        const newFileUploadGroup = document.createElement('div');
        newFileUploadGroup.innerHTML = `
            <input type="file" class="file-upload">
            <p class="upload-feedback">File selected</p>
        `;
        fileUploadContainer.appendChild(newFileUploadGroup);
    });
}