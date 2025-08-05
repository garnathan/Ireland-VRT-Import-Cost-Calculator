// VRT Calculator JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips if Bootstrap is available
    if (typeof bootstrap !== 'undefined') {
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    // Form validation and enhancement
    const vrtForm = document.getElementById('vrtForm');
    if (vrtForm) {
        initializeFormValidation();
        loadExchangeRate();
        setupRealTimeCalculation();
    }

    // Results page enhancements
    if (document.querySelector('.results-page')) {
        animateResults();
    }
});

// Form validation
function initializeFormValidation() {
    const form = document.getElementById('vrtForm');
    const ukPriceInput = document.getElementById('uk_price');
    const co2Input = document.getElementById('co2_emissions');
    const fuelTypeSelect = document.getElementById('fuel_type');

    // Real-time validation
    ukPriceInput.addEventListener('input', function() {
        validateUKPrice(this);
    });

    co2Input.addEventListener('input', function() {
        validateCO2Emissions(this);
        updateVRTRateIndicator(this.value);
    });

    fuelTypeSelect.addEventListener('change', function() {
        updateMinimumVRTInfo(this.value);
    });

    // Form submission validation
    form.addEventListener('submit', function(e) {
        if (!validateForm()) {
            e.preventDefault();
            showValidationErrors();
        } else {
            showLoadingState();
        }
    });
}

// Validate UK price input
function validateUKPrice(input) {
    const value = parseFloat(input.value);
    const feedback = input.parentNode.querySelector('.invalid-feedback') || createFeedbackElement(input.parentNode);
    
    if (isNaN(value) || value <= 0) {
        input.classList.add('is-invalid');
        input.classList.remove('is-valid');
        feedback.textContent = 'Please enter a valid price greater than £0';
    } else if (value > 1000000) {
        input.classList.add('is-invalid');
        input.classList.remove('is-valid');
        feedback.textContent = 'Price seems unusually high. Please verify.';
    } else {
        input.classList.remove('is-invalid');
        input.classList.add('is-valid');
        feedback.textContent = '';
    }
}

// Validate CO2 emissions input
function validateCO2Emissions(input) {
    const value = parseInt(input.value);
    const feedback = input.parentNode.querySelector('.invalid-feedback') || createFeedbackElement(input.parentNode);
    
    if (isNaN(value) || value <= 0) {
        input.classList.add('is-invalid');
        input.classList.remove('is-valid');
        feedback.textContent = 'Please enter valid CO2 emissions';
    } else if (value > 500) {
        input.classList.add('is-invalid');
        input.classList.remove('is-valid');
        feedback.textContent = 'CO2 emissions seem unusually high. Please verify.';
    } else {
        input.classList.remove('is-invalid');
        input.classList.add('is-valid');
        feedback.textContent = '';
    }
}

// Create feedback element for validation
function createFeedbackElement(parent) {
    const feedback = document.createElement('div');
    feedback.className = 'invalid-feedback';
    parent.appendChild(feedback);
    return feedback;
}

