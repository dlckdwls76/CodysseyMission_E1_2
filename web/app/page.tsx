"use client";

import { FormEvent, useEffect, useState } from "react";

type Quiz = { question: string; choices: string[]; answer: number };
type Score = { correct: number; total: number; score: number } | null;
type View = "home" | "play" | "add" | "list" | "score";

const defaults: Quiz[] = [
  { question: "Python에서 문자열을 나타내는 자료형은?", choices: ["int", "str", "bool", "list"], answer: 2 },
  { question: "조건에 따라 다른 코드를 실행할 때 사용하는 키워드는?", choices: ["if", "for", "def", "import"], answer: 1 },
  { question: "여러 값을 순서대로 저장하는 자료형은?", choices: ["bool", "float", "list", "None"], answer: 3 },
  { question: "함수를 정의할 때 사용하는 키워드는?", choices: ["class", "return", "while", "def"], answer: 4 },
  { question: "클래스의 인스턴스 자신을 가리키는 이름은?", choices: ["this", "self", "me", "object"], answer: 2 },
];

const nav: [View, string, string][] = [["home","⌂","홈"],["play","▶","퀴즈 풀기"],["add","+","문제 추가"],["list","≡","문제 목록"],["score","★","최고 점수"]];

export default function Home() {
  const [view, setView] = useState<View>("home");
  const [quizzes, setQuizzes] = useState<Quiz[]>(defaults);
  const [best, setBest] = useState<Score>(null);
  const [current, setCurrent] = useState(0);
  const [correct, setCorrect] = useState(0);
  const [selected, setSelected] = useState<number | null>(null);
  const [finished, setFinished] = useState(false);
  const [ready, setReady] = useState(false);

  useEffect(() => {
    try { const saved = JSON.parse(localStorage.getItem("quiz-lab") || "null"); if (saved?.quizzes) setQuizzes(saved.quizzes); if (saved?.best) setBest(saved.best); } catch {}
    setReady(true);
  }, []);
  useEffect(() => { if (ready) localStorage.setItem("quiz-lab", JSON.stringify({ quizzes, best })); }, [quizzes, best, ready]);

  function start() { setCurrent(0); setCorrect(0); setSelected(null); setFinished(false); setView("play"); }
  function move(target: View) { target === "play" ? start() : setView(target); }
  function choose(index: number) { if (selected !== null) return; setSelected(index); if (index + 1 === quizzes[current].answer) setCorrect(v => v + 1); }
  function next() {
    if (current < quizzes.length - 1) { setCurrent(v => v + 1); setSelected(null); return; }
    const score = Math.round(correct / quizzes.length * 100);
    if (!best || score > best.score) setBest({ correct, total: quizzes.length, score });
    setFinished(true);
  }
  function add(event: FormEvent<HTMLFormElement>) {
    event.preventDefault(); const data = new FormData(event.currentTarget);
    setQuizzes(q => [...q, { question: String(data.get("question")), choices: [1,2,3,4].map(n => String(data.get(`choice${n}`))), answer: Number(data.get("answer")) }]);
    event.currentTarget.reset(); setView("list");
  }

  return <main className="shell">
    <aside><div className="brand"><b>Py</b><span>Quiz Lab<small>PYTHON BASICS</small></span></div><nav>{nav.map(([id, icon, label]) => <button key={id} className={view === id ? "active" : ""} onClick={() => move(id)}><i>{icon}</i>{label}</button>)}</nav><div className="aside-card"><small>오늘의 목표</small><strong>한 문제씩, 확실하게.</strong><span>{quizzes.length}개 문제 준비됨</span></div></aside>
    <section className="content"><header><div><small>INTERACTIVE LEARNING</small><h1>{nav.find(n => n[0] === view)?.[2]}</h1></div><span className="saved">● 브라우저에 자동 저장</span></header>
      {view === "home" && <><div className="hero"><div><label>PYTHON STARTER</label><h2>문법을 읽었다면,<br/><em>이제 직접 맞혀보세요.</em></h2><p>핵심 문제로 시작해 나만의 퀴즈를 추가하고 최고 점수를 갱신해 보세요.</p><button className="primary" onClick={start}>퀴즈 시작하기 →</button></div><pre><b>class</b> Quiz:{"\n"}  <i>def</i> check_answer(self):{"\n"}    <u>return</u> answer == truth</pre></div><div className="stats"><article><span>준비된 문제</span><strong>{quizzes.length}</strong><small>직접 추가 가능</small></article><article><span>최고 기록</span><strong>{best ? `${best.score}점` : "도전 전"}</strong><small>{best ? `${best.correct}/${best.total} 정답` : "첫 기록을 만들어보세요"}</small></article><article className="lime"><span>학습 방식</span><strong>즉시</strong><small>정답 피드백 제공</small></article></div><h3 className="quick-title">빠른 시작</h3><div className="actions"><button onClick={start}>01 <b>퀴즈 풀기</b><span>→</span></button><button onClick={() => setView("add")}>02 <b>문제 만들기</b><span>→</span></button><button onClick={() => setView("list")}>03 <b>목록 보기</b><span>→</span></button></div></>}
      {view === "play" && <div className="card quiz">{!quizzes.length ? <Empty onAdd={() => setView("add")} /> : finished ? <Result correct={correct} total={quizzes.length} retry={start} /> : <><div className="meta">QUESTION {current + 1} / {quizzes.length}<span>{Math.round(current / quizzes.length * 100)}%</span></div><div className="bar"><i style={{width:`${(current + 1) / quizzes.length * 100}%`}}/></div><h2>{quizzes[current].question}</h2><div className="choices">{quizzes[current].choices.map((choice,index) => { const right = index + 1 === quizzes[current].answer; const state = selected === null ? "" : right ? "right" : selected === index ? "wrong" : "dim"; return <button className={state} key={choice} onClick={() => choose(index)}><b>{String.fromCharCode(65+index)}</b>{choice}{selected !== null && right && <i>✓</i>}</button>})}</div>{selected !== null && <div className="feedback"><strong>{selected + 1 === quizzes[current].answer ? "정답입니다!" : "아쉬워요. 정답을 확인하세요."}</strong><button onClick={next}>{current === quizzes.length - 1 ? "결과 보기" : "다음 문제"} →</button></div>}</>}</div>}
      {view === "add" && <div className="card form"><small>CREATE YOUR OWN</small><h2>새로운 문제 만들기</h2><p>문제와 선택지 4개, 정답을 입력하세요.</p><form onSubmit={add}><label>문제<input name="question" required placeholder="문제를 입력하세요"/></label><div className="input-grid">{[1,2,3,4].map(n => <label key={n}>선택지 {n}<input name={`choice${n}`} required placeholder={`선택지 ${n}`}/></label>)}</div><label>정답<select name="answer">{[1,2,3,4].map(n => <option value={n} key={n}>{String.fromCharCode(64+n)} — 선택지 {n}</option>)}</select></label><button className="primary">문제 저장하기 →</button></form></div>}
      {view === "list" && <div className="card list"><div className="title-row"><div><small>QUESTION BANK</small><h2>등록된 문제 {quizzes.length}개</h2></div><button className="primary" onClick={() => setView("add")}>+ 문제 추가</button></div>{quizzes.map((q,i) => <article key={q.question+i}><b>{String(i+1).padStart(2,"0")}</b><div><h3>{q.question}</h3><p>{q.choices.join(" · ")}</p></div><span>정답 {String.fromCharCode(64+q.answer)}</span></article>)}</div>}
      {view === "score" && <div className="card score"><div className="star">★</div><small>PERSONAL BEST</small>{best ? <><h2>{best.score}<i>점</i></h2><p>{best.total}문제 중 {best.correct}문제를 맞혔습니다.</p><button className="primary" onClick={start}>기록에 다시 도전하기 →</button></> : <><h2 className="none">아직 기록이 없어요</h2><p>첫 퀴즈를 완료하면 최고 점수가 여기에 저장됩니다.</p><button className="primary" onClick={start}>첫 퀴즈 시작하기 →</button></>}</div>}
    </section>
  </main>;
}

function Result({correct,total,retry}:{correct:number;total:number;retry:()=>void}) { const score=Math.round(correct/total*100); return <div className="result"><small>SESSION COMPLETE</small><h2>{score}<i>점</i></h2><p>{total}문제 중 <b>{correct}문제</b>를 맞혔습니다.</p><button className="primary" onClick={retry}>다시 도전하기</button></div> }
function Empty({onAdd}:{onAdd:()=>void}) { return <div className="result"><h2>문제가 없습니다</h2><button className="primary" onClick={onAdd}>문제 추가하기</button></div> }
