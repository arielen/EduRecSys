document.addEventListener('DOMContentLoaded', function () {
    function updateSoftSkillOptions() {
        const softSkillSelects = document.querySelectorAll('select[id^="id_olimpiadsoftskill-"][id$="-ss"]');
        const selectedSoftSkills = Array.from(softSkillSelects).map(select => select.value).filter(value => value);

        softSkillSelects.forEach(select => {
            Array.from(select.options).forEach(option => {
                if (selectedSoftSkills.includes(option.value) && option.value !== select.value) {
                    option.style.display = 'none';
                } else {
                    option.style.display = '';
                }
            });
        });
    }

    function addEventListeners() {
        const softSkillSelects = document.querySelectorAll('select[id^="id_olimpiadsoftskill-"][id$="-ss"]');
        softSkillSelects.forEach(select => {
            select.addEventListener('change', updateSoftSkillOptions);
        });
    }

    updateSoftSkillOptions();
    addEventListeners();

    document.addEventListener('click', function (event) {
        if (event.target.closest('button[id^="id_olimpiadsoftskill-ADD"]')) {
            setTimeout(function () {
                addEventListeners();
                updateSoftSkillOptions();
            }, 100);
        }

        const deleteButton = event.target.closest('button[id$="-DELETE-button"]');
        if (deleteButton) {
            const buttonId = deleteButton.id;
            const match = buttonId.match(/id_olimpiadsoftskill-(\d+)-DELETE-button/);
            if (match) {
                const index = match[1];
                // Находим соответствующий select элемент
                const selectElement = document.querySelector(`select[id="id_olimpiadsoftskill-${index}-ss"]`);
                if (selectElement) {
                    // Убираем значение из select
                    selectElement.value = "";
                    // Обновляем доступные опции
                    updateSoftSkillOptions();
                }
            }
        }
    });
});