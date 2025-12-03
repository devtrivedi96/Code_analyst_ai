const codeInput = document.getElementById("codeInput");
const analyzeBtn = document.getElementById("analyzeBtn");
const clearBtn = document.getElementById("clearBtn");
const modelSelect = document.getElementById("model");
const loadingSpinner = document.getElementById("loadingSpinner");
const results = document.getElementById("results");
const errorMessage = document.getElementById("errorMessage");

// Event Listeners
analyzeBtn.addEventListener("click", analyzeCode);
clearBtn.addEventListener("click", clearCode);
codeInput.addEventListener("keydown", (e) => {
  if (e.ctrlKey && e.key === "Enter") {
    analyzeCode();
  }
});

function clearCode() {
  codeInput.value = "";
  results.style.display = "none";
  errorMessage.style.display = "none";
  codeInput.focus();
}

function analyzeCode() {
  const code = codeInput.value.trim();

  if (!code) {
    showError("Please enter some code to analyze");
    return;
  }

  const model = modelSelect.value;

  // Show loading state
  loadingSpinner.style.display = "block";
  results.style.display = "none";
  errorMessage.style.display = "none";
  analyzeBtn.disabled = true;

  // Send request to backend
  fetch("/api/analyze", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ code, model }),
  })
    .then((response) => {
      if (!response.ok) {
        return response.json().then((data) => {
          throw new Error(data.error || "Analysis failed");
        });
      }
      return response.json();
    })
    .then((data) => {
      displayResults(data);
    })
    .catch((error) => {
      showError(error.message);
    })
    .finally(() => {
      loadingSpinner.style.display = "none";
      analyzeBtn.disabled = false;
    });
}

