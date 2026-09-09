/**
 * AdaptivePhish - Enhanced Frontend JavaScript
 * Professional AI Phishing Detection Interface
 */

// Configuration
const API_BASE_URL = 'http://localhost:5000';

// Global state
let scanCount = 0;
let currentResult = null;

// DOM Elements
const urlInput = document.getElementById('urlInput');
const textInput = document.getElementById('textInput');
const analyzeBtn = document.getElementById('analyzeBtn');
const analyzeTextBtn = document.getElementById('analyzeTextBtn');
const fileInput = document.getElementById('fileInput');
const analyzeScreenshotBtn = document.getElementById('analyzeScreenshotBtn');
const fileNameDisplay = document.getElementById('fileName');
const resultsSection = document.getElementById('resultsSection');
const errorSection = document.getElementById('errorSection');
const scanCountEl = document.getElementById('scanCount');

// Global state for screenshot
let selectedFile = null;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 AdaptivePhish UI initializing...');

    // Check if elements exist
    console.log('URL Input:', urlInput ? '✅' : '❌');
    console.log('Text Input:', textInput ? '✅' : '❌');
    console.log('Analyze Button:', analyzeBtn ? '✅' : '❌');
    console.log('Analyze Text Button:', analyzeTextBtn ? '✅' : '❌');

    initializeTabs();
    initializeAnalyzeButtons();
    initializeQuickTests();
    initializeTechnicalToggle();
    initializeExport();
    initializeScreenshotUpload();

    console.log('✨ AdaptivePhish Enhanced UI loaded successfully!');
    console.log('🔗 Backend API:', API_BASE_URL);

    // Test backend connection
    fetch(`${API_BASE_URL}/health`)
        .then(res => res.json())
        .then(data => {
            console.log('✅ Backend connection successful:', data);
        })
        .catch(err => {
            console.error('❌ Backend connection failed:', err);
            console.log('Make sure backend is running: cd backend && python app.py');
        });
});

/**
 * Tab Navigation
 */
function initializeTabs() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');

    tabButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetTab = btn.getAttribute('data-tab');

            // Update button states
            tabButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            // Update pane visibility
            tabPanes.forEach(pane => {
                pane.classList.remove('active');
                if (pane.id === `${targetTab}-tab`) {
                    pane.classList.add('active');
                }
            });
        });
    });
}

/**
 * Analyze Button Handlers
 */
function initializeAnalyzeButtons() {
    // URL analysis
    analyzeBtn.addEventListener('click', () => handleURLAnalysis());
    urlInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleURLAnalysis();
    });

    // Text analysis
    if (analyzeTextBtn) {
        analyzeTextBtn.addEventListener('click', () => handleTextAnalysis());
    }

    // Screenshot analysis
    if (analyzeScreenshotBtn) {
        analyzeScreenshotBtn.addEventListener('click', () => handleScreenshotAnalysis());
    }
}

/**
 * Quick Test Buttons
 */
function initializeQuickTests() {
    const quickTestBtns = document.querySelectorAll('.quick-test-btn');

    console.log(`Found ${quickTestBtns.length} quick test buttons`);

    quickTestBtns.forEach((btn, index) => {
        const url = btn.getAttribute('data-url');
        console.log(`  Button ${index + 1}: ${url}`);

        btn.addEventListener('click', () => {
            console.log(`🖱️ Quick test clicked: ${url}`);
            urlInput.value = url;
            handleURLAnalysis();
        });
    });
}

/**
 * Technical Details Toggle
 */
function initializeTechnicalToggle() {
    const toggle = document.getElementById('technicalToggle');
    const content = document.getElementById('technicalContent');
    const chevron = toggle.querySelector('.chevron');

    toggle.addEventListener('click', () => {
        const isOpen = content.style.display === 'block';
        content.style.display = isOpen ? 'none' : 'block';
        chevron.classList.toggle('open');
    });
}

/**
 * Export Functionality
 */
function initializeExport() {
    const exportBtn = document.getElementById('exportBtn');
    if (exportBtn) {
        exportBtn.addEventListener('click', () => {
            if (currentResult) {
                const dataStr = JSON.stringify(currentResult, null, 2);
                const dataBlob = new Blob([dataStr], {type: 'application/json'});
                const url = URL.createObjectURL(dataBlob);
                const link = document.createElement('a');
                link.href = url;
                link.download = `adaptivephish-scan-${Date.now()}.json`;
                link.click();
                URL.revokeObjectURL(url);
            }
        });
    }
}

