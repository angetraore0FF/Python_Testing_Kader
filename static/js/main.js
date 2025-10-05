// Animation au chargement de la page
document.addEventListener('DOMContentLoaded', function() {
    
    // Effet de parallaxe sur le fond
    if (window.innerWidth > 768) {
        document.addEventListener('mousemove', function(e) {
            const moveX = (e.clientX - window.innerWidth / 2) * 0.01;
            const moveY = (e.clientY - window.innerHeight / 2) * 0.01;
            
            const bgElements = document.querySelectorAll('body::before, body::after');
            document.body.style.backgroundPosition = `${50 + moveX}% ${50 + moveY}%`;
        });
    }
    
    // Animation des cartes de compétition
    const competitionItems = document.querySelectorAll('.competitions-list li');
    competitionItems.forEach((item, index) => {
        item.style.animationDelay = `${index * 0.1}s`;
    });
    
    // Animation des lignes du tableau
    const tableRows = document.querySelectorAll('tbody tr');
    tableRows.forEach((row, index) => {
        row.style.opacity = '0';
        row.style.transform = 'translateX(-20px)';
        
        setTimeout(() => {
            row.style.transition = 'all 0.5s ease';
            row.style.opacity = '1';
            row.style.transform = 'translateX(0)';
        }, index * 50);
    });
    
    // Animation de compteur pour les points
    const pointsBadge = document.querySelector('.points-badge strong');
    if (pointsBadge) {
        const finalValue = parseInt(pointsBadge.textContent);
        let currentValue = 0;
        const duration = 1500;
        const increment = finalValue / (duration / 16);
        
        const counter = setInterval(() => {
            currentValue += increment;
            if (currentValue >= finalValue) {
                pointsBadge.textContent = finalValue;
                clearInterval(counter);
            } else {
                pointsBadge.textContent = Math.floor(currentValue);
            }
        }, 16);
    }
    
    // Animation de shake pour les messages flash
    const flashMessages = document.querySelectorAll('.flash-messages li');
    flashMessages.forEach((message, index) => {
        setTimeout(() => {
            message.style.animation = 'shake 0.5s ease';
        }, index * 200);
    });
    
    // Effet de particules pour les boutons
    const buttons = document.querySelectorAll('button[type="submit"], .book-button, .back-button');
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            const rect = button.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const ripple = document.createElement('span');
            ripple.style.position = 'absolute';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.style.width = '0';
            ripple.style.height = '0';
            ripple.style.borderRadius = '50%';
            ripple.style.background = 'rgba(255, 255, 255, 0.6)';
            ripple.style.transform = 'translate(-50%, -50%)';
            ripple.style.animation = 'ripple 0.6s ease-out';
            
            button.style.position = 'relative';
            button.style.overflow = 'hidden';
            button.appendChild(ripple);
            
            setTimeout(() => ripple.remove(), 600);
        });
    });
    
    // Validation du formulaire de réservation
    const bookingForm = document.querySelector('form[action="/purchasePlaces"]');
    if (bookingForm) {
        const placesInput = document.getElementById('places');
        
        if (placesInput) {
            placesInput.addEventListener('input', function() {
                const value = parseInt(this.value);
                const max = parseInt(this.max);
                
                if (value > max) {
                    this.style.borderColor = '#ff6b6b';
                    this.style.boxShadow = '0 0 0 4px rgba(255, 107, 107, 0.2)';
                } else if (value > 0) {
                    this.style.borderColor = '#51cf66';
                    this.style.boxShadow = '0 0 0 4px rgba(81, 207, 102, 0.2)';
                } else {
                    this.style.borderColor = '#e0e0e0';
                    this.style.boxShadow = 'none';
                }
            });
            
            // Animation sur le focus
            placesInput.addEventListener('focus', function() {
                this.parentElement.style.transform = 'scale(1.02)';
                this.parentElement.style.transition = 'transform 0.3s ease';
            });
            
            placesInput.addEventListener('blur', function() {
                this.parentElement.style.transform = 'scale(1)';
            });
        }
    }
    
    // Animation de fade-in pour les éléments au scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    const fadeElements = document.querySelectorAll('.competition-details, .summary-box, .info-note');
    fadeElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'all 0.6s ease';
        observer.observe(el);
    });
    
    // Effet de hover 3D sur les cartes
    const cards = document.querySelectorAll('.competitions-list li');
    cards.forEach(card => {
        card.addEventListener('mousemove', function(e) {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            const rotateX = (y - centerY) / 10;
            const rotateY = (centerX - x) / 10;
            
            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-8px)`;
        });
        
        card.addEventListener('mouseleave', function() {
            card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) translateY(0)';
        });
    });
    
    // Animation de typing pour le titre (page d'accueil)
    const mainTitle = document.querySelector('h1');
    if (mainTitle && mainTitle.textContent.includes('GUDLFT')) {
        const text = mainTitle.textContent;
        mainTitle.textContent = '';
        mainTitle.style.opacity = '1';
        
        let i = 0;
        const typeWriter = setInterval(() => {
            if (i < text.length) {
                mainTitle.textContent += text.charAt(i);
                i++;
            } else {
                clearInterval(typeWriter);
            }
        }, 50);
    }
    
    // Confetti effect pour les réservations réussies
    const successMessages = document.querySelectorAll('.flash-success');
    if (successMessages.length > 0) {
        createConfetti();
    }
    
    function createConfetti() {
        const colors = ['#667eea', '#764ba2', '#f093fb', '#51cf66', '#ffd43b'];
        const confettiCount = 50;
        
        for (let i = 0; i < confettiCount; i++) {
            const confetti = document.createElement('div');
            confetti.style.position = 'fixed';
            confetti.style.width = '10px';
            confetti.style.height = '10px';
            confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
            confetti.style.left = Math.random() * 100 + '%';
            confetti.style.top = '-10px';
            confetti.style.opacity = '1';
            confetti.style.borderRadius = Math.random() > 0.5 ? '50%' : '0';
            confetti.style.transform = `rotate(${Math.random() * 360}deg)`;
            confetti.style.pointerEvents = 'none';
            confetti.style.zIndex = '9999';
            
            document.body.appendChild(confetti);
            
            const duration = Math.random() * 3 + 2;
            const destination = Math.random() * 100;
            
            confetti.animate([
                { transform: `translateY(0) rotate(0deg)`, opacity: 1 },
                { transform: `translateY(${window.innerHeight + 10}px) translateX(${destination}px) rotate(${Math.random() * 720}deg)`, opacity: 0 }
            ], {
                duration: duration * 1000,
                easing: 'cubic-bezier(0.25, 0.46, 0.45, 0.94)'
            });
            
            setTimeout(() => confetti.remove(), duration * 1000);
        }
    }
});

// Ajout des keyframes CSS via JavaScript
const style = document.createElement('style');
style.textContent = `
    @keyframes ripple {
        to {
            width: 200px;
            height: 200px;
            opacity: 0;
        }
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }
`;
document.head.appendChild(style);