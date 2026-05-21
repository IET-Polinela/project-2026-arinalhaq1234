const routes = {
    login: `
        <div class="card page-card login-card">
            <div class="card-body p-4">
                <div class="text-center mb-4">
                    <i class="bi bi-shield-lock-fill text-primary fs-1"></i>
                    <h3 class="fw-bold mt-3">Login Citizen</h3>
                    <p class="text-muted mb-0">Masuk menggunakan akun Citizen yang sudah terdaftar.</p>
                </div>

                <div id="loginMessage"></div>

                <form id="loginForm">
                    <div class="mb-3">
                        <label class="form-label fw-semibold">Username</label>
                        <input type="text" id="loginUsername" class="form-control" placeholder="Masukkan username" required>
                    </div>

                    <div class="mb-4">
                        <label class="form-label fw-semibold">Password</label>
                        <input type="password" id="loginPassword" class="form-control" placeholder="Masukkan password" required>
                    </div>

                    <button type="submit" class="btn btn-primary w-100">
                        <i class="bi bi-box-arrow-in-right me-2"></i>Login
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
                        <h5 class="fw-bold">
                            <i class="bi bi-person-circle me-2 text-primary"></i>Citizen Menu
                        </h5>
                        <p class="text-muted small mb-3">Portal pelaporan masyarakat.</p>

                        <div class="d-grid gap-2">
                            <a href="#dashboard" class="btn btn-primary">
                                <i class="bi bi-speedometer2 me-2"></i>Dashboard
                            </a>
                            <a href="#create-report" class="btn btn-outline-primary">
                                <i class="bi bi-plus-circle-fill me-2"></i>Buat Laporan
                            </a>
                        </div>
                    </div>
                </div>
            </aside>

            <section class="col-12 col-lg-6">
                <div class="card page-card">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-center gap-3 flex-wrap mb-3">
                            <div>
                                <h4 class="fw-bold mb-1">Daftar Laporan</h4>
                                <p class="text-muted mb-0">Laporan non-DRAFT dan DRAFT milik akun login.</p>
                            </div>

                            <div class="text-end">
                                <div class="fw-bold fs-3 text-primary" id="reportCount">0</div>
                                <div class="text-muted small">Total tampil</div>
                            </div>
                        </div>

                        <div id="reportList"></div>
                    </div>
                </div>
            </section>

            <aside class="col-12 col-lg-3">
                <div class="card page-card dashboard-card sticky-panel">
                    <div class="card-body">
                        <h5 class="fw-bold">
                            <i class="bi bi-info-circle-fill me-2 text-primary"></i>Informasi
                        </h5>
                        <p class="text-muted">
                            Laporan baru akan dibuat sebagai DRAFT. Nama pelapor ditampilkan anonim melalui API.
                        </p>

                        <div class="alert alert-primary rounded-4 mb-0">
                            <i class="bi bi-lightbulb-fill me-2"></i>
                            Gunakan tombol Buat Laporan untuk mengirim laporan baru.
                        </div>
                    </div>
                </div>
            </aside>
        </div>
    `,

    "create-report": `
        <div class="row justify-content-center">
            <div class="col-12 col-lg-7">
                <div class="card page-card">
                    <div class="card-body p-4">
                        <h3 class="fw-bold mb-2">
                            <i class="bi bi-plus-circle-fill text-primary me-2"></i>Buat Laporan
                        </h3>
                        <p class="text-muted mb-4">Isi laporan baru tanpa mengirim field reporter.</p>

                        <form id="createReportForm">
                            <div class="mb-3">
                                <label class="form-label fw-semibold">Judul</label>
                                <input type="text" id="reportTitle" class="form-control" placeholder="Contoh: Jalan rusak" required>
                            </div>

                            <div class="mb-3">
                                <label class="form-label fw-semibold">Kategori</label>
                                <input type="text" id="reportCategory" class="form-control" placeholder="Contoh: Infrastruktur" required>
                            </div>

                            <div class="mb-3">
                                <label class="form-label fw-semibold">Deskripsi</label>
                                <textarea id="reportDescription" class="form-control" rows="5" placeholder="Tuliskan detail laporan" required></textarea>
                            </div>

                            <div class="mb-4">
                                <label class="form-label fw-semibold">Lokasi</label>
                                <input type="text" id="reportLocation" class="form-control" placeholder="Contoh: Depok" required>
                            </div>

                            <div class="d-flex justify-content-between gap-3">
                                <a href="#dashboard" class="btn btn-outline-secondary">
                                    <i class="bi bi-arrow-left me-2"></i>Kembali
                                </a>

                                <button type="submit" class="btn btn-primary">
                                    <i class="bi bi-send-fill me-2"></i>Kirim Laporan
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    `,
};

function handleRouting() {
    const appContent = document.getElementById("app-content");
    const hash = window.location.hash.replace("#", "") || "login";

    if (!isLoggedIn() && hash !== "login") {
        window.location.hash = "#login";
        return;
    }

    if (isLoggedIn() && hash === "login") {
        window.location.hash = "#dashboard";
        return;
    }

    appContent.innerHTML = routes[hash] || routes.login;

    if (hash === "login") {
        setupLoginForm();
    }

    if (hash === "dashboard") {
        loadDashboardData();
    }

    if (hash === "create-report") {
        setupCreateReportForm();
    }

    setupLogoutButton();
}

window.addEventListener("hashchange", handleRouting);
window.addEventListener("DOMContentLoaded", handleRouting);