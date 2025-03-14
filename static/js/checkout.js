document.addEventListener('DOMContentLoaded', function() {
    const salesForm = document.getElementById('sales-form');
    if (!salesForm) return;

    // Initialize date fields
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('receipt-date').value = today;
    document.querySelector('input[type="date"]').value = today;

    // Initialize elements
    const salesEntries = document.getElementById('sales-entries');
    const addRowBtn = document.getElementById('add-row');
    const submitButton = document.getElementById('submit-button');
    const loadingSpinner = document.getElementById('loading-spinner');
    const successMessage = document.getElementById('success-message');
    
    loadingSpinner.style.display = 'none';

    // Customer selection handler
    const customerSelect = document.getElementById('customer');
    const emailInput = document.getElementById('email');
    
    customerSelect.addEventListener('change', function() {
        const selectedOption = this.options[this.selectedIndex];
        if (selectedOption.dataset.email) {
            emailInput.value = selectedOption.dataset.email;
        }
    });

    // Setup row functionality
    function setupRowHandlers(row) {
        const productSelect = row.querySelector('.product-select');
        const quantityInput = row.querySelector('.quantity-input');
        const priceInput = row.querySelector('.price-input');
        const stockDisplay = row.querySelector('.stock-display');
        const amountDisplay = row.querySelector('.amount');
        const deleteBtn = row.querySelector('.delete-row-btn');

        // Product selection handler
        productSelect.addEventListener('change', function() {
            const selectedOption = this.options[this.selectedIndex];
            if (selectedOption.value) {
                const stock = parseInt(selectedOption.dataset.stock) || 0;
                const price = parseFloat(selectedOption.dataset.price) || 0;
                
                stockDisplay.textContent = stock;
                stockDisplay.classList.toggle('low', stock < 10);
                quantityInput.max = stock;
                priceInput.value = price.toFixed(2);
                
                calculateRowAmount();
            } else {
                resetRow();
            }
        });

        // Quantity change handler
        quantityInput.addEventListener('input', function() {
            const max = parseInt(this.max);
            let value = parseInt(this.value) || 0;
            
            if (max && value > max) {
                alert('Quantity cannot exceed available stock');
                value = max;
                this.value = max;
            }
            if (value < 1) {
                value = 1;
                this.value = 1;
            }
            calculateRowAmount();
        });

        // Price change handler
        priceInput.addEventListener('input', function() {
            calculateRowAmount();
        });

        // Delete row handler
        deleteBtn.addEventListener('click', function(e) {
            e.preventDefault();
            if (salesEntries.children.length > 1) {
                row.remove();
                renumberRows();
                calculateTotals();
            } else {
                alert('Cannot delete the last row');
            }
        });

        function calculateRowAmount() {
            const quantity = parseInt(quantityInput.value) || 0;
            const price = parseFloat(priceInput.value) || 0;
            const amount = quantity * price;
            amountDisplay.textContent = amount.toFixed(2);
            calculateTotals();
        }

        function resetRow() {
            stockDisplay.textContent = '-';
            stockDisplay.classList.remove('low');
            quantityInput.max = '';
            priceInput.value = '0.00';
            amountDisplay.textContent = '0.00';
            calculateTotals();
        }
    }

    // Add row button handler
    addRowBtn.addEventListener('click', function() {
        const template = salesEntries.children[0].cloneNode(true);
        const inputs = template.querySelectorAll('input, select');
        inputs.forEach(input => {
            if (input.type === 'date') {
                input.value = today;
            } else if (input.classList.contains('quantity-input')) {
                input.value = '1';
                input.max = '';
            } else if (input.classList.contains('price-input')) {
                input.value = '0.00';
            } else if (input.classList.contains('product-select')) {
                input.selectedIndex = 0;
            }
        });
        
        template.querySelector('.stock-display').textContent = '-';
        template.querySelector('.stock-display').classList.remove('low');
        template.querySelector('.amount').textContent = '0.00';
        
        salesEntries.appendChild(template);
        renumberRows();
        setupRowHandlers(template);
    });

    // Renumber rows
    function renumberRows() {
        Array.from(salesEntries.children).forEach((row, index) => {
            row.children[0].textContent = index + 1;
        });
    }

    // Calculate totals
    function calculateTotals() {
        const amounts = Array.from(salesEntries.querySelectorAll('.amount'))
            .map(el => parseFloat(el.textContent) || 0);
            
        const subtotal = amounts.reduce((sum, amount) => sum + amount, 0);
        const discount = parseFloat(document.getElementById('discount').value) || 0;
        const total = Math.max(0, subtotal - discount);
        
        document.getElementById('subtotal').textContent = subtotal.toFixed(2);
        document.getElementById('total').textContent = total.toFixed(2);
        
        // Update delivered/deposited max values
        document.getElementById('delivered').max = total;
        document.getElementById('deposited').max = total;
    }

    // Payment amount handlers
    ['delivered', 'deposited', 'discount'].forEach(id => {
        const input = document.getElementById(id);
        input.addEventListener('input', function() {
            const value = parseFloat(this.value) || 0;
            const total = parseFloat(document.getElementById('total').textContent);
            
            if (value < 0) this.value = 0;
            if (this.max && value > parseFloat(this.max)) {
                this.value = this.max;
            }
            
            if (id === 'discount') {
                calculateTotals();
            }
        });
    });

    // Setup initial row
    setupRowHandlers(salesEntries.children[0]);

    // Form submission
    salesForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Validate customer
        if (!document.getElementById('customer').value) {
            alert('Please select a customer');
            return;
        }

        // Validate items
        const items = Array.from(salesEntries.children).map(row => ({
            product: row.querySelector('.product-select').value,
            quantity: parseInt(row.querySelector('.quantity-input').value) || 0,
            price: parseFloat(row.querySelector('.price-input').value) || 0
        }));

        if (!items.some(item => item.product && item.quantity > 0)) {
            alert('Please add at least one valid item');
            return;
        }

        submitButton.disabled = true;
        loadingSpinner.style.display = 'flex';

        try {
            const saleData = {
                receipt_number: document.getElementById('receipt-number').value,
                receipt_date: document.getElementById('receipt-date').value,
                customer: document.getElementById('customer').value,
                email: document.getElementById('email').value,
                payment_method: document.getElementById('payment-method').value,
                reference_no: document.getElementById('reference-no').value,
                deposit_to: document.getElementById('deposit-to').value,
                items: items.filter(item => item.product).map(item => ({
                    service_date: today,
                    product: item.product,
                    description: '',
                    quantity: item.quantity,
                    rate: item.price,
                    amount: (item.quantity * item.price).toFixed(2)
                })),
                subtotal: parseFloat(document.getElementById('subtotal').textContent),
                discount: parseFloat(document.getElementById('discount').value) || 0,
                total: parseFloat(document.getElementById('total').textContent),
                delivered: parseFloat(document.getElementById('delivered').value) || 0,
                deposited: parseFloat(document.getElementById('deposited').value) || 0
            };

            const response = await fetch('/sales', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(saleData)
            });

            const result = await response.json();
            
            if (response.ok) {
                successMessage.querySelector('.message-text').textContent = 
                    `Sale recorded successfully! Reference: ${result.reference}`;
                successMessage.style.display = 'flex';
                
                setTimeout(() => {
                    window.location.href = '/sales/history';
                }, 2000);
            } else {
                throw new Error(result.error || 'Failed to save sale');
            }
        } catch (error) {
            alert(error.message);
        } finally {
            submitButton.disabled = false;
            loadingSpinner.style.display = 'none';
        }
    });
});