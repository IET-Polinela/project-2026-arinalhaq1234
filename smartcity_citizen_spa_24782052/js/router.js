const routes = {
    login: `
        <div class="card page-card login-card">
            <div class="card-body p-4">
                <div class="text-center mb-4">
                    <i class="bi bi-shield-lock-fill text-primary fs-1"></i>

                    <h3 class="fw-bold mt-3">
                        Login Citizen
                    </h3>

                    <p class="text-muted mb-0">
                        Masuk menggunakan akun Citizen yang sudah terdaftar.
                    </p>
                </div>

                <div id="loginMessage"></div>

                <form id="loginForm">
                    <div class="mb-3">
                        <label class="form-label fw-semibold">
                            Username
                        </label>

                        <input
                            type="text"
                            id="loginUsername"
                            class="form-control"
                            placeholder="Masukkan username"
                            required
                        >
                    </div>

                    <div class="mb-4">
                        <label class="form-label fw-semibold">
                            Password
                        </label>

                        <input
                            type="password"
                            id="loginPassword"
                            class="form-control"
                            placeholder="Masukkan password"
                            required
                        >
                    </div>

                    <button
                        type="submit"
                        class="btn btn-primary w-100"
                    >
                        <i class="bi bi-box-arrow-in-right me-2"></i>
                        Login
                    </button>
                </form>
            </div>
        </div>
    `,

    dashboard: `
        <div class="row g-4">
            <aside class="col-12 col-lg-3">
                <div class="card page-card dashboard-card sticky-panel">
                    <div class="card-body">
                        <h5 class="fw-bold mb-1">
                            <i class="bi bi-bar-chart-fill me-2 text-primary"></i>
                            Rekap Status
                        </h5>

                        <p class="text-muted small mb-3">
                            Ringkasan laporan milik akun login.
                        </p>

                        <div class="list-group">
                            <div class="list-group-item d-flex justify-content-between">
                                <span>Draft</span>

                                <span
                                    id="draftCount"
                                    class="badge text-bg-secondary rounded-pill"
                                >
                                    0
                                </span>
                            </div>

                            <div class="list-group-item d-flex justify-content-between">
                                <span>Diproses</span>

                                <span
                                    id="processCount"
                                    class="badge text-bg-warning rounded-pill"
                                >
                                    0
                                </span>
                            </div>

                            <div class="list-group-item d-flex justify-content-between">
                                <span>Selesai</span>

                                <span
                                    id="resolvedCount"
                                    class="badge text-bg-success rounded-pill"
                                >
                                    0
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            </aside>

            <section class="col-12 col-lg-6">
                <div class="card page-card">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-center gap-3 flex-wrap mb-3">
                            <div>
                                <h4 class="fw-bold mb-1">
                                    Daftar Laporan
                                </h4>

                                <p class="text-muted mb-0">
                                    Pantau laporan pribadi dan Feed Kota.
                                </p>
                            </div>

                            <div class="text-end">
                                <div
                                    id="reportCount"
                                    class="fw-bold fs-3 text-primary"
                                >
                                    0
                                </div>

                                <div class="text-muted small">
                                    Total laporan
                                </div>
                            </div>
                        </div>

                        <div class="d-flex gap-2 flex-wrap mb-4">
                            <button
                                id="myReportsTabBtn"
                                type="button"
                                class="btn btn-primary"
                                onclick="loadDashboardData('my_reports', 1)"
                            >
                                <i class="bi bi-person-lines-fill me-1"></i>
                                Laporan Saya
                            </button>

                            <button
                                id="feedTabBtn"
                                type="button"
                                class="btn btn-outline-primary"
                                onclick="loadDashboardData('feed', 1)"
                            >
                                <i class="bi bi-globe2 me-1"></i>
                                Feed Kota
                            </button>

                            <button
                                type="button"
                                class="btn btn-success ms-auto"
                                onclick="openCreateReportModal()"
                            >
                                <i class="bi bi-plus-circle-fill me-1"></i>
                                Tambah Laporan Baru
                            </button>
                        </div>

                        <div id="reportList"></div>

                        <div
                            id="paginationContainer"
                            class="mt-4"
                        ></div>
                    </div>
                </div>
            </section>

            <aside class="col-12 col-lg-3">
                <div class="card page-card dashboard-card sticky-panel">
                    <div class="card-body">
                        <h5 class="fw-bold">
                            <i class="bi bi-info-circle-fill me-2 text-primary"></i>
                            Informasi
                        </h5>

                        <p class="text-muted">
                            Gunakan tab Laporan Saya untuk melihat laporan pribadi.
                            Gunakan Feed Kota untuk melihat laporan publik warga lain.
                        </p>

                        <div class="alert alert-primary rounded-4 mb-0">
                            <i class="bi bi-lightbulb-fill me-2"></i>
                            Laporan berstatus DRAFT milik kamu masih dapat diedit.
                        </div>
                    </div>
                </div>
            </aside>
        </div>

        <div
            class="modal fade"
            id="reportModal"
            tabindex="-1"
            aria-hidden="true"
        >
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5
                            id="reportModalTitle"
                            class="modal-title"
                        >
                            Tambah Laporan Baru
                        </h5>

                        <button
                            type="button"
                            class="btn-close"
                            data-bs-dismiss="modal"
                        ></button>
                    </div>

                    <div class="modal-body">
                        <form id="reportForm">
                            <div class="mb-3">
                                <label class="form-label fw-semibold">
                                    Judul
                                </label>

                                <input
                                    type="text"
                                    id="reportTitle"
                                    class="form-control"
                                    required
                                >
                            </div>

                            <div class="mb-3">
                                <label class="form-label fw-semibold">
                                    Kategori
                                </label>

                                <input
                                    type="text"
                                    id="reportCategory"
                                    class="form-control"
                                    required
                                >
                            </div>

                            <div class="mb-3">
                                <label class="form-label fw-semibold">
                                    Deskripsi
                                </label>

                                <textarea
                                    id="reportDescription"
                                    class="form-control"
                                    rows="4"
                                    required
                                ></textarea>
                            </div>

                            <div class="mb-3">
                                <label class="form-label fw-semibold">
                                    Lokasi
                                </label>

                                <input
                                    type="text"
                                    id="reportLocation"
                                    class="form-control"
                                    required
                                >
                            </div>
                        </form>
                    </div>

                    <div class="modal-footer">
                        <button
                            type="button"
                            class="btn btn-outline-secondary"
                            data-bs-dismiss="modal"
                        >
                            Batal
                        </button>

                        <button
                            type="button"
                            class="btn btn-warning"
                            onclick="submitReport('DRAFT')"
                        >
                            Simpan Draft
                        </button>

                        <button
                            type="button"
                            class="btn btn-primary"
                            onclick="submitReport('REPORTED')"
                        >
                            Ajukan
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `,
};

function handleRouting() {
    const appContent =
        document.getElementById("app-content");

    const hash =
        window.location.hash.replace("#", "") || "login";

    /*
     * Pengguna yang belum login tidak boleh membuka dashboard.
     * Pengguna diarahkan kembali ke halaman login.
     */
    if (
        !isLoggedIn() &&
        hash !== "login"
    ) {
        window.location.hash = "#login";
        return;
    }

    /*
     * Halaman login tetap boleh dibuka walaupun terdapat token lama.
     * Dengan demikian, pengguna selalu dapat melakukan login ulang.
     */
    appContent.innerHTML =
        routes[hash] || routes.login;

    if (hash === "login") {
        setupLoginForm();
    }

    if (hash === "dashboard") {
        loadDashboardData("my_reports", 1);
    }

    setupLogoutButton();
}

window.addEventListener(
    "hashchange",
    handleRouting
);

window.addEventListener(
    "DOMContentLoaded",
    handleRouting
);