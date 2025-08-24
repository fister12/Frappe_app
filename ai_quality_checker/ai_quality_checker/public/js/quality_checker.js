// ai_quality_checker/ai_quality_checker/public/js/quality_checker.js

frappe.ready(function() {
    const style = document.createElement('style');
    style.innerHTML = `
        .aqc-container {
            max-width: 400px;
            margin: 40px auto;
            padding: 32px 24px;
            background: #fff;
            border-radius: 12px;
            box-shadow: 0 2px 16px rgba(0,0,0,0.08);
            font-family: 'Segoe UI', Arial, sans-serif;
        }
        .aqc-title {
            font-size: 2rem;
            margin-bottom: 18px;
            color: #2d3748;
            text-align: center;
        }
        .aqc-label {
            font-size: 1rem;
            margin-bottom: 8px;
            color: #4a5568;
        }
        .aqc-input {
            width: 100%;
            padding: 10px;
            border: 1px solid #cbd5e0;
            border-radius: 6px;
            margin-bottom: 16px;
            font-size: 1rem;
        }
        .aqc-btn {
            width: 100%;
            padding: 12px;
            background: #3182ce;
            color: #fff;
            border: none;
            border-radius: 6px;
            font-size: 1rem;
            cursor: pointer;
            transition: background 0.2s;
        }
        .aqc-btn:hover {
            background: #2563eb;
        }
        .aqc-result {
            margin-top: 20px;
            font-size: 1.1rem;
            color: #2b6cb0;
            text-align: center;
        }
        .aqc-error {
            color: #e53e3e;
        }
    `;
    document.head.appendChild(style);

    const container = document.createElement('div');
    container.className = 'aqc-container';
    container.innerHTML = `
        <div class="aqc-title">AI Quality Checker</div>
        <div class="aqc-label">Material Name</div>
        <input type="text" id="aqc-material" class="aqc-input" placeholder="Enter material name" />
        <button id="aqc-check" class="aqc-btn">Check Quality</button>
        <div id="aqc-result" class="aqc-result"></div>
    `;
    document.body.appendChild(container);

    document.getElementById('aqc-check').onclick = async function() {
        const material = document.getElementById('aqc-material').value.trim();
        const resultDiv = document.getElementById('aqc-result');
        if (!material) {
            resultDiv.innerHTML = '<span class="aqc-error">Please enter a material name.</span>';
            return;
        }
        resultDiv.innerHTML = 'Checking...';
        try {
            // Example: Call your backend API (adjust endpoint as needed)
            const response = await fetch('/api/method/ai_quality_checker.api.check_quality', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ material })
            });
            const data = await response.json();
            if (data.message) {
                resultDiv.innerHTML = `<strong>Result:</strong> ${data.message}`;
            } else {
                resultDiv.innerHTML = '<span class="aqc-error">No result returned.</span>';
            }
        } catch (err) {
            resultDiv.innerHTML = `<span class="aqc-error">Error: ${err.message}</span>`;
        }
    };
});
