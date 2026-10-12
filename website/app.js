/**
 * Antimagist V5 Singularity — Commercial Website Client Logic
 * Handles interactive apex boost simulation, modal checkout, and instant key generation
 */

document.addEventListener('DOMContentLoaded', () => {
  // Elements
  const btnDemo = document.getElementById('btn-demo-telemetry');
  const terminalBody = document.getElementById('telemetry-terminal');
  const pingVal = document.getElementById('live-ping-val');
  const ramVal = document.getElementById('live-ram-val');
  const gpuVal = document.getElementById('live-gpu-val');

  const checkoutModal = document.getElementById('checkout-modal');
  const btnCloseModal = document.getElementById('btn-close-modal');
  const checkoutForm = document.getElementById('checkout-form');
  const modalTierTitle = document.getElementById('modal-tier-title');
  const modalPriceTag = document.getElementById('modal-price-tag');
  const keyDeliveryResult = document.getElementById('key-delivery-result');
  const deliveredKeyText = document.getElementById('delivered-key-text');
  const btnCopyWebKey = document.getElementById('btn-copy-web-key');
  const buyButtons = document.querySelectorAll('.btn-buy');

  let activeTier = 'LIFETIME';

  // 1. Apex Boost Simulation
  if (btnDemo) {
    btnDemo.addEventListener('click', () => {
      btnDemo.disabled = true;
      btnDemo.innerHTML = '<span>⚡ APPLYING REAL-TIME SYSTEM OPTIMIZATION...</span>';

      const logs = [
        '[>] Network Registry: Disabling Nagle packet buffering (TcpNoDelay & TcpAckFrequency=1)...',
        '[>] Memory Management: Calling Windows EmptyWorkingSet API to free standby RAM cache...',
        '[>] CPU Director: Mapping topology & setting process affinity to physical Performance Cores...',
        '[>] Windows Latency Stripper: Disabling background Xbox GameDVR recording...',
        '[>] Input Tracking: Setting 1:1 linear mouse curves (zero registry acceleration)...',
        '[✅] OPTIMIZATION VERIFIED — UNTHROTTLED HARDWARE PRIORITY ACTIVE'
      ];

      terminalBody.innerHTML = '';
      let index = 0;

      const interval = setInterval(() => {
        if (index < logs.length) {
          const div = document.createElement('div');
          div.className = 'log-line text-cyan';
          if (index === logs.length - 1) {
            div.className = 'log-line text-emerald bold highlight';
          }
          div.textContent = logs[index];
          terminalBody.appendChild(div);
          terminalBody.scrollTop = terminalBody.scrollHeight;
          index++;
        } else {
          clearInterval(interval);
          pingVal.textContent = 'Immediate';
          ramVal.textContent = 'Cache Freed';
          gpuVal.textContent = 'Monitored';
          btnDemo.innerHTML = '<span>✅ Optimization Verified</span>';
          btnDemo.classList.add('btn-primary');
          btnDemo.classList.remove('btn-secondary');
        }
      }, 350);
    });
  }

  // 2. Buy Modal Triggers
  buyButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const tier = btn.getAttribute('data-tier');
      const price = btn.getAttribute('data-price');
      activeTier = tier;

      modalTierTitle.textContent = tier === 'LIFETIME' ? 'Singularity Lifetime License' : 'Pro Gamer Monthly Pass';
      modalPriceTag.textContent = tier === 'LIFETIME' ? '€10 One-Time Lifetime Payment' : '€2 / Month Recurring Subscription';

      checkoutForm.classList.remove('hidden');
      keyDeliveryResult.classList.add('hidden');

      if (typeof checkoutModal.showModal === 'function') {
        checkoutModal.showModal();
      } else {
        checkoutModal.setAttribute('open', '');
      }
    });
  });

  if (btnCloseModal) {
    btnCloseModal.addEventListener('click', () => {
      if (typeof checkoutModal.close === 'function') {
        checkoutModal.close();
      } else {
        checkoutModal.removeAttribute('open');
      }
    });
  }

  // 3. Checkout Submission & Live Key Generator Simulation
  if (checkoutForm) {
    checkoutForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const contact = document.getElementById('buyer-contact').value;

      // Generate realistic cryptographic format key
      const randHex = () => Math.floor((1 + Math.random()) * 0x10000).toString(16).substring(1).toUpperCase();
      const prefix = activeTier === 'LIFETIME' ? 'AM5-LIFE-9999999999' : `AM5-SUB-${Math.floor(Date.now() / 1000 + 2592000)}`;
      const generatedKey = `${prefix}-${randHex()}-${randHex()}-${randHex()}`;

      checkoutForm.classList.add('hidden');
      keyDeliveryResult.classList.remove('hidden');
      deliveredKeyText.textContent = generatedKey;
    });
  }

  // 4. Copy Key Button
  if (btnCopyWebKey) {
    btnCopyWebKey.addEventListener('click', () => {
      const key = deliveredKeyText.textContent;
      navigator.clipboard.writeText(key).then(() => {
        btnCopyWebKey.textContent = '✅ Copied to Clipboard!';
        setTimeout(() => {
          btnCopyWebKey.textContent = '📋 Copy Key to Clipboard';
        }, 2500);
      });
    });
  }

  // 5. Community Feedback Form Submission
  const feedbackForm = document.getElementById('feedback-form');
  const feedbackSuccess = document.getElementById('feedback-success');

  if (feedbackForm) {
    feedbackForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const author = document.getElementById('feedback-author').value;
      const msg = document.getElementById('feedback-msg').value;

      try {
        const stored = JSON.parse(localStorage.getItem('antimagist_reviews') || '[]');
        stored.push({ author, msg, time: new Date().toISOString() });
        localStorage.setItem('antimagist_reviews', JSON.stringify(stored));
      } catch (err) {}

      feedbackForm.style.display = 'none';
      feedbackSuccess.classList.remove('hidden');
    });
  }
});
