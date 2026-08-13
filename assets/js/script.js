    const menuBtn=document.getElementById('menuBtn');
    const header=document.getElementById('topbar');
    const year=document.getElementById('year');
    if(year) year.textContent=new Date().getFullYear();

    if(menuBtn){
      menuBtn.addEventListener('click',()=>{const open=header.classList.toggle('nav-open');menuBtn.setAttribute('aria-expanded',String(open));});
      document.querySelectorAll('.nav-links a').forEach(a=>a.addEventListener('click',()=>header.classList.remove('nav-open')));
    }
    document.addEventListener('keydown',e=>{if(e.key==='Escape'){header.classList.remove('nav-open');menuBtn&&menuBtn.setAttribute('aria-expanded','false');}});

    const observer=new IntersectionObserver(entries=>entries.forEach(entry=>{if(entry.isIntersecting)entry.target.classList.add('is-visible')}),{threshold:.08});
    document.querySelectorAll('[data-tilt]').forEach(card=>{
      const motion=window.matchMedia('(prefers-reduced-motion: reduce)');
      if(motion.matches) return;
      const reset=()=>{card.style.transform='rotateX(0deg) rotateY(0deg) translateZ(0)';};
      card.addEventListener('pointermove',e=>{
        if(e.pointerType==='touch') return;
        const r=card.getBoundingClientRect();
        const x=(e.clientX-r.left)/r.width-.5;
        const y=(e.clientY-r.top)/r.height-.5;
        card.style.transform=`rotateX(${(-y*4).toFixed(2)}deg) rotateY(${(x*5).toFixed(2)}deg)`;
      });
      card.addEventListener('pointerleave',reset);
    });

    document.querySelectorAll('.reveal').forEach(el=>observer.observe(el));
