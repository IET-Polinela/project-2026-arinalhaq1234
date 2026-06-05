let currentTab = "my_reports";
let currentPage = 1;
let editingReportId = null;

const PAGE_SIZE = 10;

function extractReports(data) {
    if (Array.isArray(data)) {
        return data;
    }

    if (data && Array.isArray(data.results)) {
        return data.results;
    }

    return [];
}

function getStatusData(status) {
    const statusMap = {
        DRAFT: {
            label: "DRAFT",
            badgeClass: "status-draft",
            progress: 20,
        },

        REPORTED: {
            label: "REPORTED",
            badgeClass: "status-reported",
            progress: 40,
        },

        VERIFIED: {
            label: "VERIFIED",
            badgeClass: "status-verified",
            progress: 60,
        },

        IN_PROGRESS: {
            label: "IN PROGRESS",
            badgeClass: "status-progress",
            progress: 80,
        },

        RESOLVED: {
            label: "RESOLVED",
            badgeClass: "status-resolved",
            progress: 100,
        },
    };

    return statusMap[status] || {
        label: status,
        badgeClass: "status-draft",
        progress: 0,
    };
}

function updateActiveTabButton() {
    const myReportsButton =
        document.getElementById("myReportsTabBtn");

    const feedButton =
        document.getElementById("feedTabBtn");

    if (!myReportsButton || !feedButton) {
        return;
    }

    if (currentTab === "my_reports") {
        myReportsButton.className = "btn btn-primary";
        feedButton.className = "btn btn-outline-primary";
    } else {
        myReportsButton.className = "btn btn-outline-primary";
        feedButton.className = "btn btn-primary";
    }
}

async function loadDashboardData(tab = "my_reports", page = 1) {
    currentTab = tab;
    currentPage = page;

    const reportList =
        document.getElementById("reportList");

    const reportCount =
        document.getElementById("reportCount");

    if (!reportList || !reportCount) {
        return;
    }

    updateActiveTabButton();

    reportList.innerHTML = `
        <div class="text-muted py-3">
            <i class="bi bi-hourglass-split me-2"></i>
            Memuat laporan...
        </div>
    `;

    const result = await requestAPI(
        `/api/report/?tab=${tab}&page=${page}`,
        "GET"
    );

    if (!result.ok) {
        reportList.innerHTML = `
            <div class="alert alert-danger">
                <i class="bi bi-exclamation-triangle-fill me-2"></i>
                Gagal mengambil data laporan.
                Pastikan backend berjalan dan token login masih valid.
            </div>
        `;

        console.log("Gagal memuat laporan:", result);

        return;
    }

    const reports = extractReports(result.data);

    if (
        result.data &&
        typeof result.data.count === "number"
    ) {
        reportCount.textContent = result.data.count;
    } else {
        reportCount.textContent = reports.length;
    }

    renderList(reports);
    renderPagination(result.data);

    await loadSummaryStats();
}

function renderList(reports) {
    const reportList =
        document.getElementById("reportList");

    if (!reportList) {
        return;
    }

    if (reports.length === 0) {
        reportList.innerHTML = `
            <div class="text-center text-muted py-4">
                <i class="bi bi-inbox-fill fs-1 d-block mb-3"></i>
                Belum ada laporan pada tab ini.
            </div>
        `;

        return;
    }

    reportList.innerHTML = reports.map((report) => {
        const statusData =
            getStatusData(report.status);

        const reporterName =
            report.reporter || "Warga Anonim";

        const editButton =
            report.status === "DRAFT" &&
            report.is_owner === true
                ? `
                    <button
                        type="button"
                        class="btn btn-warning btn-sm mt-3"
                        onclick="editDraft(${report.id})"
                    >
                        <i class="bi bi-pencil-square me-1"></i>
                        Edit Draft
                    </button>
                `
                : "";

        return `
            <div class="border rounded-4 p-3 mb-3 bg-white shadow-sm">
                <div class="d-flex justify-content-between gap-3 flex-wrap">
                    <div>
                        <h6 class="fw-bold mb-1">
                            ${report.title}
                        </h6>

                        <div class="text-muted small">
                            <i class="bi bi-geo-alt-fill me-1"></i>
                            ${report.location}
                        </div>
                    </div>

                    <div>
                        <span class="status-pill ${statusData.badgeClass}">
                            ${statusData.label}
                        </span>
                    </div>
                </div>

                <p class="mt-3 mb-2">
                    ${report.description}
                </p>

                <div class="small text-muted mb-3">
                    <i class="bi bi-person-fill-lock me-1"></i>
                    ${reporterName}
                </div>

                <div class="small fw-semibold mb-1">
                    Progress Laporan
                </div>

                <div class="progress">
                    <div
                        class="progress-bar"
                        role="progressbar"
                        style="width: ${statusData.progress}%"
                    >
                        ${statusData.progress}%
                    </div>
                </div>

                ${editButton}
            </div>
        `;
    }).join("");
}

