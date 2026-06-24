const TOTAL = QUESTIONS.length;
const LETTERS = ['А','Б','В','Г'];
const quiz = document.getElementById('quiz');
let checked = false;
document.getElementById('total1').textContent = TOTAL;
document.getElementById('total2').textContent = TOTAL;

function norm(v){ return String(v).replace(/\s/g,'').replace(',', '.'); }
function escapeHtml(s){return s.replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));}

QUESTIONS.forEach(q=>{
  const card = document.createElement('div');
  card.className='q'; card.id='q'+q.n;
  let inner = '<h3><span class="num">'+q.n+'</span><span class="txt">'+escapeHtml(q.q)+'</span></h3>';
  if(q.type==='mc'){
    q.options.forEach((opt,idx)=>{
      inner += '<label class="opt" data-idx="'+idx+'">'+
               '<input type="radio" name="q'+q.n+'" value="'+idx+'">'+
               '<span class="letter">'+LETTERS[idx]+'.</span>'+
               '<span>'+escapeHtml(opt)+'</span></label>';
    });
  } else {
    inner += '<div class="num-input"><input type="text" inputmode="decimal" name="q'+q.n+'" '+
             'placeholder="Введіть числову відповідь"></div>'+
             '<div class="hint">Завдання на обчислення - впишіть число.</div>';
  }
  inner += '<div class="verdict" id="v'+q.n+'"></div>';
  inner += '<div class="explain" id="e'+q.n+'"></div>';
  inner += '<button class="btn-check" data-n="'+q.n+'">Перевірити</button>';
  card.innerHTML = inner;
  quiz.appendChild(card);
});

quiz.addEventListener('click',e=>{
  const b=e.target.closest('.btn-check'); if(!b) return;
  const q=QUESTIONS.find(x=>x.n==b.dataset.n);
  if(q) checkOne(q);
});

function countAnswered(){
  let n=0;
  QUESTIONS.forEach(q=>{
    if(q.type==='mc'){ if(document.querySelector('input[name="q'+q.n+'"]:checked')) n++; }
    else { const el=document.querySelector('input[name="q'+q.n+'"]'); if(el && el.value.trim()) n++; }
  });
  document.getElementById('answered').textContent=n;
  const pf=document.getElementById('pfill');
  if(pf) pf.style.width=(TOTAL?Math.round(n/TOTAL*100):0)+'%';
}
quiz.addEventListener('change',countAnswered);
quiz.addEventListener('input',countAnswered);

function checkOne(q){
  const card=document.getElementById('q'+q.n);
  const v=document.getElementById('v'+q.n);
  const e=document.getElementById('e'+q.n);
  let ok=false;
  if(q.type==='mc'){
    const sel=document.querySelector('input[name="q'+q.n+'"]:checked');
    const chosen = sel? parseInt(sel.value):-1;
    const correctIdx=q.correct[0];
    card.querySelectorAll('.opt').forEach(o=>{
      o.classList.remove('correct','wrong');
      const idx=parseInt(o.dataset.idx);
      if(idx===correctIdx) o.classList.add('correct');
      if(idx===chosen && chosen!==correctIdx) o.classList.add('wrong');
    });
    ok = (chosen===correctIdx);
  } else {
    const el=document.querySelector('input[name="q'+q.n+'"]');
    const val=el.value.trim();
    ok = val!=='' && norm(val)===norm(q.answer);
    el.style.borderColor = val===''? '' : (ok? 'var(--ok)':'var(--bad)');
  }
  if(ok){ v.className='verdict ok'; v.textContent='✓ Правильно (+1 бал)'; }
  else{
    v.className='verdict bad';
    v.textContent = q.type==='mc'
      ? '✗ Неправильно. Правильна відповідь: '+LETTERS[q.correct[0]]
      : '✗ Неправильно. Правильна відповідь: '+q.answer;
  }
  if(q.explain){ e.textContent='💡 '+q.explain; e.style.display='block'; }
  return ok;
}

