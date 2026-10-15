// ===============================
// CINEMATIC INTRO
// ===============================

const enterBtn = document.getElementById("enterBtn");
const intro = document.getElementById("intro");

enterBtn.addEventListener("click", () => {
    intro.classList.add("hide");

    setTimeout(() => {
        intro.style.display = "none";
    }, 1300);
});


// ===============================
// SMOOTH SECTION NAVIGATION
// ===============================

function scrollToSection(id) {
    document.getElementById(id).scrollIntoView({
        behavior: "smooth"
    });
}


// ===============================
// COUNTER ANIMATION
// ===============================

function animateCounter(element, target) {
    const duration = 1500;
    const stepTime = 20;
    const increment = target / (duration / stepTime);

    let current = 0;
    const timer = setInterval(() => {
        current += increment;

        if (current >= target) {
            current = target;
            clearInterval(timer);
        }

        element.textContent = Math.floor(current).toLocaleString();
    }, stepTime);
}

function loadDashboardMetrics() {
    fetch('/api/dashboard')
        .then((response) => response.json())
        .then((data) => {
            const metrics = [
                { selector: '.stat-card:nth-child(1) .counter', value: Number(data.generated_kwh || 0) },
                { selector: '.stat-card:nth-child(2) .counter', value: Number(data.available_kwh || 0) },
                { selector: '.stat-card:nth-child(3) .counter', value: Number(data.transactions || 0) },
                { selector: '.stat-card:nth-child(4) .counter', value: Number(data.producers || 0) + Number(data.consumers || 0) }
            ];

            metrics.forEach(({ selector, value }) => {
                const element = document.querySelector(selector);
                if (element) {
                    element.dataset.target = String(value);
                    element.textContent = '0';
                    animateCounter(element, value);
                }
            });
        })
        .catch((error) => {
            console.error('Dashboard fetch failed:', error);
        });
}

const counters = document.querySelectorAll('.counter');

const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        if (!entry.isIntersecting) return;

        const counter = entry.target;
        const target = Number(counter.dataset.target || 0);

        if (target > 0) {
            animateCounter(counter, target);
        }

        observer.unobserve(counter);
    });
}, {
    threshold: 0.5
});

counters.forEach(counter => observer.observe(counter));

window.addEventListener('DOMContentLoaded', () => {
    loadDashboardMetrics();
});


// ===============================
// PARTICLE SYSTEM
// ===============================

const canvas = document.getElementById("particles");
const ctx = canvas.getContext("2d");

let particles = [];

function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}

resizeCanvas();

window.addEventListener("resize", resizeCanvas);


for (let i = 0; i < 80; i++) {

    particles.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        size: Math.random() * 2,
        speedX: (Math.random() - 0.5) * 0.4,
        speedY: (Math.random() - 0.5) * 0.4
    });

}


function animateParticles() {

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    particles.forEach(p => {

        p.x += p.speedX;
        p.y += p.speedY;

        if (p.x < 0) p.x = canvas.width;
        if (p.x > canvas.width) p.x = 0;

        if (p.y < 0) p.y = canvas.height;
        if (p.y > canvas.height) p.y = 0;

        ctx.beginPath();

        ctx.arc(
            p.x,
            p.y,
            p.size,
            0,
            Math.PI * 2
        );

        ctx.fillStyle = "rgba(0,255,224,0.5)";
        ctx.fill();

    });

    requestAnimationFrame(animateParticles);
}

animateParticles();


// ===============================
// FAKE TRANSACTION DEMO
// ===============================

function createTransaction() {

    const button = document.querySelector(".trade-box .primary-btn");

    button.textContent = "VERIFYING BLOCKCHAIN...";

    button.disabled = true;

    setTimeout(() => {

        button.textContent = "✓ TRANSACTION CONFIRMED";

        setTimeout(() => {

            button.textContent = "CONFIRM TRANSACTION";
            button.disabled = false;

        }, 2500);

    }, 1800);
}


// ===============================
// LIVE ENERGY SIMULATION
// ===============================

setInterval(() => {

    const energyValues = document.querySelectorAll(".energy-value strong");

    energyValues.forEach(value => {

        let current = parseInt(value.textContent);

        const change = Math.floor(Math.random() * 5) - 2;

        current += change;

        if (current < 0) current = 0;

        value.textContent = current;

    });

}, 3000);