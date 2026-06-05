function isLoggedIn() {
    return Boolean(localStorage.getItem("access_token"));
}

function updateNavbarUserInfo() {
    const userDropdownWrapper =
        document.getElementById("userDropdownWrapper");

    const dropdownUsername =
        document.getElementById("dropdownUsername");

    const savedUsername =
        localStorage.getItem("logged_in_username") || "Citizen";

    if (dropdownUsername) {
        dropdownUsername.textContent = savedUsername;
    }

    if (!userDropdownWrapper) {
        return;
    }

    if (isLoggedIn()) {
        userDropdownWrapper.classList.remove("d-none");
    } else {
        userDropdownWrapper.classList.add("d-none");
    }
}

function setupLoginForm() {
    const loginForm =
        document.getElementById("loginForm");

    if (!loginForm) {
        return;
    }

    loginForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const usernameInput =
            document.getElementById("loginUsername");

        const passwordInput =
            document.getElementById("loginPassword");

        const loginMessage =
            document.getElementById("loginMessage");

        const payload = {
            username: usernameInput.value.trim(),
            password: passwordInput.value,
        };

        loginMessage.innerHTML = `
            <div class="alert alert-info">
                <i class="bi bi-hourglass-split me-2"></i>
                Sedang login...
            </div>
        `;

        const result = await requestAPI(
            "/api/token/",
            "POST",
            payload
        );

        if (
            result.ok &&
            result.status === 200 &&
            result.data &&
            result.data.access
        ) {
            localStorage.setItem(
                "access_token",
                result.data.access
            );

            localStorage.setItem(
                "refresh_token",
                result.data.refresh || ""
            );

            localStorage.setItem(
                "logged_in_username",
                payload.username
            );

            updateNavbarUserInfo();

            window.location.hash = "#dashboard";

            return;
        }

        loginMessage.innerHTML = `
            <div class="alert alert-danger">
                <i class="bi bi-exclamation-triangle-fill me-2"></i>
                Login gagal. Periksa username, password,
                dan pastikan backend Django sudah berjalan.
            </div>
        `;

        console.log("Login gagal:", result);
    });
}

function setupLogoutButton() {
    const logoutBtn =
        document.getElementById("logoutBtn");

    updateNavbarUserInfo();

    if (!logoutBtn) {
        return;
    }

    logoutBtn.onclick = function () {
        clearLoginSession();

        window.location.hash = "#login";

        window.location.reload();
    };
}