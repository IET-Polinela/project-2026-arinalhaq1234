const { defineConfig } = require("@playwright/test");
const fs = require("fs");
const path = require("path");

const envPath = path.join(__dirname, ".env");

if (fs.existsSync(envPath)) {
    for (const line of fs.readFileSync(envPath, "utf8").split(/\r?\n/)) {
        const trimmedLine = line.trim();

        if (!trimmedLine || trimmedLine.startsWith("#")) {
            continue;
        }

        const separatorIndex = trimmedLine.indexOf("=");

        if (separatorIndex === -1) {
            continue;
        }

        const key = trimmedLine.slice(0, separatorIndex).trim();
        const value = trimmedLine.slice(separatorIndex + 1).trim();

        if (!(key in process.env)) {
            process.env[key] = value;
        }
    }
}

module.exports = defineConfig({
    testDir: "./tests/e2e",
    fullyParallel: false,
    workers: 1,
    reporter: [
        ["list"],
        [
            "html",
            {
                outputFolder: "playwright-report",
                open: "never",
            },
        ],
    ],
    use: {
        browserName: "chromium",
        headless: true,
        screenshot: "only-on-failure",
        trace: "retain-on-failure",
    },
});
