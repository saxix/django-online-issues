document.addEventListener('DOMContentLoaded', function () {
    const script = document.getElementById('django-issues-script');

    const MODAL_OVERLAY_ID = 'django-issues-modal-overlay';
    const FORM_CONTAINER_ID = 'django-issues-form-container';
    const OPENER_ID = 'issue-opener';
    const FORM_ID = 'django-issues-form';
    const SCREENSHOT_PREVIEW_CONTAINER_ID = 'screenshot-preview-container';
    const SCREENSHOT_PREVIEW_IMG_ID = 'screenshot-preview-img';
    const MESSAGE_CONTAINER_ID = 'form-message-container';
    const ERRORS_CONTAINER_ID = 'form-error-container';

    const SCREENSHOT_LIBRARY = script.dataset.engine; // 'html2canvas' or 'dom-to-image'
    const SUBMIT_URL = script.dataset.url;

    axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
    axios.defaults.xsrfCookieName = "csrftoken";

    function createModal() {
        // Prevent creating multiple modals
        if (document.getElementById(MODAL_OVERLAY_ID)) {
            return;
        }

        const modalOverlay = document.createElement('div');
        modalOverlay.id = MODAL_OVERLAY_ID;
        modalOverlay.className = 'modal-overlay';
        modalOverlay.style.display = 'none';

        const modalContent = document.createElement('div');
        modalContent.id = FORM_CONTAINER_ID;
        modalContent.className = 'modal-content';

        modalOverlay.appendChild(modalContent);
        document.body.appendChild(modalOverlay);

        // Add event listener to close the modal by clicking on the overlay
        modalOverlay.addEventListener('click', function(event) {
            if (event.target === this) {
                this.style.display = 'none';
            }
        });
    }

    function displayMessage(container, message, isError = false) {
        const target = container.querySelector('.message');
        target.innerHTML = message;
        container.style.backgroundColor = isError ? '#f8d7da' : '#d4edda'; // Light red for error, light green for success
        container.style.color = isError ? '#721c24' : '#155724'; // Dark red for error, dark green for success
        container.style.border = `1px solid ${isError ? '#f5c6cb' : '#c3e6cb'}`;
        container.style.display = 'block';
    }

    function clearMessage(container) {
        const target = container.querySelector('.message');
        target.innerHTML = "";
        container.style.display = 'none';
    }

    const issueOpener = document.getElementById(OPENER_ID);
    if (issueOpener) {
        issueOpener.addEventListener('click', function() {
            let screenshotPromise = Promise.resolve(null); // Default to no screenshot data

            if (SCREENSHOT_LIBRARY) { // Only attempt screenshot if a library is configured
                if (SCREENSHOT_LIBRARY === 'html2canvas') {
                    screenshotPromise = html2canvas(document.body, {
                        width: window.innerWidth,
                        height: document.documentElement.scrollHeight,
                        allowTaint: true,
                        scale: 1,
                        foreignObjectRendering: true,
                        useCORS: true,
                    }).then(canvas => canvas.toDataURL("image/png"));
                } else if (SCREENSHOT_LIBRARY === 'dom-to-image') {
                    screenshotPromise = domtoimage.toPng(document.body);
                }
            }

            screenshotPromise.then(function (screenshotData) {
                createModal(); // Ensure the modal structure exists

                axios.get(SUBMIT_URL)
                    .then(response => {
                        const formContainer = document.getElementById(FORM_CONTAINER_ID);
                        const modalOverlay = document.getElementById(MODAL_OVERLAY_ID);
                        if (formContainer && modalOverlay) {
                            formContainer.innerHTML = response.data;

                            const titleInput = formContainer.querySelector('input[name="title"]');
                            const screenshotInput = formContainer.querySelector('input[name="screenshot"]');
                            const addScreenshotCheckbox = formContainer.querySelector('input[name="add_screenshot"]');
                            const screenshotPreviewContainer = document.getElementById(SCREENSHOT_PREVIEW_CONTAINER_ID);
                            const screenshotPreviewImg = document.getElementById(SCREENSHOT_PREVIEW_IMG_ID);

                            if (SCREENSHOT_LIBRARY) {
                                // Screenshot support is enabled
                                screenshotInput.value = screenshotData;
                                screenshotPreviewImg.src = screenshotData;

                                function togglePreview(show) {
                                    screenshotPreviewContainer.style.visibility = show ? 'visible' : 'hidden';
                                    screenshotPreviewContainer.style.opacity = show ? '1' : '0';
                                }

                                togglePreview(addScreenshotCheckbox.checked);

                                addScreenshotCheckbox.addEventListener('change', function() {
                                    togglePreview(this.checked);
                                });
                            } else {
                                // Screenshot support is disabled
                                if (screenshotInput) screenshotInput.remove(); // Remove hidden input
                                if (addScreenshotCheckbox) addScreenshotCheckbox.closest('p').remove(); // Remove checkbox and its label
                                if (screenshotPreviewContainer) screenshotPreviewContainer.remove(); // Remove preview container
                            }
                            modalOverlay.style.display = 'flex';
                            titleInput.focus();
                        }
                    })
                    .catch(error => {
                        console.error('Error loading form:', error);
                    });
            });
        });
        issueOpener.style.display = 'block';
    }

    // Use event delegation on the document to handle the form submission
    document.addEventListener('submit', function(event) {
        if (event.target.id === FORM_ID) {
            event.preventDefault();

            const form = event.target;
            const modalOverlay= document.getElementById(MODAL_OVERLAY_ID);
            const messageContainer = modalOverlay.querySelector(`#${MESSAGE_CONTAINER_ID}`);
            const errorContainer = modalOverlay.querySelector(`#${ERRORS_CONTAINER_ID}`);
            if (messageContainer) clearMessage(messageContainer); // Clear previous messages

            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());

            // If add_screenshot is not checked, remove screenshot from data
            if (!data.add_screenshot) {
                delete data.screenshot;
            }

            axios.post(SUBMIT_URL, data, {
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': data.csrfmiddlewaretoken
                }
            })
            .then(response => {
                if (response.data.success) {
                    const formContainer = document.getElementById(FORM_CONTAINER_ID);
                    const form = formContainer.querySelector("form");

                    if (messageContainer) {
                        // formContainer.innerHTML = '';
                        form.style.display = 'none';
                        displayMessage(messageContainer, response.data.message, false);
                    }

                    // Optionally hide modal after a delay for success message to be read
                    setTimeout(() => {
                        const modalOverlay = document.getElementById(MODAL_OVERLAY_ID);
                        if (modalOverlay) {
                            modalOverlay.style.display = 'none';
                        }
                        if (formContainer) {
                            formContainer.innerHTML = ''; // Clear the content
                        }
                        if (messageContainer) clearMessage(messageContainer); // Clear message after hiding modal
                    }, 3000); // Hide after 3 seconds

                } else {
                    // Display error message and form errors
                    let errorMessage = response.data.message || "An error occurred.";
                    if (response.data.errors) {
                        errorMessage += "<br><ul>";
                        for (const field in response.data.errors) {
                            errorMessage += `<li><strong>${field}:</strong> ${response.data.errors[field].join(", ")}</li>`;
                        }
                        errorMessage += "</ul>";
                    }
                    if (errorContainer){
                        displayMessage(errorContainer, errorMessage, true);
                    }
                }
            })
            .catch(error => {
                const errorMessage = error.response && error.response.data && error.response.data.message
                                     ? error.response.data.message
                                     : "An unexpected error occurred.";
                if (messageContainer) displayMessage(messageContainer, errorMessage, true);
                console.error('Error submitting form:', error);
            });
        }
    });

    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            const modalOverlay = document.getElementById(MODAL_OVERLAY_ID);
            if (modalOverlay && modalOverlay.style.display !== 'none') {
                modalOverlay.style.display = 'none';
            }
        }
    });
});