// Update VRT rate indicator based on CO2 emissions
function updateVRTRateIndicator(co2Value) {
    const co2 = parseInt(co2Value);
    if (isNaN(co2)) return;

    let rate, className, description;
    
    // Official Irish Revenue VRT rates
    if (co2 <= 50) {
        rate = 7;
        className = 'co2-low';
        description = 'Very low emissions - Excellent';
    } else if (co2 <= 80) {
        rate = 9;
        className = 'co2-low';
        description = 'Low emissions - Very good';
    } else if (co2 <= 85) {
        rate = 9.75;
        className = 'co2-low';
        description = 'Low emissions - Good';
    } else if (co2 <= 90) {
        rate = 10.5;
        className = 'co2-low';
        description = 'Moderate emissions';
    } else if (co2 <= 95) {
        rate = 11.25;
        className = 'co2-low';
        description = 'Moderate emissions';
    } else if (co2 <= 100) {
        rate = 12;
        className = 'co2-low';
        description = 'Moderate emissions';
    } else if (co2 <= 105) {
        rate = 12.75;
        className = 'co2-medium';
        description = 'Moderate emissions';
    } else if (co2 <= 110) {
        rate = 13.5;
        className = 'co2-medium';
        description = 'Moderate emissions';
    } else if (co2 <= 115) {
        rate = 15.25;
        className = 'co2-medium';
        description = 'Higher emissions';
    } else if (co2 <= 120) {
        rate = 16;
        className = 'co2-medium';
        description = 'Higher emissions';
    } else if (co2 <= 125) {
        rate = 16.75;
        className = 'co2-medium';
        description = 'Higher emissions';
    } else if (co2 <= 130) {
        rate = 17.5;
        className = 'co2-medium';
        description = 'Higher emissions';
    } else if (co2 <= 135) {
        rate = 19.25;
        className = 'co2-medium';
        description = 'High emissions';
    } else if (co2 <= 140) {
        rate = 20;
        className = 'co2-medium';
        description = 'High emissions';
    } else if (co2 <= 145) {
        rate = 21.5;
        className = 'co2-high';
        description = 'High emissions';
    } else if (co2 <= 150) {
        rate = 25;
        className = 'co2-high';
        description = 'Very high emissions';
    } else if (co2 <= 155) {
        rate = 27.5;
        className = 'co2-high';
        description = 'Very high emissions';
    } else if (co2 <= 170) {
        rate = 30;
        className = 'co2-high';
        description = 'Very high emissions';
    } else if (co2 <= 190) {
        rate = 35;
        className = 'co2-high';
        description = 'Extremely high emissions';
    } else {
        rate = 41;
        className = 'co2-high';
        description = 'Maximum VRT rate';
    }

    // Update or create VRT rate indicator
    let indicator = document.getElementById('vrt-rate-indicator');
    if (!indicator) {
        indicator = document.createElement('div');
        indicator.id = 'vrt-rate-indicator';
        indicator.className = 'mt-2 p-2 rounded';
        document.getElementById('co2_emissions').parentNode.appendChild(indicator);
    }

    indicator.className = `mt-2 p-2 rounded ${className === 'co2-low' ? 'bg-success' : className === 'co2-medium' ? 'bg-warning' : 'bg-danger'} bg-opacity-10`;
    indicator.innerHTML = `
        <small class="${className}">
            <i class="fas fa-info-circle"></i>
            VRT Rate: <strong>${rate}%</strong> - ${description}
        </small>
    `;
}

// Update minimum VRT information based on fuel type
function updateMinimumVRTInfo(fuelType) {
    const minimumAmounts = {
        'petrol': 125,
        'diesel': 200,
        'electric': 0,
        'hybrid': 125
    };

    let info = document.getElementById('minimum-vrt-info');
    if (!info) {
        info = document.createElement('div');
        info.id = 'minimum-vrt-info';
        info.className = 'mt-2';
        document.getElementById('fuel_type').parentNode.appendChild(info);
    }

    const amount = minimumAmounts[fuelType] || 125;
    const color = fuelType === 'electric' ? 'success' : 'info';
    
    info.innerHTML = `
        <small class="text-${color}">
            <i class="fas fa-info-circle"></i>
            Minimum VRT for ${fuelType}: <strong>€${amount}</strong>
        </small>
    `;
}

