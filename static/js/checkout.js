document.addEventListener('DOMContentLoaded', function() {
    const salesForm = document.getElementById('sales-form');
    const salesEntries = document.getElementById('sales-entries');
    const addRowBtn = document.getElementById('add-row');
    const subtotalEl = document.getElementById('subtotal');
    const discountEl = document.getElementById('discount');
    const totalEl = document.getElementById('total');
    const deliveredEl = document.getElementById('delivered');
    const depositedEl = document.getElementById('deposited');

    // Calculate row amount
    function calculateRowAmount(row) {
        // Get quantity and rate inputs within this specific row
        const quantityInput = row.querySelector('input[type="number"][min="1"]');
        const rateInput = row.querySelector('input[type="number"][step="0.01"]');
        const amountCell = row.querySelector('.amount');

        if (quantityInput && rateInput && amountCell) {
            const quantity = parseFloat(quantityInput.value) || 0;
            const rate = parseFloat(rateInput.value) || 0;
            const amount = quantity * rate;
            amountCell.textContent = amount.toFixed(2);
            calculateTotals();
        }
    }

    // Calculate all totals
    function calculateTotals() {
        let subtotal = 0;
        // Calculate subtotal from all row amounts
        document.querySelectorAll('#sales-entries tr').forEach(row => {
            const amountCell = row.querySelector('.amount');
            if (amountCell) {
                subtotal += parseFloat(amountCell.textContent) || 0;
            }
        });

        // Update subtotal display
        subtotalEl.textContent = subtotal.toFixed(2);

        // Calculate final total with discount
        const discount = parseFloat(discountEl.value) || 0;
        if (discount > subtotal) {
            discountEl.value = subtotal.toFixed(2);
            alert('Discount cannot exceed subtotal');
            return;
        }

        const total = subtotal - discount;
        totalEl.textContent = total.toFixed(2);

        // Adjust delivered and deposited amounts if they exceed new total
        const delivered = parseFloat(deliveredEl.value) || 0;
        if (delivered > total) {
            deliveredEl.value = total.toFixed(2);
        }

        const deposited = parseFloat(depositedEl.value) || 0;
        if (deposited > Math.min(total, delivered)) {
            depositedEl.value = Math.min(total, delivered).toFixed(2);
        }
    }

    // Add new row to sales table
    function addNewRow() {
        const rowCount = salesEntries.children.length;
        const newRow = document.createElement('tr');
        newRow.innerHTML = `
            <td>${rowCount + 1}</td>
            <td><input type="date" class="form-control-sm" required></td>
            <td><input type="text" class="form-control-sm" required></td>
            <td><input type="text" class="form-control-sm"></td>
            <td><input type="number" class="form-control-sm" min="1" value="1" required></td>
            <td><input type="number" class="form-control-sm" step="0.01" value="0.00" required></td>
            <td class="amount">0.00</td>
        `;
        salesEntries.appendChild(newRow);
        attachRowListeners(newRow);
        calculateTotals();
    }

    // Attach event listeners to row inputs
    function attachRowListeners(row) {
        const quantityInput = row.querySelector('input[type="number"][min="1"]');
        const rateInput = row.querySelector('input[type="number"][step="0.01"]');

        if (quantityInput && rateInput) {
            quantityInput.addEventListener('input', () => calculateRowAmount(row));
            rateInput.addEventListener('input', () => calculateRowAmount(row));
        }
    }

    // Initialize form
    function initializeForm() {
        // Set today's date as default
        const today = new Date().toISOString().split('T')[0];
        document.getElementById('receipt-date').value = today;

        // Initialize first row calculations
        const firstRow = salesEntries.querySelector('tr');
        if (firstRow) {
            attachRowListeners(firstRow);
            calculateRowAmount(firstRow);
        }
    }

    // Add event listeners for amount inputs
    discountEl.addEventListener('input', calculateTotals);
    deliveredEl.addEventListener('input', function() {
        const delivered = parseFloat(this.value) || 0;
        if (delivered < 0) this.value = 0;
        calculateTotals();
    });

    depositedEl.addEventListener('input', function() {
        const deposited = parseFloat(this.value) || 0;
        if (deposited < 0) this.value = 0;
        calculateTotals();
    });

    // Add event listener for add row button
    addRowBtn.addEventListener('click', addNewRow);

    // Form submission handler
    salesForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Validate form
        if (!this.checkValidity()) {
            alert('Please fill in all required fields.');
            return;
        }

        // Show loading state
        const submitButton = document.getElementById('submit-button');
        const loadingSpinner = document.getElementById('loading-spinner');
        const successMessage = document.getElementById('success-message');
        
        submitButton.style.display = 'none';
        loadingSpinner.style.display = 'flex';
        salesForm.classList.add('form-submitting');

        // Collect form data
        const formData = {
            receipt_number: document.getElementById('receipt-number').textContent,
            customer: document.getElementById('customer').value,
            email: document.getElementById('email').value,
            receipt_date: document.getElementById('receipt-date').value,
            payment_method: document.getElementById('payment-method').value,
            reference_no: document.getElementById('reference-no').value,
            deposit_to: document.getElementById('deposit-to').value,
            subtotal: subtotalEl.textContent,
            discount: discountEl.value,
            total: totalEl.textContent,
            delivered: deliveredEl.value,
            deposited: depositedEl.value,
            items: []
        };

        // Collect items data
        document.querySelectorAll('#sales-entries tr').forEach(row => {
            const inputs = row.querySelectorAll('input');
            formData.items.push({
                service_date: inputs[0].value,
                product: inputs[1].value,
                description: inputs[2].value,
                quantity: inputs[3].value,
                rate: inputs[4].value,
                amount: row.querySelector('.amount').textContent
            });
        });

        // Submit form
        fetch('/sales', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrf_token')
            },
            body: JSON.stringify(formData)
        })
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json();
        })
        .then(data => {
            if (data.status === 'success') {
                // Show success message
                successMessage.querySelector('.message-text').textContent = 
                    `Sale recorded successfully! Reference: ${data.reference}`;
                successMessage.style.display = 'flex';
                
                // Redirect after showing message briefly
                setTimeout(() => {
                    window.location.href = '/sales_storage';
                }, 2000);
            } else {
                throw new Error(data.message || 'An error occurred while saving the sale');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert(error.message || 'There was an error submitting the form. Please try again.');
            resetSubmitState();
        });
    });

    // Helper function to reset submit button state
    function resetSubmitState() {
        const submitButton = document.getElementById('submit-button');
        const loadingSpinner = document.getElementById('loading-spinner');
        
        submitButton.style.display = 'inline-flex';
        loadingSpinner.style.display = 'none';
        salesForm.classList.remove('form-submitting');
    }

    // Get CSRF token
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }

    // Initialize the form
    initializeForm();
});