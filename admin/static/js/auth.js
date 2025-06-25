async function login(event) {
    event.preventDefault();

    const form = document.getElementById('login-form');
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    try {
        const response = await fetch('/api/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            const errorData = await response.json();
            displayErrors(errorData);
            return;
        }

        const result = await response.json();

        if (result.access_token) {
            window.location.href = '/dashboard';
        } else {
            alert(result.message || 'Unknown error');
        }
    } catch (error) {
        console.error('Failed to login:', error);
        alert('Failed to login, please try again');
    }
}

async function logout() {
    try {
        const response = await fetch('/api/auth/logout', {
            method: 'POST'
        });
        
        if (response.ok) {
            window.location.href = '/login';
        }
    } catch (error) {
        console.error('Failed to logout:', error);
    }
}

function displayErrors(errorData) {
    if (errorData && errorData.detail) {
        alert(errorData.detail);
    }
}