function displayResults(data) {
  results.style.display = "block";
  errorMessage.style.display = "none";

  // Display Syntax Check
  const syntaxResult = document.getElementById("syntaxResult");
  if (data.syntax_valid) {
    syntaxResult.innerHTML = `<div class="metric"><span class="metric-label">Status:</span> <span class="status-pass">✓ Valid</span></div>`;
  } else {
    syntaxResult.innerHTML = `
            <div class="metric"><span class="metric-label">Status:</span> <span class="status-fail">✗ Invalid</span></div>
            ${
              data.syntax_error
                ? `<div class="metric"><span class="metric-label">Error:</span> ${escapeHtml(
                    data.syntax_error
                  )}</div>`
                : ""
            }
        `;
  }

  // Display Quality Metrics
  const qualityResult = document.getElementById("qualityResult");
  const quality = data.quality_metrics;
  qualityResult.innerHTML = `
        <div class="metric"><span class="metric-label">Lines of Code:</span> <span class="metric-value">${
          quality.line_count
        }</span></div>
        <div class="metric"><span class="metric-label">McCabe Complexity:</span> <span class="metric-value">${
          quality.mccabe_complexity
        }</span></div>
        <div class="metric"><span class="metric-label">Complexity Level:</span> <span class="metric-value">${getComplexityLevel(
          quality.mccabe_complexity
        )}</span></div>
    `;

  // Display Logic Analysis
  const logicResult = document.getElementById("logicResult");
  const logicAnalysis = data.logic_analysis || {};
  if (logicAnalysis.total_issues > 0) {
    let issuesHtml = `<div class="metric"><span class="metric-label">Total Issues:</span> <span class="metric-value">${logicAnalysis.total_issues}</span></div>`;
    if (logicAnalysis.severity_count) {
      issuesHtml += `
        <div class="metric"><span class="metric-label">Critical:</span> <span class="metric-value">${
          logicAnalysis.severity_count.Critical || 0
        }</span></div>
        <div class="metric"><span class="metric-label">Major:</span> <span class="metric-value">${
          logicAnalysis.severity_count.Major || 0
        }</span></div>
        <div class="metric"><span class="metric-label">Minor:</span> <span class="metric-value">${
          logicAnalysis.severity_count.Minor || 0
        }</span></div>
      `;
    }
    if (logicAnalysis.issues && logicAnalysis.issues.length > 0) {
      issuesHtml +=
        '<div style="margin-top: 10px;"><strong>Issues Found:</strong><ul class="suggestions-list">';
      logicAnalysis.issues.slice(0, 5).forEach((issue) => {
        const severity = issue.severity === "Major" ? "⚠️" : "ℹ️";
        issuesHtml += `<li>${severity} [Line ${issue.line}] ${escapeHtml(
          issue.message
        )}<br><small style="color: #999;">→ ${escapeHtml(
          issue.suggestion
        )}</small></li>`;
      });
      if (logicAnalysis.issues.length > 5) {
        issuesHtml += `<li>... and ${
          logicAnalysis.issues.length - 5
        } more issues</li>`;
      }
      issuesHtml += "</ul></div>";
    }
    logicResult.innerHTML = issuesHtml;
  } else {
    logicResult.innerHTML =
      '<div class="metric"><span class="status-pass">✓ No logic issues found!</span></div>';
  }

  // Display Best Practices
  const practicesResult = document.getElementById("practicesResult");
  const practices = data.best_practices || {};
  let practicesHtml = "";
  let issueCount = 0;

  if (practices.pep8_violations && practices.pep8_violations.length > 0) {
    issueCount += practices.pep8_violations.length;
    practicesHtml += `<div><strong>PEP 8 Violations (${practices.pep8_violations.length}):</strong>`;
    practicesHtml += practices.pep8_violations
      .slice(0, 3)
      .map(
        (v) =>
          `<div style="margin: 5px 0; padding: 5px; background: #fff3cd; border-radius: 3px; font-size: 13px;">
          Line ${v.line}: ${escapeHtml(v.issue)}<br><small>→ ${escapeHtml(
            v.suggestion
          )}</small>
      </div>`
      )
      .join("");
    if (practices.pep8_violations.length > 3) {
      practicesHtml += `<small>... and ${
        practices.pep8_violations.length - 3
      } more</small>`;
    }
    practicesHtml += "</div>";
  }

  if (practices.security_issues && practices.security_issues.length > 0) {
    issueCount += practices.security_issues.length;
    practicesHtml += `<div style="margin-top: 10px;"><strong>🔒 Security Issues (${practices.security_issues.length}):</strong>`;
    practices.security_issues.forEach((s) => {
      const severity = s.severity === "Critical" ? "🚨" : "⚠️";
      practicesHtml += `<div style="margin: 5px 0; padding: 5px; background: #f8d7da; border-radius: 3px; font-size: 13px;">
          ${severity} ${escapeHtml(s.issue)}<br><small>→ ${escapeHtml(
        s.suggestion
      )}</small>
      </div>`;
    });
    practicesHtml += "</div>";
  }

  if (issueCount === 0) {
    practicesHtml =
      '<div class="metric"><span class="status-pass">✓ Code follows best practices!</span></div>';
  }

  practicesResult.innerHTML =
    practicesHtml || '<div class="metric">No practice issues detected</div>';

  // Display AI Review
  const reviewResult = document.getElementById("reviewResult");
  const review = data.ai_review;
  let suggestionsHtml = "";
  if (review.suggestions && review.suggestions.length > 0) {
    suggestionsHtml = `
            <div style="margin-top: 10px;">
                <strong style="color: #333;">💡 Suggestions:</strong>
                <ul class="suggestions-list">
                    ${review.suggestions
                      .map((s) => `<li>${escapeHtml(s)}</li>`)
                      .join("")}
                </ul>
            </div>
        `;
  }

  let issuesHtml = "";
  if (review.issues && review.issues !== "No issues found") {
    // If issues is a string, render directly
    if (typeof review.issues === "string") {
      issuesHtml = `
            <div style="margin-top: 10px; padding: 10px; background: #f8d7da; border-left: 4px solid #721c24; border-radius: 4px;">
                <strong style="color: #721c24;">⚠️ Issues:</strong>
                <div style="color: #721c24; margin-top: 5px;">${escapeHtml(
                  review.issues
                )}</div>
            </div>
        `;
    } else if (Array.isArray(review.issues)) {
      // Array of issues
      issuesHtml = `<div style="margin-top: 10px;"><strong style="color: #721c24;">⚠️ Issues:</strong><ul class="suggestions-list">`;
      review.issues.forEach((it) => {
        issuesHtml += `<li>${escapeHtml(
          typeof it === "string" ? it : JSON.stringify(it)
        )}</li>`;
      });
      issuesHtml += `</ul></div>`;
    } else if (typeof review.issues === "object") {
      // Object: probably a mapping of model -> analysis
      issuesHtml = `<div style="margin-top: 10px; padding: 10px; background: #f8d7da; border-left: 4px solid #721c24; border-radius: 4px;"><strong style="color: #721c24;">⚠️ Issues (per model):</strong>`;
      Object.entries(review.issues).forEach(([k, v]) => {
        let rendered = "";
        if (typeof v === "string") rendered = escapeHtml(v);
        else
          try {
            rendered = escapeHtml(JSON.stringify(v, null, 2));
          } catch (e) {
            rendered = escapeHtml(String(v));
          }
        issuesHtml += `<div style="margin-top:8px;"><strong>${escapeHtml(
          k
        )}:</strong><pre style="white-space:pre-wrap; font-size:13px; background:#fff; padding:6px; border-radius:4px;">${rendered}</pre></div>`;
      });
      issuesHtml += `</div>`;
    }
  }

  let ratingHtml = "";
  if (review.quality_rating && review.quality_rating !== "N/A") {
    ratingHtml = `<div class="metric"><span class="metric-label">Quality Rating:</span> <span class="metric-value">${escapeHtml(
      review.quality_rating
    )}</span></div>`;
  }

  let recommendationHtml = "";
  if (review.recommendation) {
    recommendationHtml = `
            <div style="margin-top: 10px; padding: 10px; background: #d1ecf1; border-left: 4px solid #0c5460; border-radius: 4px;">
                <strong style="color: #0c5460;">💬 Recommendation:</strong>
                <div style="color: #0c5460; margin-top: 5px;">${escapeHtml(
                  review.recommendation
                )}</div>
            </div>
        `;
  }

  reviewResult.innerHTML = `
        <div class="metric"><span class="metric-label">Model:</span> <span class="metric-value">${escapeHtml(
          review.model_used || "AI Model"
        )}</span></div>
        <div style="padding: 10px; background: #e7f3ff; border-left: 4px solid #0066cc; border-radius: 4px; margin: 10px 0;">
            <strong style="color: #004085;">📝 Summary:</strong>
            <div style="color: #004085; margin-top: 5px; line-height: 1.6;">${escapeHtml(
              review.summary
            )}</div>
        </div>
        ${suggestionsHtml}
        ${issuesHtml}
        ${ratingHtml}
        ${recommendationHtml}
    `;
}

