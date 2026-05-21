function isLoggedIn() {
    return Boolean(localStorage.getItem("access_token"));
}

function updateNavbarUserInfo() {
    const userDropdownWrapper = document.getElementById("userDropdownWrapper");
    const navbarUsername = document.getElementById("navbarUsername");
    const dropdownUsername = document.getElementById("dropdownUsername");

    if (!userDropdownWrapper || !navbarUsername || !dropdownUsername) {
        return;
    }

    if (isLoggedIn()) {
        const savedUsername = localStorage.getItem("logged_in_username") || "Citizen";
        navbarUsername.textContent = savedUsername;
        dropdownUsername.textContent = savedUsername;
        userDropdownWrapper.classList.remove("d-none");
    } else {
        navbarUsername.textContent = "Citizen";
        dropdownUsername.textContent = "Citizen";
        userDropdownWrapper.classList.add("d-none");
    }
}

function setupLoginForm() {
    const loginForm = document.getElementById("loginForm");

    if (!loginForm) {
        return;
    }

    loginForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const usernameInput = document.getElementById("loginUsername");
        const passwordInput = document.getElementById("loginPassword");
        const loginMessage = document.getElementById("loginMessage");

        const payload = {
            username: usernameInput.value,
            password: passwordInput.value,
        };

        loginMessage.innerHTML = `
            <div class="alert alert-info">
                <i class="bi bi-hourglass-split me-2"></i>Sedang login...
            </div>
        `;

        const result = await requestAPI("/api/token/", "POST", payload);

        if (result.ok && result.status === 200) {
            localStorage.setItem("access_token", result.data.access);
            localStorage.setItem("refresh_token", result.data.refresh);
            localStorage.setItem("logged_in_username", payload.username);

            loginMessage.innerHTML = `
                <div class="alert alert-success">
                    <i class="bi bi-check-circle-fill me-2"></i>Login berhasil.
                </div>
            `;

            updateNavbarUserInfo();
            alert("Login berhasil.");
            window.location.hash = "#dashboard";
            return;
        }

        loginMessage.innerHTML = `
            <div class="alert alert-danger">
                <i class="bi bi-exclamation-triangle-fill me-2"></i>Login gagal. Periksa username dan password.
            </div>
        `;
    });
}

function setupLogoutButton() {
    const logoutBtn = document.getElementById("logoutBtn");

    updateNavbarUserInfo();

    if (!logoutBtn) {
        return;
    }

    logoutBtn.onclick = function () {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        localStorage.removeItem("logged_in_username");

        updateNavbarUserInfo();
        alert("Logout berhasil.");
        window.location.hash = "#login";
        location.reload();
    };
}