const API_BASE_URL = "http://localhost:8000"; // Cambia esto si el backend tiene otra URL

document.addEventListener("DOMContentLoaded", () => {
    loadHistory();
});

async function askQuestion() {
    const questionText = document.getElementById("questionInput").value.trim();
    if (!questionText) return;

    try {
        const response = await fetch(`${API_BASE_URL}/questions/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: questionText }),
        });

        if (!response.ok) throw new Error("Error sending question");

        document.getElementById("questionInput").value = "";
        loadHistory();
    } catch (error) {
        console.error("Failed to ask question:", error);
    }
}

async function fetchResponses(questionId) {
    try {
        const response = await fetch(`${API_BASE_URL}/responses/`);
        if (!response.ok) throw new Error("Error fetching responses");

        const responses = await response.json();
        const responseContainer = document.getElementById("responseContainer");
        responseContainer.innerHTML = "<h3>AI Responses:</h3>";

        responses
            .filter(res => res.question_id === questionId)
            .forEach(res => {
                responseContainer.innerHTML += `<p><strong>${res.ai_name}:</strong> ${res.response_text}</p>`;
            });

        fetchSummary(questionId);
        fetchSimilarities(questionId);
    } catch (error) {
        console.error("Failed to fetch responses:", error);
    }
}

async function fetchSummary(questionId) {
    try {
        const response = await fetch(`${API_BASE_URL}/summaries/`);
        if (!response.ok) throw new Error("Error fetching summaries");

        const summaries = await response.json();
        const summary = summaries.find(s => s.question_id === questionId);
        if (summary) {
            document.getElementById("responseContainer").innerHTML += `<h3>Summary:</h3><p>${summary.summary_text}</p>`;
        }
    } catch (error) {
        console.error("Failed to fetch summary:", error);
    }
}

async function fetchSimilarities(questionId) {
    try {
        const response = await fetch(`${API_BASE_URL}/similarities/`);
        if (!response.ok) throw new Error("Error fetching similarities");

        const similarities = await response.json();
        const similarity = similarities.find(s => s.question_id === questionId);
        if (similarity) {
            document.getElementById("responseContainer").innerHTML += `<h3>Similarity Score:</h3><p>${similarity.similarity_score}</p>`;
        }
    } catch (error) {
        console.error("Failed to fetch similarities:", error);
    }
}

async function loadHistory() {
    try {
        const response = await fetch(`${API_BASE_URL}/questions/`);
        if (!response.ok) throw new Error("Error fetching questions");

        const questions = await response.json();
        const historyList = document.getElementById("historyList");
        historyList.innerHTML = "";

        questions
            .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
            .forEach(q => {
                const listItem = document.createElement("li");
                listItem.style.display = "flex";
                listItem.style.justifyContent = "space-between";
                listItem.style.alignItems = "center";
                listItem.style.padding = "10px";
                listItem.style.background = "#f8f9fa";
                listItem.style.borderRadius = "5px";
                listItem.style.marginBottom = "5px";

                const date = new Date(q.created_at);
                const formattedDate = date.toLocaleString();

                const questionText = document.createElement("span");
                questionText.innerHTML = `<strong>${q.text}</strong> <br> <small>${formattedDate}</small>`;
                questionText.style.cursor = "pointer";
                questionText.onclick = () => fetchResponses(q.id);

                const deleteButton = document.createElement("button");
                deleteButton.textContent = "🗑️";
                deleteButton.style.backgroundColor = "red";
                deleteButton.style.color = "white";
                deleteButton.style.border = "none";
                deleteButton.style.padding = "5px 10px";
                deleteButton.style.borderRadius = "5px";
                deleteButton.style.cursor = "pointer";
                deleteButton.onclick = () => deleteQuestion(q.id);

                listItem.appendChild(questionText);
                listItem.appendChild(deleteButton);
                historyList.appendChild(listItem);
            });
    } catch (error) {
        console.error("Failed to load history:", error);
    }
}

async function deleteQuestion(questionId) {
    if (!confirm("Are you sure you want to delete this question and all related data?")) return;

    try {
        const response = await fetch(`${API_BASE_URL}/questions/${questionId}`, {
            method: "DELETE",
        });

        if (!response.ok) throw new Error("Error deleting question");

        loadHistory();
        document.getElementById("responseContainer").innerHTML = "";
    } catch (error) {
        console.error("Failed to delete question:", error);
    }
}