/**
 * Screenshot Upload Functionality
 */
function initializeScreenshotUpload() {
    if (fileInput) {
        fileInput.addEventListener('change', (event) => {
            const file = event.target.files[0];
            if (file) {
                selectedFile = file;
                fileNameDisplay.textContent = `✅ Selected: ${file.name}`;
                analyzeScreenshotBtn.style.display = 'inline-flex';
                console.log('📸 File selected:', file.name);
            }
        });
    }
}

/**
 * Handle URL Analysis
 */
async function handleURLAnalysis() {
    const url = urlInput.value.trim();

    if (!url) {
        showError('Please enter a URL');
        return;
    }

    if (!isValidURL(url)) {
        showError('Please enter a valid URL (e.g., https://example.com)');
        return;
    }

    hideAll();
    setLoadingState(analyzeBtn, true);

    try {
        const result = await analyzeURL(url);
        currentResult = result;
        displayResults(result);
        incrementScanCount();
    } catch (error) {
        console.error('Analysis error:', error);
        showError(error.message || 'Failed to analyze URL. Make sure the backend server is running.');
    } finally {
        setLoadingState(analyzeBtn, false);
    }
}

/**
 * Handle Text Analysis
 */
async function handleTextAnalysis() {
    const text = textInput.value.trim();

    if (!text || text.length < 10) {
        showError('Please enter at least 10 characters of text to analyze');
        return;
    }

    hideAll();
    setLoadingState(analyzeTextBtn, true);

    try {
        const result = await analyzeText(text);
        currentResult = result;
        displayResults(result);
        incrementScanCount();
    } catch (error) {
        console.error('Text analysis error:', error);
        showError(error.message || 'Failed to analyze text.');
    } finally {
        setLoadingState(analyzeTextBtn, false);
    }
}

/**
 * Handle Screenshot Analysis
 */
async function handleScreenshotAnalysis() {
    if (!selectedFile) {
        showError('Please select a screenshot file first');
        return;
    }

    hideAll();
    setLoadingState(analyzeScreenshotBtn, true);

    try {
        const result = await analyzeScreenshot(selectedFile);
        currentResult = result;
        displayResults(result);
        incrementScanCount();
    } catch (error) {
        console.error('Screenshot analysis error:', error);
        showError(error.message || 'Failed to analyze screenshot.');
    } finally {
        setLoadingState(analyzeScreenshotBtn, false);
    }
}

/**
 * API Calls
 */
async function analyzeURL(url) {
    const response = await fetch(`${API_BASE_URL}/analyze/url`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ url })
    });

    if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
    }

    const data = await response.json();
    if (!data.success) {
        throw new Error('Analysis failed');
    }

    return data;
}

async function analyzeText(text, url = null) {
    const response = await fetch(`${API_BASE_URL}/analyze/text`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ text, url })
    });

    if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
    }

    const data = await response.json();
    if (!data.success) {
        throw new Error('Analysis failed');
    }

    return data;
}