document.getElementById('check').addEventListener('click',()=>{
  let score=0;
  QUESTIONS.forEach(q=>{ if(checkOne(q)) score++; });
  checked=true;
  showResult(score);
});

function showResult(score){
  const pct=Math.round(score/TOTAL*100);
  const res=document.getElementById('result');
  document.getElementById('scoreLine').textContent='Результат: '+score+' / '+TOTAL;
  document.getElementById('pctLine').textContent='· '+pct+'%';
  const b=document.getElementById('gradeBadge');
  let label,bg,fg;
  if(pct>=90){label='Відмінно';bg='#dcfce7';fg='#15803d';}
  else if(pct>=75){label='Добре';bg='#dbeafe';fg='#1d4ed8';}
  else if(pct>=50){label='Задовільно';bg='#fef9c3';fg='#a16207';}
  else{label='Потрібно повторити';bg='#fee2e2';fg='#b91c1c';}
  b.textContent=label; b.style.background=bg; b.style.color=fg;
  res.classList.add('show');
  document.getElementById('abar').classList.remove('hide');   // показати панель з результатом
  if(window.__fitBars) window.__fitBars();                    // переобчислити відступ під вищу панель
  window.scrollTo({top:0,behavior:'smooth'});
}

document.getElementById('reset').addEventListener('click',()=>{
  if(checked && !confirm('Очистити всі відповіді та пройти тест заново?')) return;
  document.querySelectorAll('input').forEach(i=>{
    if(i.type==='radio') i.checked=false; else {i.value='';i.style.borderColor='';}
  });
  document.querySelectorAll('.opt').forEach(o=>o.classList.remove('correct','wrong'));
  document.querySelectorAll('.verdict').forEach(v=>{v.textContent='';v.className='verdict';});
  document.querySelectorAll('.explain').forEach(e=>{e.textContent='';e.style.display='none';});
  document.getElementById('result').classList.remove('show');
  checked=false; countAnswered();
  if(window.__fitBars) window.__fitBars();
  window.scrollTo({top:0,behavior:'smooth'});
});

// Авто-приховування хедера й нижньої панелі за напрямком скролу:
//   хедер  — ховається ВНИЗ, з'являється ВГОРУ (і завжди видимий біля верху);
//   панель — навпаки: ВНИЗ показується, ВГОРУ ховається (і завжди видима біля низу).
// Поважає prefers-reduced-motion. Тонка смужка прогресу не ховається ніколи.
(function(){
  const abar=document.getElementById('abar');
  const topbar=document.getElementById('topbar');
  // відступи body = реальна висота панелей (щоб не перекривали контент навіть при переносі кнопок)
  function fitBars(){
    if(topbar) document.body.style.paddingTop=topbar.offsetHeight+'px';
    if(abar) document.body.style.paddingBottom=(abar.offsetHeight+8)+'px';
  }
  window.__fitBars=fitBars;   // щоб викликати після показу/приховування результату
  fitBars();
  if(window.ResizeObserver){
    const ro=new ResizeObserver(fitBars);
    if(topbar) ro.observe(topbar);
    if(abar) ro.observe(abar);
  }
  window.addEventListener('resize',fitBars);
  if(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  let lastY=window.scrollY||0, ticking=false;
  const TH=6;
  function update(){
    const y=window.scrollY||0, dy=y-lastY;
    const nearBottom=(window.innerHeight+y)>=(document.documentElement.scrollHeight-160);
    const nearTop=y<70;
    if(dy>TH){                                   // скрол вниз
      if(topbar && !nearTop) topbar.classList.add('hide');
      if(abar) abar.classList.remove('hide');
    } else if(dy<-TH){                           // скрол вгору
      if(topbar) topbar.classList.remove('hide');
      if(abar && !nearBottom) abar.classList.add('hide');
    }
    if(nearTop && topbar) topbar.classList.remove('hide');
    if(nearBottom && abar) abar.classList.remove('hide');
    lastY=y; ticking=false;
  }
  window.addEventListener('scroll',function(){
    if(!ticking){ requestAnimationFrame(update); ticking=true; }
  },{passive:true});
})();
