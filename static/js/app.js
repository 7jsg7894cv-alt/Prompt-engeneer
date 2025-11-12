// Prompt Maître - Frontend Application
// Configuration
const API_BASE_URL = window.location.origin;
const EXAMPLES = {
    1: "Je veux connecter Airtable à Slack pour être notifié quand un nouvel enregistrement est ajouté.",
    2: "Créer une automatisation qui récupère les nouveaux leads depuis Google Sheets, vérifie leur validité avec une API, enrichit les données via OpenAI, puis crée un enregistrement dans Airtable et envoie une notification Slack avec un résumé généré par IA.",
    3: "Synchroniser automatiquement les tâches entre Notion et Airtable dans les deux sens, en temps réel."
};

// DOM Elements
const rawTextInput = document.getElementById('rawTextInput');
const charCount = document.getElementById('charCount');
const generateBtn = document.getElementById('generateBtn');
const exampleButtons = document.querySelectorAll('.example-btn');
const loadingState = document.getElementById('loadingState');
const resultsSection = document.getElementById('resultsSection');
const errorState = document.getElementById('errorState');
const errorMessage = document.getElementById('errorMessage');
const tabButtons = document.querySelectorAll('.tab-btn');
const textTab = document.getElementById('textTab');
const jsonTab = document.getElementById('jsonTab');
const textPrompt = document.getElementById('textPrompt');
const jsonPrompt = document.getElementById('jsonPrompt');
const copyButtons = document.querySelectorAll('.copy-btn');
const toast = document.getElementById('toast');

// State
let currentPromptData = null;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initializeEventListeners();
    updateCharacterCount();
});

// Event Listeners
function initializeEventListeners() {
    // Input textarea
    rawTextInput.addEventListener('input', updateCharacterCount);
    rawTextInput.addEventListener('input', validateInput);

    // Generate button
    generateBtn.addEventListener('click', handleGenerate);

    // Example buttons
    exampleButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const exampleId = btn.getAttribute('data-example');
            rawTextInput.value = EXAMPLES[exampleId];
            updateCharacterCount();
            validateInput();
            // Smooth scroll to input
            rawTextInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
            // Focus with selection
            setTimeout(() => {
                rawTextInput.focus();
                rawTextInput.setSelectionRange(0, 0);
            }, 300);
        });
    });

    // Tab buttons
    tabButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetTab = btn.getAttribute('data-tab');
            switchTab(targetTab);
        });
    });

    // Copy buttons
    copyButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const copyType = btn.getAttribute('data-copy');
            handleCopy(copyType);
        });
    });

    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        // Ctrl/Cmd + Enter to generate
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            e.preventDefault();
            if (!generateBtn.disabled) {
                handleGenerate();
            }
        }
    });
}

// Character count
function updateCharacterCount() {
    const count = rawTextInput.value.length;
    charCount.textContent = count;

    if (count > 5000) {
        charCount.style.color = 'var(--error)';
    } else if (count > 4500) {
        charCount.style.color = 'var(--warning)';
    } else {
        charCount.style.color = 'var(--text-tertiary)';
    }
}

// Validate input
function validateInput() {
    const text = rawTextInput.value.trim();
    const isValid = text.length >= 10 && text.length <= 5000;
    generateBtn.disabled = !isValid;
}