// Load current exchange rate
function loadExchangeRate() {
    const exchangeRateDisplay = document.getElementById('exchange_rate_display');
    if (!exchangeRateDisplay) return;

    exchangeRateDisplay.value = 'Loading...';
    
    fetch('/api/exchange-rate')
        .then(response => response.json())
        .then(data => {
            exchangeRateDisplay.value = data.gbp_to_eur.toFixed(4);
            
            // Add timestamp info
            const timestamp = new Date(data.timestamp).toLocaleString();
            let timestampInfo = document.getElementById('exchange-rate-timestamp');
            if (!timestampInfo) {
                timestampInfo = document.createElement('small');
                timestampInfo.id = 'exchange-rate-timestamp';
                timestampInfo.className = 'text-muted d-block';
                exchangeRateDisplay.parentNode.parentNode.appendChild(timestampInfo);
            }
            timestampInfo.textContent = `Updated: ${timestamp}`;
        })
        .catch(error => {
            console.error('Error fetching exchange rate:', error);
            exchangeRateDisplay.value = '1.1700 (fallback)';
            
            let errorInfo = document.getElementById('exchange-rate-error');
            if (!errorInfo) {
                errorInfo = document.createElement('small');
                errorInfo.id = 'exchange-rate-error';
                errorInfo.className = 'text-warning d-block';
                exchangeRateDisplay.parentNode.parentNode.appendChild(errorInfo);
            }
            errorInfo.innerHTML = '<i class="fas fa-exclamation-triangle"></i> Using fallback rate - verify current rate';
        });
}

// Setup real-time calculation preview
function setupRealTimeCalculation() {
    const inputs = ['uk_price', 'co2_emissions', 'fuel_type', 'vehicle_age', 'import_origin'];
    let debounceTimer;

    inputs.forEach(inputId => {
        const input = document.getElementById(inputId);
        if (input) {
            input.addEventListener('input', function() {
                clearTimeout(debounceTimer);
                debounceTimer = setTimeout(showQuickEstimate, 500);
            });
            
            // Also listen for change events on select elements
            if (input.tagName === 'SELECT') {
                input.addEventListener('change', function() {
                    clearTimeout(debounceTimer);
                    debounceTimer = setTimeout(showQuickEstimate, 500);
                });
            }
        }
    });
}

// Show quick estimate without full calculation
function showQuickEstimate() {
    const ukPrice = parseFloat(document.getElementById('uk_price').value);
    const co2Emissions = parseInt(document.getElementById('co2_emissions').value);
    const exchangeRate = parseFloat(document.getElementById('exchange_rate_display').value);
    const importOrigin = document.getElementById('import_origin').value;

    if (isNaN(ukPrice) || isNaN(co2Emissions) || isNaN(exchangeRate)) return;

    // Quick calculation
    const vehicleValueEur = ukPrice * exchangeRate;
    const transportCosts = 350; // Rough estimate
    const omv = vehicleValueEur + transportCosts;
    
    // Customs Duty (10% of vehicle value for UK, 0% for Northern Ireland)
    const customsDuty = importOrigin === 'uk' ? vehicleValueEur * 0.10 : 0;
    
    // VRT calculation using official Irish Revenue rates
    let vrtRate;
    if (co2Emissions <= 50) vrtRate = 7;
    else if (co2Emissions <= 80) vrtRate = 9;
    else if (co2Emissions <= 85) vrtRate = 9.75;
    else if (co2Emissions <= 90) vrtRate = 10.5;
    else if (co2Emissions <= 95) vrtRate = 11.25;
    else if (co2Emissions <= 100) vrtRate = 12;
    else if (co2Emissions <= 105) vrtRate = 12.75;
    else if (co2Emissions <= 110) vrtRate = 13.5;
    else if (co2Emissions <= 115) vrtRate = 15.25;
    else if (co2Emissions <= 120) vrtRate = 16;
    else if (co2Emissions <= 125) vrtRate = 16.75;
    else if (co2Emissions <= 130) vrtRate = 17.5;
    else if (co2Emissions <= 135) vrtRate = 19.25;
    else if (co2Emissions <= 140) vrtRate = 20;
    else if (co2Emissions <= 145) vrtRate = 21.5;
    else if (co2Emissions <= 150) vrtRate = 25;
    else if (co2Emissions <= 155) vrtRate = 27.5;
    else if (co2Emissions <= 170) vrtRate = 30;
    else if (co2Emissions <= 190) vrtRate = 35;
    else vrtRate = 41;

    const estimatedVRT = omv * (vrtRate / 100);
    
    // VAT (21% on vehicle + customs duty + VRT)
    const vatBase = vehicleValueEur + customsDuty + estimatedVRT;
    const vatAmount = vatBase * 0.21;
    
    const totalEstimate = vehicleValueEur + transportCosts + customsDuty + estimatedVRT + vatAmount + 102;

    // Show quick estimate
    showQuickEstimateDisplay(totalEstimate, estimatedVRT, customsDuty, vatAmount, importOrigin);
}