function showError(message) {
  errorMessage.textContent = "❌ Error: " + message;
  errorMessage.style.display = "block";
  results.style.display = "none";
}

function getComplexityLevel(complexity) {
  if (complexity <= 1) return "Very Simple";
  if (complexity <= 5) return "Simple";
  if (complexity <= 10) return "Moderate";
  if (complexity <= 20) return "Complex";
  return "Very Complex";
}

function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

// Focus on code input on page load
window.addEventListener("load", () => {
  codeInput.focus();
  loadAvailableModels();
});

// Fetch available models from backend and populate model select
function loadAvailableModels() {
  fetch("/api/models")
    .then((res) => {
      if (!res.ok) return res.json().then((d) => Promise.reject(d));
      return res.json();
    })
    .then((data) => {
      // Clear existing options
      while (modelSelect.firstChild)
        modelSelect.removeChild(modelSelect.firstChild);

      // Add cloud models first
      if (data.cloud_models && data.cloud_models.length) {
        data.cloud_models.forEach((m) => {
          const opt = document.createElement("option");
          opt.value = m.id;
          opt.textContent = m.name;
          modelSelect.appendChild(opt);
        });
      }

      // Add a separator / optgroup for custom models if present
      if (data.custom_models && data.custom_models.length) {
        const sep = document.createElement("option");
        sep.textContent = "--- Custom / Local Models ---";
        sep.disabled = true;
        modelSelect.appendChild(sep);

        data.custom_models.forEach((m) => {
          const opt = document.createElement("option");
          opt.value = m.id;
          // Show API/link info inline so users know if the model exposes an API
          const apiNote = m.api
            ? m.api_endpoint
              ? ` (api: ${m.api_endpoint})`
              : ` (api: ${m.link})`
            : " (no API)";
          opt.textContent = `${m.name}${apiNote}`;
          modelSelect.appendChild(opt);
        });
      }
    })
    .catch((err) => {
      console.warn("Could not load models:", err);
      // leave defaults if any
    });
}
