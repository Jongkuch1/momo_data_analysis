class MoMoDashboard {
    constructor() {
        this.apiBase = 'http://localhost:5000/api';
        this.transactions = [];
        this.statistics = {};
        this.charts = {};
        this.init();
    }

    async init() {
        this.showLoading();
        await this.loadData();
        this.setupEventListeners();
        this.hideLoading();
    }

    showLoading() {
        document.getElementById('loadingSpinner').style.display = 'block';
    }

    hideLoading() {
        document.getElementById('loadingSpinner').style.display = 'none';
    }

    async loadData() {
        try {
            await Promise.all([
                this.loadStatistics(),
                this.loadTransactions()
            ]);
            this.updateDashboard();
        } catch (error) {
            console.error('Error loading data:', error);
            this.showError('Failed to load data. Please ensure the API server is running.');
        }
    }

    async loadStatistics() {
        const response = await fetch(`${this.apiBase}/statistics`);
        this.statistics = await response.json();
    }

    async loadTransactions(filters = {}) {
        const params = new URLSearchParams(filters);
        const response = await fetch(`${this.apiBase}/transactions?${params}`);
        this.transactions = await response.json();
    }

    updateDashboard() {
        this.updateStatCards();
        this.updateCharts();
        this.updateTransactionTable();
        this.populateTypeFilter();
    }

    updateStatCards() {
        const { overall } = this.statistics;
        
        document.getElementById('totalTransactions').textContent = 
            overall.total_transactions?.toLocaleString() || '0';
        
        document.getElementById('totalAmount').textContent = 
            `${(overall.total_amount || 0).toLocaleString()} RWF`;
        
        document.getElementById('avgAmount').textContent = 
            `${Math.round(overall.avg_amount || 0).toLocaleString()} RWF`;
        
        document.getElementById('maxAmount').textContent = 
            `${(overall.max_amount || 0).toLocaleString()} RWF`;
    }

    updateCharts() {
        this.createTypeChart();
        this.createMonthlyChart();
    }

    createTypeChart() {
        const ctx = document.getElementById('typeChart').getContext('2d');
        
        if (this.charts.typeChart) {
            this.charts.typeChart.destroy();
        }

        const typeData = this.statistics.by_type || [];
        const colors = [
            '#FFCB05', '#FFA500', '#FF8C00', '#FFD700',
            '#1a1a1a', '#333333', '#666666', '#999999'
        ];

        this.charts.typeChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: typeData.map(item => item.transaction_type),
                datasets: [{
                    data: typeData.map(item => item.count),
                    backgroundColor: colors.slice(0, typeData.length),
                    borderWidth: 2,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 20,
                            usePointStyle: true
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.parsed;
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((value / total) * 100).toFixed(1);
                                return `${label}: ${value} (${percentage}%)`;
                            }
                        }
                    }
                }
            }
        });
    }

    createMonthlyChart() {
        const ctx = document.getElementById('monthlyChart').getContext('2d');
        
        if (this.charts.monthlyChart) {
            this.charts.monthlyChart.destroy();
        }

        const monthlyData = this.statistics.by_month || [];

        this.charts.monthlyChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: monthlyData.map(item => item.month),
                datasets: [{
                    label: 'Transaction Count',
                    data: monthlyData.map(item => item.count),
                    backgroundColor: 'rgba(255, 203, 5, 0.8)',
                    borderColor: 'rgba(255, 203, 5, 1)',
                    borderWidth: 2,
                    yAxisID: 'y'
                }, {
                    label: 'Total Amount (RWF)',
                    data: monthlyData.map(item => item.total_amount),
                    type: 'line',
                    borderColor: 'rgba(26, 26, 26, 1)',
                    backgroundColor: 'rgba(26, 26, 26, 0.1)',
                    borderWidth: 3,
                    fill: false,
                    yAxisID: 'y1'
                }]
            },
            options: {
                responsive: true,
                interaction: {
                    mode: 'index',
                    intersect: false,
                },
                scales: {
                    x: {
                        display: true,
                        title: {
                            display: true,
                            text: 'Month'
                        }
                    },
                    y: {
                        type: 'linear',
                        display: true,
                        position: 'left',
                        title: {
                            display: true,
                            text: 'Transaction Count'
                        }
                    },
                    y1: {
                        type: 'linear',
                        display: true,
                        position: 'right',
                        title: {
                            display: true,
                            text: 'Amount (RWF)'
                        },
                        grid: {
                            drawOnChartArea: false,
                        },
                    }
                },
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    }
                }
            }
        });
    }

    updateTransactionTable() {
        const tbody = document.getElementById('transactionsBody');
        tbody.innerHTML = '';

        this.transactions.forEach(transaction => {
            const row = document.createElement('tr');
            
            const typeClass = this.getTypeClass(transaction.transaction_type);
            const formattedDate = this.formatDate(transaction.date_time);
            const details = this.getTransactionDetails(transaction);

            row.innerHTML = `
                <td>${formattedDate}</td>
                <td><span class="transaction-type ${typeClass}">${transaction.transaction_type}</span></td>
                <td class="amount">${(transaction.amount || 0).toLocaleString()} RWF</td>
                <td>${details}</td>
                <td><button class="view-btn" onclick="dashboard.showTransactionDetail(${transaction.id})">View</button></td>
            `;
            
            tbody.appendChild(row);
        });
    }

    getTypeClass(type) {
        const typeMap = {
            'Incoming Money': 'type-incoming',
            'Payment to Code Holder': 'type-payment',
            'Transfer to Mobile Number': 'type-transfer',
            'Bank Deposit': 'type-deposit',
            'Airtime Bill Payment': 'type-payment',
            'Cash Power Bill Payment': 'type-payment',
            'Third Party Transaction': 'type-third-party',
            'Agent Withdrawal': 'type-withdrawal',
            'Bank Transfer': 'type-transfer',
            'Internet/Voice Bundle Purchase': 'type-bundle'
        };
        return typeMap[type] || 'type-payment';
    }

    formatDate(dateString) {
        if (!dateString) return 'N/A';
        const date = new Date(dateString);
        return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
    }

    getTransactionDetails(transaction) {
        if (transaction.sender) return `From: ${transaction.sender}`;
        if (transaction.recipient) return `To: ${transaction.recipient}`;
        if (transaction.phone_number) return `To: ${transaction.phone_number}`;
        if (transaction.bank_name) return `Bank: ${transaction.bank_name}`;
        if (transaction.agent_name) return `Agent: ${transaction.agent_name}`;
        if (transaction.bundle_type) return `${transaction.bundle_type}: ${transaction.bundle_size || 'N/A'}`;
        return 'N/A';
    }

    populateTypeFilter() {
        const select = document.getElementById('typeFilter');
        const types = [...new Set(this.transactions.map(t => t.transaction_type))];
        
        select.innerHTML = '<option value="">All Transaction Types</option>';
        types.forEach(type => {
            const option = document.createElement('option');
            option.value = type;
            option.textContent = type;
            select.appendChild(option);
        });
    }

    setupEventListeners() {
        document.getElementById('searchInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.searchTransactions();
            }
        });
    }

    async searchTransactions() {
        const searchTerm = document.getElementById('searchInput').value.trim();
        if (!searchTerm) {
            await this.loadTransactions();
            this.updateTransactionTable();
            return;
        }

        this.showLoading();
        try {
            const response = await fetch(`${this.apiBase}/search?q=${encodeURIComponent(searchTerm)}`);
            this.transactions = await response.json();
            this.updateTransactionTable();
        } catch (error) {
            console.error('Search error:', error);
            this.showError('Search failed');
        }
        this.hideLoading();
    }

    async applyFilters() {
        const filters = {
            type: document.getElementById('typeFilter').value,
            start_date: document.getElementById('startDate').value,
            end_date: document.getElementById('endDate').value,
            min_amount: document.getElementById('minAmount').value,
            max_amount: document.getElementById('maxAmount').value
        };

        // Remove empty filters
        Object.keys(filters).forEach(key => {
            if (!filters[key]) delete filters[key];
        });

        this.showLoading();
        await this.loadTransactions(filters);
        this.updateTransactionTable();
        this.hideLoading();
    }

    clearFilters() {
        document.getElementById('typeFilter').value = '';
        document.getElementById('startDate').value = '';
        document.getElementById('endDate').value = '';
        document.getElementById('minAmount').value = '';
        document.getElementById('maxAmount').value = '';
        document.getElementById('searchInput').value = '';
        
        this.loadTransactions().then(() => {
            this.updateTransactionTable();
        });
    }

    async showTransactionDetail(transactionId) {
        try {
            const response = await fetch(`${this.apiBase}/transaction/${transactionId}`);
            const transaction = await response.json();
            
            if (transaction.error) {
                this.showError('Transaction not found');
                return;
            }

            this.displayTransactionDetail(transaction);
        } catch (error) {
            console.error('Error loading transaction detail:', error);
            this.showError('Failed to load transaction details');
        }
    }

    displayTransactionDetail(transaction) {
        const detailsDiv = document.getElementById('transactionDetails');
        
        const fields = [
            { label: 'Transaction ID', value: transaction.transaction_id },
            { label: 'Type', value: transaction.transaction_type },
            { label: 'Amount', value: `${(transaction.amount || 0).toLocaleString()} RWF` },
            { label: 'Fee', value: `${(transaction.fee || 0).toLocaleString()} RWF` },
            { label: 'Date & Time', value: this.formatDate(transaction.date_time) },
            { label: 'Sender', value: transaction.sender },
            { label: 'Recipient', value: transaction.recipient },
            { label: 'Phone Number', value: transaction.phone_number },
            { label: 'Agent Name', value: transaction.agent_name },
            { label: 'Agent Phone', value: transaction.agent_phone },
            { label: 'Bank Name', value: transaction.bank_name },
            { label: 'Reference', value: transaction.reference },
            { label: 'Meter Number', value: transaction.meter_number },
            { label: 'Bundle Type', value: transaction.bundle_type },
            { label: 'Bundle Size', value: transaction.bundle_size },
            { label: 'Validity Period', value: transaction.validity_period },
            { label: 'Raw Message', value: transaction.raw_message }
        ];

        detailsDiv.innerHTML = fields
            .filter(field => field.value)
            .map(field => `
                <div class="detail-item">
                    <span class="detail-label">${field.label}:</span>
                    <span class="detail-value">${field.value}</span>
                </div>
            `).join('');

        document.getElementById('detailModal').style.display = 'block';
    }

    showError(message) {
        alert(message); // Simple error handling - could be improved with a proper notification system
    }
}

// Global functions for HTML onclick handlers
function searchTransactions() {
    dashboard.searchTransactions();
}

function applyFilters() {
    dashboard.applyFilters();
}

function clearFilters() {
    dashboard.clearFilters();
}

function closeModal() {
    document.getElementById('detailModal').style.display = 'none';
}

// Initialize dashboard when page loads
let dashboard;
document.addEventListener('DOMContentLoaded', () => {
    dashboard = new MoMoDashboard();
});

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('detailModal');
    if (event.target === modal) {
        modal.style.display = 'none';
    }
}