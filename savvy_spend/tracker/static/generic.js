document.addEventListener("DOMContentLoaded", function () {
 
    const currencyForm = document.getElementById('add-category-form');
 
    if (!currencyForm) {
        return;
    }
 
    currencyForm.addEventListener('submit', function(e) {
        e.preventDefault();
 
        const formData = new FormData(this);
        const url = this.getAttribute('data-url');
 
        fetch(url, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
                'X-Requested-With': 'XMLHttpRequest'
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
});
 
document.addEventListener("DOMContentLoaded", function () {
 
    const currencyForm = document.getElementById('add-transaction-form');
 
    if (!currencyForm) {
        return;
    }
 
    currencyForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);
        const url = this.getAttribute('data-url');
 
        fetch(url, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
                'X-Requested-With': 'XMLHttpRequest'
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
 
document.querySelectorAll('.add-funds-form').forEach(form => {
    form.addEventListener('submit', function(e) {
        e.preventDefault();
 
        const goalId = this.dataset.goalId;
        const formData = new FormData(this);
        const csrfToken = this.querySelector('[name=csrfmiddlewaretoken]').value;
 
        fetch(`/savings/add/${goalId}/`, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrfToken
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Funds added successfully');
 
                document.getElementById(`saved-amount-${goalId}`).innerText = `$${data.goal.current_amount}`;
                document.getElementById(`progress-${goalId}`).innerText = `${data.goal.progress}%`;
 
                this.reset();
            } else {
                alert('Error: ' + data.error);
            }
        })
        .catch(error => console.error('Error:', error));
    });
});
 
document.addEventListener("DOMContentLoaded", function () {

    const currencyForm = document.getElementById('currency-form');
    
    if (!currencyForm) {
        return;
    }

    currencyForm.addEventListener('submit', function(e) {
        e.preventDefault();

        const fromCurrency = document.getElementById('from-currency').value;
        const toCurrency = document.getElementById('to-currency').value;
        const amountElement = document.getElementById('amounts');
        const amount = amountElement.value.trim();

        if (!fromCurrency || !toCurrency || amount === "") {
            alert("Моля, въведете сума за конвертиране!");
            amountElement.focus();
            return;
        }

        fetch(`/convert/?from=${fromCurrency}&to=${toCurrency}&amount=${amount}`)
        .then(response => response.json())
        .then(data => {
            
            if (data.success) {
                document.getElementById('converted-amount').innerText = `$${data.converted_amount} ${toCurrency}`;
            } else {
                alert("Error: " + data.error);
            }
        })
        .catch(error => console.error('Error:', error));
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const savingsCalculator = document.getElementById('savings-calculator');
    
    if (savingsCalculator) {
        savingsCalculator.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const targetAmount = parseFloat(document.getElementById('target-savings').value);
            const avgSavings = parseFloat(document.getElementById('savings-calculator').dataset.avgSavings);
            
            if (isNaN(targetAmount) || targetAmount <= 0) {
                alert("Please enter a valid target amount.");
                return;
            }
            
            const monthsRequired = Math.ceil(targetAmount / avgSavings);
            document.getElementById('required-savings').innerText = `You need to save $${(targetAmount / monthsRequired).toFixed(2)} per month for the next ${monthsRequired} months.`;
        });
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const generateBtn = document.getElementById('generate-advice');
    const adviceBox = document.getElementById('advice-box');

    if (generateBtn && adviceBox) {
        generateBtn.addEventListener('click', async function () {
            adviceBox.innerHTML = '<p>Loading advice...</p>';

            try {
                const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
                const response = await fetch('/generate_financial_advice/', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken,
                    },
                });

                const data = await response.json();
                const formattedText = data.financial_advice
                    .replace(/\*/g, '')
                    .split('\n')
                    .map(paragraph => `<p>${paragraph}</p>`)
                    .join('');

                adviceBox.innerHTML = formattedText;
            } catch (error) {
                adviceBox.innerHTML = '<p>Failed to generate advice. Please try again.</p>';
                console.error('Error:', error);
            }
        });
    }
});