// Handle generate
async function handleGenerate() {
    const text = rawTextInput.value.trim();

    if (!text || text.length < 10) {
        showToast('Veuillez entrer au moins 10 caractères', 'error');
        return;
    }

    if (text.length > 5000) {
        showToast('Le texte ne peut pas dépasser 5000 caractères', 'error');
        return;
    }

    // Show loading state
    hideAllStates();
    loadingState.style.display = 'block';
    generateBtn.disabled = true;

    try {
        const response = await fetch(`${API_BASE_URL}/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ raw_text: text })
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();
        currentPromptData = data;

        // Display results
        displayResults(data);

        // Show success toast
        showToast('Prompt généré avec succès !', 'success');

        // Scroll to results
        setTimeout(() => {
            resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 100);

    } catch (error) {
        console.error('Generation error:', error);
        showError(error.message);
        showToast('Erreur lors de la génération', 'error');
    } finally {
        generateBtn.disabled = false;
    }
}

// Display results
function displayResults(data) {
    hideAllStates();

    // Set prompt content
    textPrompt.textContent = data.text_prompt;
    jsonPrompt.textContent = JSON.stringify(JSON.parse(data.json_prompt), null, 2);

    // Set metadata
    const metadata = data.metadata;

    // Tools
    const toolsHTML = metadata.detected_tools
        .map(tool => `<span class="tool-badge">${tool}</span>`)
        .join(' ');
    document.getElementById('detectedTools').innerHTML = toolsHTML || 'Aucun';

    // Intent
    document.getElementById('detectedIntent').textContent =
        metadata.detected_intent.charAt(0).toUpperCase() + metadata.detected_intent.slice(1);

    // Complexity
    const complexityScore = metadata.complexity_score;
    const complexityHTML = generateComplexityStars(complexityScore);
    document.getElementById('complexityScore').innerHTML = complexityHTML;

    // Generation time
    document.getElementById('generationTime').textContent =
        `${metadata.generation_time_seconds.toFixed(3)}s`;

    // Show results section
    resultsSection.style.display = 'block';
}

// Generate complexity stars
function generateComplexityStars(score) {
    const stars = [];
    const colors = ['#10b981', '#3b82f6', '#f59e0b', '#ef4444', '#dc2626'];

    for (let i = 0; i < 5; i++) {
        if (i < score) {
            stars.push(`<span style="color: ${colors[score - 1]}">★</span>`);
        } else {
            stars.push('<span style="color: var(--border)">★</span>');
        }
    }

    return stars.join('');
}

// Switch tab
function switchTab(tabName) {
    // Update tab buttons
    tabButtons.forEach(btn => {
        if (btn.getAttribute('data-tab') === tabName) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });

    // Update tab content
    if (tabName === 'text') {
        textTab.classList.add('active');
        jsonTab.classList.remove('active');
    } else {
        jsonTab.classList.add('active');
        textTab.classList.remove('active');
    }
}

// Handle copy
async function handleCopy(type) {
    let textToCopy = '';

    if (type === 'text') {
        textToCopy = currentPromptData.text_prompt;
    } else if (type === 'json') {
        textToCopy = currentPromptData.json_prompt;
    }

    try {
        await navigator.clipboard.writeText(textToCopy);
        showToast('Copié dans le presse-papier !', 'success');
    } catch (error) {
        console.error('Copy failed:', error);
        // Fallback method
        fallbackCopy(textToCopy);
    }
}

// Fallback copy method
function fallbackCopy(text) {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    textarea.style.opacity = '0';
    document.body.appendChild(textarea);
    textarea.select();

    try {
        document.execCommand('copy');
        showToast('Copié dans le presse-papier !', 'success');
    } catch (error) {
        showToast('Impossible de copier', 'error');
    }

    document.body.removeChild(textarea);
}

// Show error
function showError(message) {
    hideAllStates();
    errorMessage.textContent = message;
    errorState.style.display = 'block';
}

// Hide all states
function hideAllStates() {
    loadingState.style.display = 'none';
    resultsSection.style.display = 'none';
    errorState.style.display = 'none';
}

// Show toast notification
function showToast(message, type = 'info') {
    toast.textContent = message;
    toast.className = 'toast';

    if (type === 'success') {
        toast.classList.add('success');
    } else if (type === 'error') {
        toast.classList.add('error');
    }

    // Show toast
    setTimeout(() => {
        toast.classList.add('show');
    }, 100);

    // Hide toast after 3 seconds
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3100);
}

// Add CSS for tool badges dynamically
const style = document.createElement('style');
style.textContent = `
    .tool-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        background: linear-gradient(135deg, var(--primary-light), var(--secondary));
        color: white;
        border-radius: var(--radius-sm);
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
        box-shadow: var(--shadow-sm);
    }
`;
document.head.appendChild(style);

// Console welcome message
console.log('%c🚀 Prompt Maître', 'font-size: 20px; font-weight: bold; color: #6366f1;');
console.log('%cGénérateur Automatique de Prompts No Code', 'font-size: 14px; color: #64748b;');
console.log('%cAPI Documentation: ' + API_BASE_URL + '/docs', 'color: #3b82f6;');
