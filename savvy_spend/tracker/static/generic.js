document.getElementById('add-category-form').addEventListener('submit', function(e) {
    e.preventDefault();

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

            const categoryList = document.getElementById('category-list');
            const newListItem = document.createElement('li');
            newListItem.textContent = data.category.name;
            categoryList.appendChild(newListItem);

            const categoryDropdown = document.getElementById('category');
            if (categoryDropdown) {
                const newOption = document.createElement('option');
                newOption.value = data.category.id;
                newOption.textContent = data.category.name;
                categoryDropdown.appendChild(newOption);
            }

            this.reset();
        } else {
            alert('Error: ' + data.error);
        }
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById('add-transaction-form').addEventListener('submit', function(e) {
    e.preventDefault();
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

            const newTransactionElement = document.createElement('tr');
            newTransactionElement.innerHTML = `
                <td>${data.transaction.date}</td>
                <td>${data.transaction.type}</td>
                <td>${data.transaction.amount}</td>
                <td>${data.transaction.category}</td>
                <td>${data.transaction.description}</td>`;
            document.getElementById('transaction-list').appendChild(newTransactionElement);

            this.reset();
        } else {
            alert('Error: ' + data.error);
        }
    })
    .catch(error => console.error('Error:', error));
});

function deleteTransaction(transactionId) {
    if (!confirm("Are you sure you want to delete this transaction?")) return;

    fetch(`/transactions/delete/${transactionId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            'X-Requested-With': 'XMLHttpRequest'
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            document.getElementById(`transaction-${transactionId}`).remove();
        } else {
            alert("Error deleting transaction.");
        }
    })
    .catch(error => console.error('Error:', error));
}

function deleteCategory(categoryId) {
    if (!confirm("Are you sure you want to delete this category?")) return;

    fetch(`/delete_category/${categoryId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            'X-Requested-With': 'XMLHttpRequest'
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Category deleted successfully!");
            document.getElementById(`category-${categoryId}`).remove();
        } else {
            alert("Error deleting category.");
        }
    })
    .catch(error => console.error('Error:', error));
}

document.getElementById('add-budget-form').addEventListener('submit', function(e) {
    e.preventDefault();

    const formData = new FormData(this);
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch("{% url 'budget' %}", {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrfToken
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Budget added successfully');

            const newRow = document.createElement('tr');
            newRow.innerHTML = `
                <td>${data.budget.month}/${data.budget.year}</td>
                <td>$0.00</td>  <!-- Тук може да добавим приходи, ако искаш -->
                <td>$0.00</td>  <!-- Тук може да добавим разходи -->
                <td>$${data.budget.amount}</td>
            `;
            document.getElementById('budget-list').appendChild(newRow);

            this.reset();
        } else {
            alert('Error: ' + data.error);
        }
    })
    .catch(error => console.error('Error:', error));
});

