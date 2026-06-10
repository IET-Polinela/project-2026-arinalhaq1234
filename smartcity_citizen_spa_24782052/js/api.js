const API_BASE_URL = "http://103.151.63.86:8005";

function clearLoginSession() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("logged_in_username");
}

async function requestAPI(endpoint, method = "GET", bodyData = null) {
    const accessToken = localStorage.getItem("access_token");

    const headers = {
        "Content-Type": "application/json",
    };

    if (accessToken) {
        headers["Authorization"] = `Bearer ${accessToken}`;
    }

    const options = {
        method: method,
        headers: headers,
    };

    if (bodyData !== null) {
        options.body = JSON.stringify(bodyData);
    }

    try {
        const response = await fetch(
            `${API_BASE_URL}${endpoint}`,
            options
        );

        let data = null;

        const contentType = response.headers.get("content-type");

        if (
            contentType &&
            contentType.includes("application/json")
        ) {
            data = await response.json();
        }

        /*
         * Jika token lama sudah kedaluwarsa, hapus sesi login.
         * Pengecualian diberikan untuk endpoint login agar pesan
         * username atau password salah tetap dapat ditampilkan.
         */
        if (
            response.status === 401 &&
            endpoint !== "/api/token/"
        ) {
            clearLoginSession();

            window.location.hash = "#login";

            setTimeout(() => {
                window.location.reload();
            }, 100);
        }

        return {
            ok: response.ok,
            status: response.status,
            data: data,
        };
    } catch (error) {
        console.error("Backend tidak dapat dihubungi:", error);

        return {
            ok: false,
            status: 0,
            data: null,
        };
    }
}