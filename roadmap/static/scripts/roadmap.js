
window.addEventListener("DOMContentLoaded", () => {
    initializeCheckboxes();
    locateStep();
    loadProgress();
    showInfo();
    deleteConfirm();
    roadmapCompletedConfetti();
});

function initializeCheckboxes() {
    let numChkpts = 0; // Iniciar desde 0 para evitar problemas de índice
    const checkpointsDataEl = document.getElementById('checkpoints-data');
    if (!checkpointsDataEl) return;

    const checkpoints = JSON.parse(checkpointsDataEl.textContent);
    const checkboxes = document.querySelectorAll('input[type="checkbox"][name="remarkablePoint"]');

    checkboxes.forEach(checkbox => {
        checkbox.value = numChkpts;
        checkbox.checked = checkpoints[numChkpts] || false;
        numChkpts++;
    });
}

function locateStep() {
    const url = window.location.pathname;
    const splittedUrl = url.split('/');
    const stepNumber = parseInt(splittedUrl[splittedUrl.length - 1]);

    if (splittedUrl.length === 5 && stepNumber > 0) {
        openModal(stepNumber);
    }
}

function roadmapCompletedConfetti() {
    const checkboxes = document.querySelectorAll('input[type="checkbox"][name="remarkablePoint"]');
    const allChecked = Array.from(checkboxes).every(checkbox => checkbox.checked);

    if (allChecked) {
        const duration = 10 * 1000;
        const animationEnd = Date.now() + duration;
        const defaults = { startVelocity: 30, spread: 360, ticks: 60, zIndex: 0 };

        function randomInRange(min, max) {
            return Math.random() * (max - min) + min;
        }

        const interval = setInterval(() => {
            const timeLeft = animationEnd - Date.now();
            if (timeLeft <= 0) {
                clearInterval(interval);
                return;
            }

            const particleCount = 100 * (timeLeft / duration);
            try {
                confetti({ ...defaults, particleCount, origin: { x: randomInRange(0.1, 0.3), y: Math.random() - 0.2 } });
                confetti({ ...defaults, particleCount, origin: { x: randomInRange(0.7, 0.9), y: Math.random() - 0.2 } });
            } catch (error) {
                console.error("Confetti error:", error);
                clearInterval(interval);
            }
        }, 250);
    }
}

function openModal(step) {
    const stepElement = document.getElementById('modal' + step);
    if (stepElement) {
        stepElement.showModal();
    }
}

function submitForm(checkbox, step) {
    const checkpoint = document.getElementById('checkpoint' + step);
    if (!checkpoint) return;

    checkpoint.value = checkbox.value;
    checkpoint.removeAttribute('id'); // Eliminar el ID duplicado
    checkpoint.name = 'checkpoint';
    checkbox.form.submit();
}

function loadProgress() {
    const checkboxes = document.querySelectorAll('input[type="checkbox"][name="remarkablePoint"]');
    const checkedCount = Array.from(checkboxes).filter(checkbox => checkbox.checked).length;
    console.log(`Progreso: ${checkedCount} checkpoints completados`);
}

function deleteConfirm() {
    const btnModalDelete = document.getElementById('btn-modalDelete');
    const btnModalDeleteClose = document.getElementById('btn-modalDeleteClose');
    const modalDelete = document.getElementById('modalDelete');

    if (!btnModalDelete || !btnModalDeleteClose || !modalDelete) return;

    btnModalDelete.addEventListener("click", () => modalDelete.showModal());
    btnModalDeleteClose.addEventListener("click", () => modalDelete.close());

    window.addEventListener("click", (event) => {
        if (event.target === modalDelete) {
            modalDelete.close();
        }
    });
}

document.addEventListener("DOMContentLoaded", () => {
    const urlParams = new URLSearchParams(window.location.search);
    const status = urlParams.get("status");

    if (status) {
        const modalClone = document.getElementById("modalClone");
        const modalTitle = document.getElementById("modalTitle");
        const modalBody = document.getElementById("modalBody");

        if (status === "success") {
            modalTitle.textContent = "Success";
            modalBody.textContent = "Roadmap cloned successfully!";
        } else if (status === "exists") {
            modalTitle.textContent = "Warning";
            modalBody.textContent = "You already have a roadmap with the same content. Visit your profile to see it.";
        }

        modalClone?.showModal();
        if (window.history && window.history.replaceState) {
            history.replaceState(null, "", window.location.pathname);
        }
    }

    document.getElementById("btn-modalClone")?.addEventListener("click", () => {
        const modalClone = document.getElementById("modalClone");
        modalClone?.close();
    });

    const saveButton = document.getElementById('saveProgress');
    if (saveButton) {
        saveButton.addEventListener('click', async () => {
            const checkpoints = [];
            const checkboxes = document.querySelectorAll('input[name="remarkablePoint"]');

            checkboxes.forEach(checkbox => {
                checkpoints.push({
                    number: checkbox.value,
                    completed: checkbox.checked
                });
            });

            try {
                const response = await fetch('/roadmap/save-progress/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify({
                        roadmapId: document.body.dataset.roadmapId,
                        checkpoints: checkpoints
                    })
                });

                if (response.ok) {
                    alert('Progreso guardado con éxito');
                } else {
                    alert('Error al guardar el progreso');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Hubo un problema al guardar el progreso');
            }
        });
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (const cookie of cookies) {
                const trimmedCookie = cookie.trim();
                if (trimmedCookie.startsWith(`${name}=`)) {
                    cookieValue = decodeURIComponent(trimmedCookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
