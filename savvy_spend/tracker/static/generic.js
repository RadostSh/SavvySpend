document.getElementById('add-category-form').addEventListener('submit', function(e) {
    e.preventDefault();  // Предотвратяване на стандартното поведение на формата
    const formData = new FormData(this);

    fetch(addCategoryUrl, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': formData.get('csrfmiddlewaretoken'),  // Важно за Django CSRF защита
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Category added successfully');

            // Създаване на нов елемент в списъка
            const newListElement = document.createElement('li');
            newListElement.textContent = formData.get('category_name');  // Използвайте полето от формата за име на категорията

            // Добавяне на новия елемент към съществуващия списък
            const categoryList = document.getElementById('category-list');
            categoryList.appendChild(newListElement);

            // Изчистване на полето за въвеждане след добавяне
            this.reset();
        } else {
            alert('Error: ' + data.error);
        }
    })
    .catch(error => console.error('Error:', error));
});