// Display quick estimate
function showQuickEstimateDisplay(total, vrt, customsDuty, vat, importOrigin) {
    let estimateDiv = document.getElementById('quick-estimate');
    if (!estimateDiv) {
        estimateDiv = document.createElement('div');
        estimateDiv.id = 'quick-estimate';
        estimateDiv.className = 'alert alert-info mt-3';
        document.getElementById('vrtForm').appendChild(estimateDiv);
    }

    const customsDutyDisplay = importOrigin === 'uk' 
        ? `<span class="h6 text-danger">€${customsDuty.toFixed(0)}</span>`
        : `<span class="h6 text-success">€0 <small>(No duty)</small></span>`;

    estimateDiv.innerHTML = `
        <h6><i class="fas fa-calculator"></i> Quick Estimate</h6>
        <div class="row">
            <div class="col-md-3">
                <strong>VRT:</strong><br>
                <span class="h6 text-warning">€${vrt.toFixed(0)}</span>
            </div>
            <div class="col-md-3">
                <strong>Customs Duty:</strong><br>
                ${customsDutyDisplay}
            </div>
            <div class="col-md-3">
                <strong>VAT (21%):</strong><br>
                <span class="h6 text-primary">€${vat.toFixed(0)}</span>
            </div>
            <div class="col-md-3">
                <strong>Total Cost:</strong><br>
                <span class="h5 text-success">€${total.toFixed(0)}</span>
            </div>
        </div>
        <small class="text-muted">
            <i class="fas fa-info-circle"></i>
            Rough estimate - click calculate for detailed breakdown
        </small>
    `;
}

// Validate entire form
function validateForm() {
    const ukPrice = parseFloat(document.getElementById('uk_price').value);
    const co2Emissions = parseInt(document.getElementById('co2_emissions').value);
    
    return !isNaN(ukPrice) && ukPrice > 0 && 
           !isNaN(co2Emissions) && co2Emissions > 0 && co2Emissions <= 500;
}

// Show validation errors
function showValidationErrors() {
    const alert = document.createElement('div');
    alert.className = 'alert alert-danger alert-dismissible fade show mt-3';
    alert.innerHTML = `
        <i class="fas fa-exclamation-triangle"></i>
        <strong>Please correct the following errors:</strong>
        <ul class="mb-0 mt-2">
            <li>Ensure UK price is greater than £0</li>
            <li>Ensure CO2 emissions are between 1 and 500 g/km</li>
        </ul>
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.getElementById('vrtForm').insertBefore(alert, document.getElementById('vrtForm').firstChild);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (alert.parentNode) {
            alert.remove();
        }
    }, 5000);
}

// Show loading state during calculation
function showLoadingState() {
    const submitBtn = document.querySelector('button[type="submit"]');
    if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = `
            <span class="spinner-border spinner-border-sm me-2" role="status"></span>
            Calculating...
        `;
    }
}

// Animate results on results page
function animateResults() {
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
}

// Utility function to format currency
function formatCurrency(amount, currency = 'EUR') {
    return new Intl.NumberFormat('en-IE', {
        style: 'currency',
        currency: currency,
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    }).format(amount);
}

// Copy results to clipboard
function copyResults() {
    const resultsText = document.querySelector('.results-summary').innerText;
    navigator.clipboard.writeText(resultsText).then(() => {
        showToast('Results copied to clipboard!', 'success');
    }).catch(() => {
        showToast('Failed to copy results', 'error');
    });
}

// Show toast notification
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `alert alert-${type === 'error' ? 'danger' : type === 'success' ? 'success' : 'info'} position-fixed`;
    toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    toast.innerHTML = `
        ${message}
        <button type="button" class="btn-close ms-2" onclick="this.parentElement.remove()"></button>
    `;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        if (toast.parentNode) {
            toast.remove();
        }
    }, 3000);
}
