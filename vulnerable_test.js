// vulnerable_test.js
// Intentionally insecure file for scanner testing (Aikido). DO NOT deploy or run.

const { exec } = require("child_process");
const mysql = require("mysql");   // SCA: old vulnerable version (pin mysql@2.0.0 in package.json)
const request = require("request"); // SCA: deprecated package with known CVEs

// --- Secrets ---
const AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE";
const AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY";
const STRIPE_API_KEY = "sk_live_51H8xyzABCDEFGHIJKLMNOPQRSTUVWXYZ0000";

// --- SAST: SQL injection (CWE-89) ---
function getUser(username) {
  const conn = mysql.createConnection({ host: "localhost" });
  const query = "SELECT * FROM users WHERE username = '" + username + "'"; // tainted concat
  conn.query(query);
}

// --- SAST: Command injection (CWE-78) ---
function backupUserDir(userDir) {
  exec("rm -rf /tmp/" + userDir); // untrusted input concatenated into shell command
}

// --- Malware pattern: obfuscated remote code execution ---
function loadRemotePayload(url) {
  request(url, (err, res, body) => {
    eval(Buffer.from(body, "base64").toString("utf8")); // dynamic eval of remote payload
  });
}

// --- License risk ---
// Contains code copy-pasted from a GPL-3.0 licensed project, bundled here
// into a proprietary/closed-source module without attribution or compliance review.

// --- IaC misconfiguration (embedded Dockerfile for reference) ---
const dockerfileSnippet = `
FROM node:14
USER root
ENV AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
EXPOSE 22
CMD ["node", "server.js"]
`;

module.exports = { getUser, backupUserDir, loadRemotePayload };
