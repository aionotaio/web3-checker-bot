let currentPage = 1;
let totalPages = 1;
let currentFilters = {};


function showSection(sectionId) {
    document.querySelectorAll('main section').forEach(section => {
        section.classList.remove('active-section');
    });
    document.getElementById(sectionId).classList.add('active-section');
}

async function fetchData(url, method, body = null) {
    try {
        const options = { 
            method,
            credentials: 'include'
        };

        if (body) {
            options.body = JSON.stringify(body);
            options.headers = { 'Content-Type': 'application/json' };
        }
                
        const response = await fetch(url, options);
                
        if (response.status === 204) {
            return { success: true };
        }
                
        const data = await response.json();
                
        if (!response.ok) {
            throw new Error(data.detail || `Error: ${response.status}`);
        }
        
        const totalCount = response.headers.get('X-Total-Count');
        
        return { 
            success: true, 
            data: Array.isArray(data) ? data : data.items || data,
            total: totalCount ? parseInt(totalCount) : null
        };
    } catch (error) {
        console.error('Error:', error);
        return { success: false, error: error.message };
    }
}

async function sendCommand(url, method) {
    const command = url.split('/').pop();
    const commandNames = {
        'start': '<Start>',
        'stop': '<Stop>',
        'restart': '<Restart>'
    };
            
    const result = await fetchData(url, method);
            
    if (result.success) {
        showAlert(`Command ${commandNames[command]} was successful!`, 'success');
    } else {
        showAlert(`Command ${commandNames[command]} was unsuccessful: ${result.error}`, 'error');
    }
}

async function broadcastMessage() {
    const message = document.getElementById('broadcast-message').value.trim();
    const resultBox = document.getElementById('broadcast-result');
            
    resultBox.innerHTML = '';
            
    if (!message) {
        showAlert('Enter a message', 'error', 'broadcast-result');
        return;
    }
            
    const loader = document.createElement('div');
    loader.className = 'loader';
    resultBox.appendChild(loader);
            
    const result = await fetchData('/api/bot/notify', 'POST', { message });
            
    resultBox.innerHTML = '';
            
    if (result.success) {
        showAlert('Message successfully sent to all users!', 'success', 'broadcast-result');
        document.getElementById('broadcast-message').value = '';
    } else {
        showAlert(`Error: ${result.error}`, 'error', 'broadcast-result');
    }
}

async function sendUserMessage() {
    const userId = document.getElementById('user-id').value.trim();
    const message = document.getElementById('user-message').value.trim();
    const resultBox = document.getElementById('user-message-result');
            
    resultBox.innerHTML = '';
            
    if (!userId || !message) {
        showAlert('Please fill all fields', 'error', 'user-message-result');
        return;
    }
            
    const loader = document.createElement('div');
    loader.className = 'loader';
    resultBox.appendChild(loader);
            
    const result = await fetchData(`/api/bot/notify/${userId}`, 'POST', { message });
            
    resultBox.innerHTML = '';
            
    if (result.success) {
        showAlert(`Message successfully sent to user with Telegram ID ${userId}`, 'success', 'user-message-result');
        document.getElementById('user-message').value = '';
    } else {
        showAlert(`Error: ${result.error}`, 'error', 'user-message-result');
    }
}

async function getUser() {
    const userId = document.getElementById('search-user-id').value.trim();
    const resultBox = document.getElementById('user-search-result');
            
    resultBox.innerHTML = '';
            
    if (!userId) {
        showAlert('Enter a valid Telegram ID', 'error', 'user-search-result');
        return;
    }
            
    const loader = document.createElement('div');
    loader.className = 'loader';
    resultBox.appendChild(loader);
            
    const result = await fetchData(`/api/users/${userId}`, 'GET');
            
    resultBox.innerHTML = '';
            
    if (!result.success) {
        showAlert(`Error: ${result.error}`, 'error', 'user-search-result');
        return;
    }
            
    renderUserCard(result.data, resultBox);
}

async function getAllUsers() {
    const resultBox = document.getElementById('user-search-result');  
    resultBox.innerHTML = '';
            
    const loader = document.createElement('div');
    loader.className = 'loader';
    resultBox.appendChild(loader);

    const filters = getCurrentFilters();
    currentFilters = filters;
    
    let url = `/api/users/?page=${currentPage - 1}&size=${filters.size}`;
    if (filters.language) url += `&language_code=${filters.language}`;
    if (filters.is_banned !== undefined) url += `&is_banned=${filters.is_banned}`;
    if (filters.is_premium !== undefined) url += `&is_premium=${filters.is_premium}`;

    const result = await fetchData(url, 'GET');
            
    resultBox.innerHTML = '';
            
    if (!result.success) {
        showAlert(`Error: ${result.error}`, 'error', 'user-search-result');
        return;
    }
            
    if (!result.data || result.data.length === 0) {
        resultBox.innerHTML = '<p>No users found</p>';
        return;
    }
    
    updatePagination(result.total);

    const countHeader = document.createElement('h3');
    countHeader.textContent = `Total users: ${result.data.length}`;
    resultBox.appendChild(countHeader);
            
    result.data.forEach(user => {
        renderUserCard(user, resultBox);
    });
}

