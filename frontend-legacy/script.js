const API_BASE_URL = "http://localhost:8000";

console.log('hola');

document.addEventListener("DOMContentLoaded", () => {
    loadHistory();
});
function showLoader() {
    const loader = document.getElementById("loader");
    if (loader) {
        loader.style.display = "block";
    } else {
        console.error("Loader element not found.");
    }
}

function hideLoader() {
    const loader = document.getElementById("loader");
    if (loader) {
        loader.style.display = "none";
    }
}

async function askQuestion() {
    const questionText = document.getElementById("questionInput").value.trim();
    if (!questionText) return;

    showLoader();
    try {
        const response = await fetch(`${API_BASE_URL}/questions/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: questionText }),
        });

        if (!response.ok) throw new Error("Error sending question");

        const data = await response.json();
        document.getElementById("questionInput").value = "";
        displayFullResults(data);
        await loadHistory();
    } catch (error) {
        console.error("Failed to ask question:", error);
    } finally {
        hideLoader();
    }
}

function displayFullResults(data) {
    const container = document.getElementById("responseContainer");
    container.innerHTML = "";

    // Question
    container.innerHTML += `<h3>Question:</h3><p>${data.question}</p>`;

    // Responses
    container.innerHTML += `<h3>AI Responses:</h3>`;
    for (const [ai, text] of Object.entries(data.responses)) {
        container.innerHTML += `<p><strong>${ai}:</strong> ${text}</p>`;
    }

    // Similarities
    container.innerHTML += `<h3>Lexical Similarities:</h3>`;
    for (const [pair, score] of Object.entries(data.similarities)) {
        container.innerHTML += `<p>${pair}: ${score.toFixed(2)}</p>`;
    }

    // Semantic Similarities
    container.innerHTML += `<h3>Semantic Similarities:</h3>`;
    for (const item of data.semantic_similarities || []) {
        container.innerHTML += `<p>${item.ai1} vs ${item.ai2}: ${item.score.toFixed(2)}</p>`;
    }

    // Contradictions
    container.innerHTML += `<h3>Contradictions:</h3>`;
    for (const item of data.contradictions || []) {
        container.innerHTML += `<p>${item.ai1} vs ${item.ai2}: <strong>${item.label}</strong> (${item.score.toFixed(2)})</p>`;
    }

    // Named Entities
    container.innerHTML += `<h3>Named Entities:</h3>`;
    for (const [ai, entities] of Object.entries(data.named_entities || {})) {
        container.innerHTML += `<p><strong>${ai}:</strong></p><ul>`;
        for (const ent of entities) {
            container.innerHTML += `<li>${ent.word} (${ent.entity_group})</li>`;
        }
        container.innerHTML += `</ul>`;
    }

    // Sentiments
    container.innerHTML += `<h3>Sentiments:</h3>`;
    for (const [ai, sentiments] of Object.entries(data.sentiments || {})) {
        container.innerHTML += `<p><strong>${ai}:</strong></p><ul>`;
        for (const sent of sentiments) {
            container.innerHTML += `<li>${sent.label} (${sent.score.toFixed(2)})</li>`;
        }
        container.innerHTML += `</ul>`;
    }

    // Summary
    container.innerHTML += `<h3>Summary:</h3><p>${data.summary}</p>`;
}

async function fetchResponses(questionId) {
    showLoader();
    try {
        const response = await fetch(`${API_BASE_URL}/responses/by-question/`+questionId);
        if (!response.ok) throw new Error("Error fetching responses");

        const responses = await response.json();
        const responseContainer = document.getElementById("responseContainer");
        responseContainer.innerHTML = "<h3>AI Responses:</h3>";

        responses
            .filter(res => res.question_id === questionId)
            .forEach(res => {
                responseContainer.innerHTML += `<p><strong>${res.ai_name}:</strong> ${res.response_text}</p>`;
            });
        
        console.log('fetchResponses');
        await fetchSummary(questionId);
        await fetchSimilarities(questionId);
    } catch (error) {
        console.error("Failed to fetch responses:", error);
    } finally {
        hideLoader();
    }
}

async function fetchSummary(questionId) {
    try {
        const response = await fetch(`${API_BASE_URL}/summaries/by-question/`+questionId);
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
        const response = await fetch(`${API_BASE_URL}/similarities/by-question/`+questionId);
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
    showLoader();
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
                listItem.className = "history-item";

                console.log(q.created_at);
                const date = new Date(q.created_at);
                const formattedDate = date.toLocaleString();

                const questionText = document.createElement("span");
                questionText.innerHTML = `<strong>${q.text}</strong> <br> <small>${formattedDate}</small>`;
                questionText.style.cursor = "pointer";
                questionText.onclick = () => fetchResponses(q.id);

                const deleteButton = document.createElement("button");
                deleteButton.textContent = "🗑️";
                deleteButton.className = "delete-btn";
                deleteButton.onclick = () => deleteQuestion(q.id);

                listItem.appendChild(questionText);
                listItem.appendChild(deleteButton);
                historyList.appendChild(listItem);
            });
    } catch (error) {
        console.error("Failed to load history:", error);
    } finally {
        hideLoader();
    }
}

async function deleteQuestion(questionId) {
    showLoader();
    try {
        const response = await fetch(`${API_BASE_URL}/questions/${questionId}`, {
            method: "DELETE",
        });

        if (!response.ok) throw new Error("Error deleting question");

        await loadHistory();
        document.getElementById("responseContainer").innerHTML = "";
    } catch (error) {
        console.error("Failed to delete question:", error);
    } finally {
        hideLoader();
    }
}
