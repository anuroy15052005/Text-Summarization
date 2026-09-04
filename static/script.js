const btn = document.getElementById("summarize-btn");
const btnText = document.getElementById("btn-text");
const btnSpinner = document.getElementById("btn-spinner");
const input = document.getElementById("dialogue-input");
const errorMsg = document.getElementById("error-msg");
const resultSection = document.getElementById("result-section");
const resultText = document.getElementById("result-text");

btn.addEventListener("click", async () => {
  const text = input.value.trim();

  errorMsg.classList.add("hidden");
  errorMsg.textContent = "";

  if (!text) {
    errorMsg.textContent = "Enter a dialogue first.";
    errorMsg.classList.remove("hidden");
    return;
  }

  setLoading(true);
  resultSection.classList.add("hidden");

  try {
    const response = await fetch(`/predict?text=${encodeURIComponent(text)}`, {
      method: "POST"
    });

    if (!response.ok) {
      throw new Error(`Request failed (${response.status})`);
    }

    const summary = await response.json();
    resultText.textContent = summary;
    resultSection.classList.remove("hidden");
  } catch (err) {
    errorMsg.textContent = "Couldn't generate a summary. Try again.";
    errorMsg.classList.remove("hidden");
  } finally {
    setLoading(false);
  }
});

function setLoading(isLoading) {
  btn.disabled = isLoading;
  btnText.textContent = isLoading ? "Summarizing..." : "Summarize";
  btnSpinner.classList.toggle("hidden", !isLoading);
}