function getCurrentFilters() {
    const language = document.getElementById('filter-language').value || null;
    const status = document.getElementById('filter-status').value;
    const premium = document.getElementById('filter-premium').value;
    const size = parseInt(document.getElementById('page-size').value);
    
    return {
        language,
        is_banned: status === 'banned' ? true : (status === 'active' ? false : undefined),
        is_premium: premium === 'true' ? true : (premium === 'false' ? false : undefined),
        size
    };
}

function applyFilters() {
    currentPage = 1;
    getAllUsers();
}

function changePage(delta) {
    const newPage = currentPage + delta;
    if (newPage > 0 && newPage <= totalPages) {
        currentPage = newPage;
        getAllUsers();
    }
}

function updatePagination(totalItems) {
    const pageSize = currentFilters.size || 25;
    totalPages = Math.ceil(totalItems / pageSize);
    
    document.getElementById('page-info').textContent = `Page ${currentPage} of ${totalPages}`;
    document.getElementById('prev-page').disabled = currentPage <= 1;
    document.getElementById('next-page').disabled = currentPage >= totalPages;
}

function renderUserCard(user, container) {
    const card = document.createElement('div');
    card.className = 'user-card';
            
    const formatDate = (dateString) => {
        if (!dateString) return 'Unknown';
        const date = new Date(dateString);
        return date.toLocaleString();
    };
            
    let walletsHtml = '';
    if (user.wallets && user.wallets.length > 0) {
        walletsHtml = '<div class="wallet-list"><strong>User wallets:</strong>';
        user.wallets.forEach(wallet => {
            if (wallet) {
                walletsHtml += `<div class="wallet-item">${wallet}</div>`;
            }
        });
        walletsHtml += '</div>';
    }
            
    card.innerHTML = `
        <div class="user-card-header">
            <h4>ID: ${user.telegram_id}</h4>
            <div class="user-status">
                <span class="tag ${user.is_banned ? 'tag-banned' : 'tag-active'}">
                    ${user.is_banned ? 'Banned' : 'Active'}
                </span>
                ${user.is_premium ? '<span class="tag tag-premium">Premium</span>' : ''}
            </div>
        </div>
        <div class="user-card-body">
            <p><strong>Full name:</strong> ${user.full_name || 'Not stated'}</p>
            <p><strong>Username:</strong> @${user.username || 'Not stated'}</p>
            <p><strong>Language code:</strong> ${user.language_code ? user.language_code.toUpperCase() : 'Not stated'}</p>
            <p><strong>Joined at:</strong> ${formatDate(user.joined_at)}</p>
            <p><strong>Last active at:</strong> ${formatDate(user.last_active_at)}</p>
            ${walletsHtml}
        </div>
    `;
            
    container.appendChild(card);
}

async function banUser() {
    const userId = document.getElementById('ban-user-id').value.trim();
    const resultBox = document.getElementById('ban-result');
            
    resultBox.innerHTML = '';
            
    if (!userId) {
        showAlert('Enter a valid Telegram ID', 'error', 'ban-result');
        return;
    }
            
    const loader = document.createElement('div');
    loader.className = 'loader';
    resultBox.appendChild(loader);
            
    const result = await fetchData(`/api/users/${userId}/ban`, 'PATCH');
            
    resultBox.innerHTML = '';
            
    if (!result.success) {
        showAlert(`Error: ${result.error}`, 'error', 'ban-result');
    } else {
        showAlert(`User with Telegram ID ${userId} was successfully banned`, 'success', 'ban-result');
        if (document.getElementById('search-user-id').value.trim() === userId) {
            getUser();
        }
    }
}

async function unbanUser() {
    const userId = document.getElementById('ban-user-id').value.trim();
    const resultBox = document.getElementById('ban-result');
            
    resultBox.innerHTML = '';
            
    if (!userId) {
        showAlert('Enter a valid Telegram ID', 'error', 'ban-result');
        return;
    }
            
    const loader = document.createElement('div');
    loader.className = 'loader';
    resultBox.appendChild(loader);
            
    const result = await fetchData(`/api/users/${userId}/unban`, 'PATCH');
            
    resultBox.innerHTML = '';
            
    if (!result.success) {
        showAlert(`Error: ${result.error}`, 'error', 'ban-result');
    } else {
        showAlert(`User with Telegram ID ${userId} was successfully unbanned`, 'success', 'ban-result');
        if (document.getElementById('search-user-id').value.trim() === userId) {
            getUser();
        }
    }
}

