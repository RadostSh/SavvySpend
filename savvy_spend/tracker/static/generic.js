document.getElementById('add-category-form').addEventListener('submit', function(e) {
    e.preventDefault();  // Спира стандартното изпращане на формата

    const formData = new FormData(this);

    fetch("{% url 'add_category' %}", {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Category added successfully');

            // Добавяне на новата категория в списъка без презареждане
            const categoryList = document.getElementById('category-list');
            const newListItem = document.createElement('li');
            newListItem.textContent = data.category.name;
            categoryList.appendChild(newListItem);

            // Ако има dropdown за категории, добавяме новата категория в него
            const categoryDropdown = document.getElementById('category');
            if (categoryDropdown) {
                const newOption = document.createElement('option');
                newOption.value = data.category.id;
                newOption.textContent = data.category.name;
                categoryDropdown.appendChild(newOption);
            }

            this.reset(); // Изчистване на формата
        } else {
            alert('Error: ' + data.error);
        }
    })
    .catch(error => console.error('Error:', error));
});


document.getElementById('add-transaction-form').addEventListener('submit', function(e) {
    e.preventDefault();  // Спира стандартното изпращане на формата
    const formData = new FormData(this);

    fetch("{% url 'add_transaction' %}", {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Transaction added successfully');

            // Добавяне на транзакцията в таблицата без презареждане
            const newTransactionElement = document.createElement('tr');
            newTransactionElement.innerHTML = `
                <td>${data.transaction.date}</td>
                <td>${data.transaction.type}</td>
                <td>${data.transaction.amount}</td>
                <td>${data.transaction.category}</td>
                <td>${data.transaction.description}</td>`;
            document.getElementById('transaction-list').appendChild(newTransactionElement);

            this.reset(); // Изчистване на формата
        } else {
            alert('Error: ' + data.error);
        }
    })
    .catch(error => console.error('Error:', error));
});