function renderPagination(data) {
    const paginationContainer =
        document.getElementById("paginationContainer");

    if (!paginationContainer) {
        return;
    }

    if (!data || Array.isArray(data)) {
        paginationContainer.innerHTML = "";

        return;
    }

    const totalItems = data.count || 0;

    const totalPages = Math.max(
        1,
        Math.ceil(totalItems / PAGE_SIZE)
    );

    paginationContainer.innerHTML = `
        <nav>
            <ul class="pagination justify-content-center mb-0">
                <li class="page-item ${data.previous ? "" : "disabled"}">
                    <button
                        type="button"
                        class="page-link"
                        onclick="loadDashboardData('${currentTab}', ${currentPage - 1})"
                        ${data.previous ? "" : "disabled"}
                    >
                        Previous
                    </button>
                </li>

                <li class="page-item active">
                    <span class="page-link">
                        Halaman ${currentPage} dari ${totalPages}
                    </span>
                </li>

                <li class="page-item ${data.next ? "" : "disabled"}">
                    <button
                        type="button"
                        class="page-link"
                        onclick="loadDashboardData('${currentTab}', ${currentPage + 1})"
                        ${data.next ? "" : "disabled"}
                    >
                        Next
                    </button>
                </li>
            </ul>
        </nav>
    `;
}

async function loadSummaryStats() {
    const result = await requestAPI(
        "/api/report/?tab=my_reports&page_size=1000",
        "GET"
    );

    if (!result.ok) {
        console.log("Gagal mengambil rekap:", result);

        return;
    }

    const reports = extractReports(result.data);

    const draftCount = reports.filter(
        (report) => report.status === "DRAFT"
    ).length;

    const processCount = reports.filter(
        (report) =>
            report.status === "REPORTED" ||
            report.status === "VERIFIED" ||
            report.status === "IN_PROGRESS"
    ).length;

    const resolvedCount = reports.filter(
        (report) => report.status === "RESOLVED"
    ).length;

    document.getElementById("draftCount").textContent =
        draftCount;

    document.getElementById("processCount").textContent =
        processCount;

    document.getElementById("resolvedCount").textContent =
        resolvedCount;
}

function openCreateReportModal() {
    const modalElement =
        document.getElementById("reportModal");

    const form =
        document.getElementById("reportForm");

    const modalTitle =
        document.getElementById("reportModalTitle");

    if (!modalElement || !form || !modalTitle) {
        window.location.hash = "#dashboard";

        return;
    }

    editingReportId = null;

    form.reset();

    modalTitle.textContent =
        "Tambah Laporan Baru";

    const modal =
        bootstrap.Modal.getOrCreateInstance(
            modalElement
        );

    modal.show();
}

async function editDraft(id) {
    const result = await requestAPI(
        `/api/report/${id}/`,
        "GET"
    );

    if (!result.ok) {
        alert("Draft gagal dibuka.");

        console.log(result);

        return;
    }

    const report = result.data;

    document.getElementById("reportTitle").value =
        report.title || "";

    document.getElementById("reportCategory").value =
        report.category || "";

    document.getElementById("reportDescription").value =
        report.description || "";

    document.getElementById("reportLocation").value =
        report.location || "";

    document.getElementById("reportModalTitle").textContent =
        "Edit Draft Laporan";

    editingReportId = id;

    const modalElement =
        document.getElementById("reportModal");

    const modal =
        bootstrap.Modal.getOrCreateInstance(
            modalElement
        );

    modal.show();
}

async function submitReport(status) {
    const form =
        document.getElementById("reportForm");

    if (!form.reportValidity()) {
        return;
    }

    const payload = {
        title:
            document.getElementById("reportTitle").value,

        category:
            document.getElementById("reportCategory").value,

        description:
            document.getElementById("reportDescription").value,

        location:
            document.getElementById("reportLocation").value,

        status: status,
    };

    const isEditing =
        editingReportId !== null;

    const endpoint = isEditing
        ? `/api/report/${editingReportId}/`
        : "/api/report/";

    const method = isEditing
        ? "PUT"
        : "POST";

    const result = await requestAPI(
        endpoint,
        method,
        payload
    );

    if (
        !result.ok ||
        ![200, 201].includes(result.status)
    ) {
        alert("Laporan gagal disimpan.");

        console.log(result);

        return;
    }

    const modalElement =
        document.getElementById("reportModal");

    const modal =
        bootstrap.Modal.getInstance(
            modalElement
        );

    if (modal) {
        modal.hide();
    }

    form.reset();

    editingReportId = null;

    alert(
        isEditing
            ? "Draft berhasil diperbarui."
            : "Laporan berhasil dibuat."
    );

    await loadDashboardData(
        currentTab,
        currentPage
    );
}