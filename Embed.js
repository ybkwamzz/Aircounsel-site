(function() {
    // 1. Capture configuration from the script tag
    const scriptTag = document.currentScript;
    const firmId = scriptTag?.getAttribute('data-firm') || 'default_firm';
    const iframeUrl = 'https://aircounsel.uk/intake.html';
    const iframeOrigin = new URL(iframeUrl).origin;
    const WEBHOOK_URL = 'https://ngrokhq.link/vid';

    // 2. Inject Strict Structural CSS (Protected from host site styling)
    const style = document.createElement('style');
    style.innerHTML = `
        .strata-embed-btn {
            position: fixed; bottom: 32px; right: 32px; z-index: 2147483646;
            background: #0d1b2a; color: #b89a5a; border: 1px solid #b89a5a;
            padding: 16px 28px; font-family: system-ui, -apple-system, sans-serif; 
            font-size: 13px; font-weight: 500; letter-spacing: 0.15em; 
            text-transform: uppercase; cursor: pointer; 
            box-shadow: 0 4px 24px rgba(0,0,0,0.2);
            transition: all 0.25s ease;
        }
        .strata-embed-btn:hover { 
            background: #162032; 
            transform: translateY(-2px); 
            border-color: #d4b97a;
        }
        .strata-embed-overlay {
            position: fixed; inset: 0; background: rgba(3, 3, 10, 0.95);
            z-index: 2147483647; display: none; align-items: center; justify-content: center;
            backdrop-filter: blur(4px);
        }
        .strata-embed-modal {
            width: 100%; max-width: 720px; height: 90vh; 
            border: 1px solid rgba(184,154,90,0.18);
            background: #070d14; position: relative; 
            display: flex; flex-direction: column;
            box-shadow: 0 10px 40px rgba(0,0,0,0.5);
        }
        .strata-embed-close {
            position: absolute; top: -45px; right: 0; background: none; border: none;
            color: rgba(248,247,244,0.52); font-family: monospace; font-size: 13px;
            cursor: pointer; text-transform: uppercase; letter-spacing: 0.15em;
            transition: color 0.2s;
        }
        .strata-embed-close:hover { color: #b89a5a; }
        .strata-embed-iframe { 
            width: 100%; height: 100%; border: none; background: #070d14;
        }
    `;
    document.head.appendChild(style);

    // 3. Construct the UI Architecture
    const btn = document.createElement('button');
    btn.className = 'strata-embed-btn';
    btn.innerText = 'Start Assessment';

    const overlay = document.createElement('div');
    overlay.className = 'strata-embed-overlay';

    const modal = document.createElement('div');
    modal.className = 'strata-embed-modal';

    const closeBtn = document.createElement('button');
    closeBtn.className = 'strata-embed-close';
    closeBtn.innerText = '✕ Close Window';

    const iframe = document.createElement('iframe');
    iframe.className = 'strata-embed-iframe';
    // Load the raw form and pass configuration via postMessage once ready.
    iframe.src = iframeUrl;

    iframe.onload = () => {
        iframe.contentWindow?.postMessage({
            action: 'INIT_CONFIG',
            firm_id: firmId
        }, iframeOrigin);
    };

    // 4. Assemble the DOM
    modal.appendChild(closeBtn);
    modal.appendChild(iframe);
    overlay.appendChild(modal);
    document.body.appendChild(btn);
    document.body.appendChild(overlay);

    // 5. Deterministic Interaction Logic
    btn.onclick = () => { 
        overlay.style.display = 'flex'; 
        document.body.style.overflow = 'hidden'; // Prevent background scrolling
    };
    
    const closeModal = () => { 
        overlay.style.display = 'none'; 
        document.body.style.overflow = '';
    };
    closeBtn.onclick = closeModal;

    // Optional: Listen for completion message from intake.html to auto-close
    window.addEventListener('message', (event) => {
        // Only accept messages from the embedded intake origin and the specific completion token
        if (event.origin === iframeOrigin && event.data === 'STRATA_INTAKE_COMPLETE') {
            // Auto-close the overlay 3 seconds after confirmation displays
            setTimeout(closeModal, 3000);
        }
    });
})();