async function loadStats(type) {
    let url = '/api/stats/';
    if (type === 'activity') url += 'activity';
    if (type === 'languages') url += 'languages';
            
    const container = document.getElementById('stats-results');
    container.innerHTML = '';
            
    const loader = document.createElement('div');
    loader.className = 'loader';
    container.appendChild(loader);
            
    const result = await fetchData(url, 'GET');
            
    container.innerHTML = '';
            
    if (!result.success) {
        showAlert(`Error: ${result.error}`, 'error', 'stats-results');
        return;
    }
            
    renderStats(result.data, type, container);
}

function renderStats(data, type, container) {
    const formatDate = (dateString) => {
        if (!dateString) return 'Unknown';
        const date = new Date(dateString);
        return date.toLocaleString();
    };

    if (type === 'general') {
        container.innerHTML = `
            <h3>Total Stats</h3>
            <div class="stats-grid">
                <div class="stat-card">
                    <h4>Total users</h4>
                    <p><strong>${data.total_users || 0}</strong></p>
                </div>
                <div class="stat-card">
                    <h4>Banned users</h4>
                    <p><strong>${data.banned_users || 0}</strong></p>
                </div>
                <div class="stat-card">
                    <h4>Premium users</h4>
                    <p><strong>${data.premium_users || 0}</strong></p>
                </div>
            </div>
            <h3 style="margin-top: 20px;">Activity Stats</h3>
            <div class="stats-grid">
                ${Object.entries(data.active_stats.active_users || {}).map(([period, count]) => `
                    <div class="stat-card">
                        <h4>Active for last ${period.replace('_', ' ')}</h4>
                        <p><strong>${count}</strong></p>
                    </div>
                `).join('')}
            </div>
            <div class="stats-grid" style="margin-top: 15px;">
                <div class="stat-card">
                    <h4>First user joined at</h4>
                    <p>${formatDate(data.active_stats.first_user_joined_at)}</p>
                </div>
                <div class="stat-card">
                    <h4>Last user activity at</h4>
                    <p>${formatDate(data.active_stats.last_user_active_at)}</p>
                </div>
            </div>
            <h3 style="margin-top: 20px;">Language Stats</h3>
            <div class="stats-grid">
                ${Object.entries(data.language_stats.languages || {}).map(([lang, count]) => `
                    <div class="stat-card">
                        <h4>${lang.toUpperCase()}</h4>
                        <p><strong>${count}</strong> users</p>
                    </div>
                `).join('')}
            </div>
        `;
    } else if (type === 'activity') {
        container.innerHTML = `
            <h3>Activity Stats</h3>
            <div class="stats-grid">
                ${Object.entries(data.active_users || {}).map(([period, count]) => `
                    <div class="stat-card">
                        <h4>Active for last ${period.replace('_', ' ')}</h4>
                        <p><strong>${count}</strong></p>
                    </div>
                `).join('')}
            </div>
            <div class="stats-grid" style="margin-top: 15px;">
                <div class="stat-card">
                    <h4>First user joined at</h4>
                    <p>${formatDate(data.first_user_joined_at)}</p>
                </div>
                <div class="stat-card">
                    <h4>Last user activity at</h4>
                    <p>${formatDate(data.last_user_active_at)}</p>
                </div>
            </div>
        `;
    } else if (type === 'languages') {
        container.innerHTML = `
            <h3>Language Stats</h3>
            <div class="stats-grid">
                ${Object.entries(data.languages || {}).map(([lang, count]) => `
                    <div class="stat-card">
                        <h4>${lang.toUpperCase()}</h4>
                        <p><strong>${count}</strong> users</p>
                    </div>
                `).join('')}
            </div>
        `;
    }
}

function showGlobalAlert(message, type) {
    const alertContainer = document.createElement('div');
    alertContainer.className = `alert ${type} global-alert`;
    alertContainer.textContent = message;
    document.body.appendChild(alertContainer);

    setTimeout(() => {
        alertContainer.style.opacity = '0';
        setTimeout(() => alertContainer.remove(), 300);
    }, 5000);
}

function showAlert(message, type, containerId = null) {
    if (containerId) {
        const container = document.getElementById(containerId);
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert ${type}`;
        alertDiv.textContent = message;
        container.appendChild(alertDiv);

        setTimeout(() => {
            alertDiv.style.opacity = '0';
            setTimeout(() => alertDiv.remove(), 300);
        }, 5000);
    } else {
        showGlobalAlert(message, type);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    showSection('bot-control');
});
