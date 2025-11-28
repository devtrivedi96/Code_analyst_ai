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

  // Display AI Review
  const reviewResult = document.getElementById("reviewResult");
  const review = data.ai_review;
  let suggestionsHtml = "";
  if (review.suggestions && review.suggestions.length > 0) {
    suggestionsHtml = `
            <div style="margin-top: 10px;">
                <strong style="color: #333;">Suggestions:</strong>
                <ul class="suggestions-list">
                    ${review.suggestions
                      .map((s) => `<li>${escapeHtml(s)}</li>`)
                      .join("")}
                </ul>
            </div>
        `;
  }

  reviewResult.innerHTML = `
        <div class="metric"><span class="metric-label">Summary:</span></div>
        <div style="padding: 8px; background: white; border-radius: 4px; margin: 8px 0; color: #555; line-height: 1.5;">${escapeHtml(
          review.summary
        )}</div>
        ${suggestionsHtml}
        <div class="metric" style="margin-top: 10px;"><span class="metric-label">Severity:</span> <span class="metric-value">${escapeHtml(
          review.severity
        )}</span></div>
        <div class="metric"><span class="metric-label">Model:</span> <span class="metric-value">${escapeHtml(
          review.model_used
        )}</span></div>
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
});