async function analyzeScreenshot(file) {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${API_BASE_URL}/analyze/screenshot`, {
        method: 'POST',
        body: formData
    });

    if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
    }

    const data = await response.json();
    if (!data.success) {
        throw new Error('Analysis failed');
    }

    return data;
}

/**
 * Display Results
 */
function displayResults(data) {
    const result = data.result;

    // Add module type to result for proper display
    result.module = data.module; // Extract module from top-level API response

    // Show results section
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

    // Update verdict
    updateVerdict(result);

    // Update score circle
    updateScoreCircle(result.risk_score);

    // Update risk meter
    updateRiskMeter(result.risk_score);

    // Update module scores
    updateModuleScores(result);

    // Update findings
    updateFindings(result);

    // Update technical details
    updateTechnicalDetails(data); // Pass full data to show module info
}

/**
 * Update Verdict
 */
function updateVerdict(result) {
    const verdictIcon = document.getElementById('verdictIconLarge');
    const verdictText = document.getElementById('verdictText');
    const analyzedUrl = document.getElementById('analyzedUrl');
    const verdictCard = document.querySelector('.verdict-card');

    // Update icon and text
    verdictIcon.textContent = result.verdict_color;
    verdictText.textContent = result.verdict;

    // Update URL/description (if exists)
    if (result.url) {
        analyzedUrl.textContent = result.url;
    } else if (result.text) {
        analyzedUrl.textContent = '📝 Text Content Analysis';
    } else if (result.module === 'text_analyzer') {
        analyzedUrl.textContent = '📝 Text Content Analysis';
    } else if (result.module === 'visual_analyzer') {
        analyzedUrl.textContent = '🖼️ Screenshot Analysis';
    } else {
        analyzedUrl.textContent = '';
    }

    // Update card style
    const verdictClass = result.verdict.toLowerCase();
    verdictCard.className = 'card verdict-card glow-card verdict-' + verdictClass;
}

/**
 * Update Score Circle
 */
function updateScoreCircle(score) {
    const scoreNumber = document.getElementById('scoreNumber');
    const scoreCircle = document.getElementById('scoreCircle');
    const circumference = 339.292;
    const offset = circumference - (score / 100) * circumference;

    // Animate number
    animateValue(scoreNumber, 0, score, 1000);

    // Animate circle
    setTimeout(() => {
        scoreCircle.style.strokeDashoffset = offset;

        // Change color based on score
        let color;
        if (score < 40) color = 'var(--success-color)';
        else if (score < 70) color = 'var(--warning-color)';
        else color = 'var(--danger-color)';

        scoreCircle.style.stroke = color;
    }, 100);
}

/**
 * Update Risk Meter
 */
function updateRiskMeter(score) {
    const riskMeterFill = document.getElementById('riskMeterFill');
    const riskLevelText = document.getElementById('riskLevelText');

    // Animate fill
    setTimeout(() => {
        riskMeterFill.style.width = score + '%';
    }, 200);

    // Update level text
    let level;
    if (score < 40) level = 'LOW';
    else if (score < 70) level = 'MEDIUM';
    else level = 'HIGH';

    riskLevelText.textContent = level;
}

/**
 * Update Module Scores
 */
function updateModuleScores(result) {
    // Determine which module was used based on the result
    const moduleType = result.module || 'url_analyzer';

    // Get all module cards
    const urlCard = document.querySelector('.module-card:nth-child(1)');
    const visualCard = document.querySelector('.module-card:nth-child(2)');
    const textCard = document.querySelector('.module-card:nth-child(3)');

    // Reset all modules to N/A and inactive state
    document.getElementById('urlModuleScore').textContent = 'N/A';
    document.getElementById('visualModuleScore').textContent = 'N/A';
    document.getElementById('textModuleScore').textContent = 'N/A';

    // Reset progress bars
    document.getElementById('urlModuleBar').style.width = '0%';
    document.getElementById('visualModuleBar').style.width = '0%';
    document.getElementById('textModuleBar').style.width = '0%';

    // Set all cards to inactive
    urlCard.classList.add('module-inactive');
    visualCard.classList.add('module-inactive');
    textCard.classList.add('module-inactive');

    // Remove green dots from all
    const allDots = document.querySelectorAll('.status-dot');
    allDots.forEach(dot => dot.classList.remove('status-success'));

    // Update the specific module that was used
    const score = result.risk_score;

    if (moduleType === 'url_analyzer') {
        // URL Analysis
        document.getElementById('urlModuleScore').textContent = score + '%';
        urlCard.classList.remove('module-inactive');

        // Update status to "Analysis Complete"
        const urlStatus = urlCard.querySelector('.module-card-status span:last-child');
        if (urlStatus) {
            urlStatus.textContent = 'Analysis Complete';
        }

        // Update status dot to green
        const urlDot = urlCard.querySelector('.status-dot');
        if (urlDot) urlDot.classList.add('status-success');

        setTimeout(() => {
            document.getElementById('urlModuleBar').style.width = score + '%';
        }, 300);
        console.log('✅ URL Analysis module updated:', score + '%');
    } else if (moduleType === 'text_analyzer') {
        // Text Analysis
        document.getElementById('textModuleScore').textContent = score + '%';
        textCard.classList.remove('module-inactive');

        // Update status to "Analysis Complete"
        const textStatus = textCard.querySelector('.module-card-status span:last-child');
        if (textStatus) {
            textStatus.textContent = 'Analysis Complete';
        }

        // Update status dot to green
        const textDot = textCard.querySelector('.status-dot');
        if (textDot) textDot.classList.add('status-success');

        setTimeout(() => {
            document.getElementById('textModuleBar').style.width = score + '%';
        }, 300);
        console.log('✅ Text Analysis module updated:', score + '%');
    } else if (moduleType === 'visual_analyzer') {
        // Visual Analysis
        document.getElementById('visualModuleScore').textContent = score + '%';
        visualCard.classList.remove('module-inactive');

        // Update status to "Analysis Complete"
        const visualStatus = visualCard.querySelector('.module-card-status span:last-child');
        if (visualStatus) {
            visualStatus.textContent = 'Analysis Complete';
        }

        // Update status dot to green
        const visualDot = visualCard.querySelector('.status-dot');
        if (visualDot) visualDot.classList.add('status-success');

        setTimeout(() => {
            document.getElementById('visualModuleBar').style.width = score + '%';
        }, 300);
        console.log('✅ Visual Analysis module updated:', score + '%');
    }

    // Reset unused modules to their default status text
    if (moduleType !== 'url_analyzer') {
        const urlStatus = urlCard.querySelector('.module-card-status span:last-child');
        if (urlStatus) {
            urlStatus.textContent = 'Requires URL';
        }
    }

    if (moduleType !== 'text_analyzer') {
        const textStatus = textCard.querySelector('.module-card-status span:last-child');
        if (textStatus) {
            textStatus.textContent = 'Requires Text Content';
        }
    }

    if (moduleType !== 'visual_analyzer') {
        const visualStatus = visualCard.querySelector('.module-card-status span:last-child');
        if (visualStatus) {
            visualStatus.textContent = 'Requires Screenshot';
        }
    }
}

/**
 * Update Findings
 */
function updateFindings(result) {
    const findingsList = document.getElementById('findingsList');
    const findingsCount = document.getElementById('findingsCount');

    findingsList.innerHTML = '';

    if (!result.flags || result.flags.length === 0) {
        findingsList.innerHTML = '<div class="finding-item safe">✅ No significant issues detected</div>';
        findingsCount.textContent = '0 flags';
        return;
    }

    // Update count
    findingsCount.textContent = `${result.flags.length} flag${result.flags.length > 1 ? 's' : ''}`;

    // Add each flag
    result.flags.forEach(flag => {
        const item = document.createElement('div');
        item.className = 'finding-item';

        if (flag.startsWith('✅')) {
            item.classList.add('safe');
        }

        item.textContent = flag;
        findingsList.appendChild(item);
    });
}

/**
 * Update Technical Details
 */
function updateTechnicalDetails(result) {
    const technicalData = document.getElementById('technicalData');
    technicalData.textContent = JSON.stringify(result, null, 2);
}

/**
 * Utility Functions
 */
function hideAll() {
    resultsSection.style.display = 'none';
    errorSection.style.display = 'none';
}

function showError(message) {
    errorSection.style.display = 'block';
    document.getElementById('errorMessage').textContent = message;
    errorSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    resultsSection.style.display = 'none';
}

function setLoadingState(button, isLoading) {
    const btnText = button.querySelector('.btn-text');
    const btnLoading = button.querySelector('.btn-loading');

    if (isLoading) {
        btnText.style.display = 'none';
        btnLoading.style.display = 'flex';
        button.disabled = true;
    } else {
        btnText.style.display = 'inline';
        btnLoading.style.display = 'none';
        button.disabled = false;
    }
}

function isValidURL(string) {
    try {
        if (!string.match(/^https?:\/\//i)) {
            string = 'http://' + string;
            urlInput.value = string;
        }
        const url = new URL(string);
        return url.protocol === 'http:' || url.protocol === 'https:';
    } catch (e) {
        return false;
    }
}

function incrementScanCount() {
    scanCount++;
    if (scanCountEl) {
        scanCountEl.textContent = scanCount;
    }
}

function animateValue(element, start, end, duration) {
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        const value = Math.floor(progress * (end - start) + start);
        element.textContent = value;
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}

console.log('🛡️ AdaptivePhish Professional UI Ready');
console.log('Backend API:', API_BASE_URL);
