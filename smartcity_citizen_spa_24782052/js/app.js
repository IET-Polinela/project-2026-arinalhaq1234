function getStatusBadge(status) {
    if (status === "DRAFT") {
        return `<span class="status-pill status-draft">DRAFT</span>`;
    }

    if (status === "REPORTED") {
        return `<span class="status-pill status-reported">REPORTED</span>`;
    }

    if (status === "VERIFIED") {
        return `<span class="status-pill status-verified">VERIFIED</span>`;
    }

    if (status === "IN_PROGRESS") {
        return `<span class="status-pill status-progress">IN_PROGRESS</span>`;
    }

    if (status === "RESOLVED") {
        return `<span class="status-pill status-resolved">RESOLVED</span>`;
    }

    return `<span class="status-pill status-draft">${status}</span>`;
}

async function loadDashboardData() {
    const reportList = document.getElementById("reportList");
    const reportCount = document.getElementById("reportCount");

    if (!reportList || !reportCount) {
        return;
    }

    reportList.innerHTML = `
        <div class="text-muted">
            <i class="bi bi-hourglass-split me-2"></i>Memuat laporan...
        </div>
    `;

    const result = await requestAPI("/api/report/", "GET");

    if (!result.ok) {
        reportList.innerHTML = `
            <div class="alert alert-danger">
                <i class="bi bi-exclamation-triangle-fill me-2"></i>Gagal mengambil data laporan. Silakan login ulang.
            </div>
        `;
        return;
    }

    const reports = Array.isArray(result.data) ? result.data : [];
    reportCount.textContent = reports.length;

    if (reports.length === 0) {
        reportList.innerHTML = `
            <div class="text-center text-muted py-4">
                <i class="bi bi-inbox-fill fs-1 d-block mb-3"></i>
                Belum ada laporan.
            </div>
        `;
        return;
    }

    reportList.innerHTML = reports.map(report => `
        <div class="border rounded-4 p-3 mb-3 bg-white">
            <div class="d-flex justify-content-between gap-3 flex-wrap">
                <div>
                    <h6 class="fw-bold mb-1">${report.title}</h6>
                    <div class="text-muted small">
                        <i class="bi bi-geo-alt-fill me-1"></i>${report.location}
                    </div>
                </div>
                <div>${getStatusBadge(report.status)}</div>
            </div>

            <p class="mt-3 mb-2">${report.description}</p>

            <div class="small text-muted">
                <i class="bi bi-person-fill-lock me-1"></i>${report.reporter}
            </div>
        </div>
    `).join("");
}

function setupCreateReportForm() {
    const form = document.getElementById("createReportForm");

    if (!form) {
        return;
    }

    form.addEventListener("submit", async function (event) {
        event.preventDefault();

        const payload = {
            title: document.getElementById("reportTitle").value,
            category: document.getElementById("reportCategory").value,
            description: document.getElementById("reportDescription").value,
            location: document.getElementById("reportLocation").value,
            status: "DRAFT",
        };

        const result = await requestAPI("/api/report/", "POST", payload);

        if (result.ok) {
            alert("Laporan berhasil dibuat.");
            form.reset();
            loadDashboardData();
            return;
        }

        alert("Gagal membuat laporan. Pastikan token masih valid dan semua field terisi.");
        console.log(result);
    });
}