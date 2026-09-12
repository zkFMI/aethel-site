"""Build Aethel's English and Japanese product pages without dependencies."""
from pathlib import Path
from html import escape
import os
import shutil

ROOT = Path(__file__).parent
OUT = ROOT/'public'
BASE = (os.environ.get('SITE_URL') or 'https://aethel.fi').rstrip('/')
COPY = {
 'en': {
  'title':'Aethel — Programmable payment-stream receivables',
  'description':'Aethel turns signed payment streams into financeable receivables with independent credit assessment, guarantees, funding and servicing.',
  'nav':['The product','Lifecycle','Providers','Evaluate'],
  'label':'AETHEL / A ZKFMI APPLICATION',
  'headline':'A payment stream.<br>A financeable receivable.',
  'intro':'Aethel turns a signed payment stream into a receivable, with credit assessment, guarantees, funding and servicing supplied by independent providers.',
  'cta':'Explore the lifecycle','secondary':'Read the specification',
  'note':'Programmable obligations. Explicit provider roles. Settlement through zkFMI.',
  'focus':'THE PRODUCT','focus_title':'The stream is<br>the receivable.',
  'focus_body':'Keep the payment obligation at the centre. Define which streams may be financed, bind decisions and guarantees to the same receivable, and record each change in a versioned lifecycle.',
  'features':[
   ('Signed payment streams','Register a payment stream with identifiable terms, versions and authorization. Group eligible streams into receivable series governed by an explicit policy.'),
   ('Independent financial providers','Combine credit assessors, guarantors and liquidity providers. Their responsibilities and signed commitments remain separate.'),
   ('Settlement with evidence','Connect issuance and claims to zkPI settlement instructions and DeFMI. The host validates settlement evidence before finalizing the corresponding state.')],
  'lifecycle':'THE LIFECYCLE','life_title':'One obligation.<br>Traceable decisions.',
  'life_body':'The core state machine records the commercial meaning of a receivable. External providers and settlement systems connect through explicit interfaces.',
  'stages':[('Register','Attest the payment stream and define the eligible receivable series.'),('Assess & cover','Attach signed credit decisions and guarantee commitments to the receivable context.'),('Fund & issue','Compare funding quotes, issue the receivable and connect the asset transfer to settlement.'),('Service','Record payment evidence, delinquency, cure and permitted servicing actions.'),('Close or claim','Close a paid obligation, or bind default evidence to guarantee claims and loss allocation.')],
  'boundary':'Aethel records obligations and their lifecycle. It does not hold cash, securities or legal title. Authoritative asset settlement belongs to DeFMI; legal treatment is deployment-specific.',
  'provider_label':'OPEN PROVIDER MODEL','provider_title':'Each role has<br>its own authority.',
  'provider_body':'A credit decision does not become a guarantee. A guarantee does not grant funding authority. Providers are registered with narrowly scoped capabilities that can be suspended, revoked or rotated.',
  'roles':[('Stream attestor','Attests the payment stream and its updates.'),('Credit assessor','Signs a decision for the specific receivable.'),('Guarantor','Commits coverage backed by an external facility.'),('Liquidity provider','Submits a funding quote.'),('Servicer','Performs authorized servicing actions.'),('Credential issuer','Vouches for a qualification issuer key.')],
  'integration_title':'Connected through zkFMI',
  'integration_body':'DeKYX supplies qualification checks. DeCCP manages guarantee facilities and capacity. zkPI binds settlement instructions, and DeFMI owns asset and cash settlement. Aethel’s host connects these modules to its business state.',
  'evaluate_label':'EVALUATE AETHEL','evaluate_title':'Start with the obligation<br>you need to finance.',
  'evaluate_body':'Review the source and enterprise PoC guide with the teams responsible for origination, credit, funding and servicing. Define the stream, provider roles, settlement path and evidence required for your deployment.',
  'status_title':'Research implementation','status_body':'The repository contains a deterministic Rust state machine and application-owned integration modules. Aethel has not been audited for production use.',
  'limits_title':'Scope a pilot explicitly','limits_body':'Qualification is scope-pseudonymous. Guarantee claims and releases currently use full-cover transitions. Asset custody and settlement, provider onboarding and the legal treatment of receivables require deployment-specific evaluation.',
  'docs':'Enterprise PoC guide (Japanese)','source':'Explore the source',
  'brand':'Aethel is a payment-stream receivables application in the zkFMI stack, developed under the æmeth (Aemeth) project brand.',
  'footer':'Payment streams, composed.','skip':'Skip to content',
 },
 'ja': {
  'title':'Aethel — 支払ストリームを、資金調達可能な債権へ',
  'description':'Aethelは署名付き支払ストリームを債権に変え、独立した事業者による与信・保証・資金供給・回収管理を組み合わせるzkFMIのアプリケーションです。',
  'nav':['プロダクト','債権の流れ','提供者の役割','実証・評価'],
  'label':'AETHEL / A ZKFMI APPLICATION',
  'headline':'支払ストリームを、<br>資金調達可能な債権へ。',
  'intro':'Aethelは署名付きの支払ストリームを債権に変え、独立した事業者による与信評価・保証・資金供給・回収管理を組み合わせます。',
  'cta':'債権の流れを見る','secondary':'仕様を読む',
  'note':'支払義務をプログラムで扱い、役割を明確にし、zkFMIの決済につなぐ。',
  'focus':'プロダクト','focus_title':'支払の流れ自体を、<br>債権として扱う。',
  'focus_body':'中心にあるのは支払義務です。資金調達の対象となるストリームを定義し、与信判断と保証を同じ債権に結び付け、状態の変化をバージョン付きで記録します。',
  'features':[
   ('署名付き支払ストリーム','条件・バージョン・認可を明示して支払ストリームを登録。適格なストリームを、明示的な方針を持つ債権シリーズにまとめます。'),
   ('独立した金融サービス提供者','与信評価者、保証者、資金供給者を組み合わせます。各者の責任と署名付きのコミットメントを分けて扱います。'),
   ('証跡と結び付いた決済','債権発行や保証請求をzkPI決済指図とDeFMIにつなぎます。ホストが決済証跡を検証した後に、対応する状態を確定します。')],
  'lifecycle':'債権のライフサイクル','life_title':'一つの支払義務を、<br>追跡できる判断へ。',
  'life_body':'コアの状態機械が、債権の業務上の意味を記録します。外部の事業者と決済システムは、明示的なインターフェースで接続します。',
  'stages':[('登録','支払ストリームを証明し、対象となる債権シリーズを定義します。'),('与信・保証','署名付き与信判断と保証コミットメントを債権の文脈に結び付けます。'),('資金供給・発行','資金供給見積を比較し、債権を発行。資産の移転を決済に接続します。'),('回収管理','支払証跡、延滞、解消、許可された回収管理上の操作を記録します。'),('完済・保証請求','完済した支払義務を終了するか、不履行証跡を保証請求と損失配賦に結び付けます。')],
  'boundary':'Aethelは支払義務とその状態を記録します。現金・証券・法的権原を保有しません。資産決済の正本はDeFMIが担い、法的な取扱いは導入ごとに定義します。',
  'provider_label':'開かれた提供者モデル','provider_title':'役割ごとに、<br>権限を明確にする。',
  'provider_body':'与信判断は保証にはならず、保証の権限は資金供給の権限を意味しません。各提供者は限定された役割で登録され、停止・失効・鍵更新を管理できます。',
  'roles':[('ストリーム証明者','支払ストリームとその更新を証明します。'),('与信評価者','対象の債権に対する与信判断へ署名します。'),('保証者','外部の保証枠に裏付けられた保証を約束します。'),('資金供給者','資金供給の見積を提示します。'),('回収管理者','認可された回収管理上の操作を実行します。'),('資格発行者','資格の発行者鍵を承認します。')],
  'integration_title':'zkFMIを通じて接続',
  'integration_body':'DeKYXが資格確認、DeCCPが保証枠と残容量、zkPIが決済指図、DeFMIが資産・資金の決済を担当します。Aethelのホストが、これらのモジュールを業務状態につなぎます。',
  'evaluate_label':'実証・評価','evaluate_title':'資金調達したい<br>支払義務を起点に。',
  'evaluate_body':'債権の組成・与信・資金供給・回収管理の担当者と、ソースコードと企業向けPoCガイドをご覧ください。支払ストリーム、提供者の役割、決済経路、必要な証跡を導入ごとに定義します。',
  'status_title':'現在は研究実装','status_body':'リポジトリには決定論的なRustの状態機械と、アプリケーション側の接続モジュールがあります。本番利用に向けた監査は未実施です。',
  'limits_title':'実証の範囲を明示する','limits_body':'資格確認はスコープ内の仮名性を前提とします。保証請求・解放は現在、全額を対象とする状態遷移です。資産の保管と決済、提供者の参加、債権の法的取扱いは、導入ごとに評価が必要です。',
  'docs':'企業向けPoCガイド','source':'ソースコードを見る',
  'brand':'Aethelは、æmeth（Aemeth）が開発するzkFMI体系の、支払ストリーム債権アプリケーションです。',
  'footer':'支払ストリームを、組み合わせる。','skip':'本文へ移動',
 }
}

def render(lang):
 d=COPY[lang]; ja=lang=='ja'; p='../' if ja else './'; path='/ja/' if ja else '/'
 tech='https://zkfmi.com/'+('ja/' if ja else '')
 nav=''.join(f'<a href="#{key}">{label}</a>' for key,label in zip(['product','lifecycle','providers','evaluate'],d['nav']))
 features=''.join(f'<article class="case"><span class="number">0{i}</span><h3>{title}</h3><p>{body}</p></article>' for i,(title,body) in enumerate(d['features'],1))
 stages=''.join(f'<li><span class="number">0{i}</span><h3>{title}</h3><p>{body}</p></li>' for i,(title,body) in enumerate(d['stages'],1))
 roles=''.join(f'<div><dt>{title}</dt><dd>{body}</dd></div>' for title,body in d['roles'])
 return f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(d['title'])}</title><meta name="description" content="{escape(d['description'])}"><link rel="canonical" href="{BASE}{path}"><link rel="alternate" hreflang="en" href="{BASE}/"><link rel="alternate" hreflang="ja" href="{BASE}/ja/"><link rel="alternate" hreflang="x-default" href="{BASE}/"><meta property="og:title" content="{escape(d['title'])}"><meta property="og:description" content="{escape(d['description'])}"><meta property="og:type" content="website"><meta property="og:url" content="{BASE}{path}"><meta name="theme-color" content="#006472"><link rel="icon" href="{p}favicon.svg"><link rel="stylesheet" href="{p}style.css"></head>
<body><a class="skip" href="#main">{d['skip']}</a><header class="shell header"><a class="wordmark" href="{p}">aethel<span class="wordmark-period">.</span></a><nav aria-label="{'メイン' if ja else 'Main'}">{nav}</nav><a class="language" lang="{'en' if ja else 'ja'}" hreflang="{'en' if ja else 'ja'}" href="{'../' if ja else './ja/'}">{'EN' if ja else '日本語'}</a></header>
<main id="main"><section class="shell hero"><p class="eyebrow">{d['label']}</p><h1>{d['headline']}</h1><p class="intro">{d['intro']}</p><div class="actions"><a class="button" href="#lifecycle">{d['cta']} <span aria-hidden="true">↗</span></a><a class="text-link" href="https://github.com/zkFMI/aethel#readme">{d['secondary']} <span aria-hidden="true">↗</span></a></div><p class="hero-note">{d['note']}</p></section>
<section id="product" class="section shell"><div class="section-heading"><p class="eyebrow">{d['focus']}</p><div><h2>{d['focus_title']}</h2><p class="section-intro">{d['focus_body']}</p></div></div><div class="cases">{features}</div></section>
<section id="lifecycle" class="technology"><div class="shell"><div class="section-heading"><p class="eyebrow">{d['lifecycle']}</p><div><h2>{d['life_title']}</h2><p class="section-intro">{d['life_body']}</p></div></div><ol class="lifecycle">{stages}</ol><p class="caption">{d['boundary']}</p></div></section>
<section id="providers" class="section shell"><div class="section-heading"><p class="eyebrow">{d['provider_label']}</p><div><h2>{d['provider_title']}</h2><p class="section-intro">{d['provider_body']}</p></div></div><dl class="roles">{roles}</dl><div class="avalanche"><h3>{d['integration_title']}</h3><p>{d['integration_body']}</p></div></section>
<section id="evaluate" class="collaborate"><div class="shell"><div class="section-heading"><p class="eyebrow">{d['evaluate_label']}</p><div><h2>{d['evaluate_title']}</h2><p class="section-intro">{d['evaluate_body']}</p></div></div><div class="evidence-grid"><article><h3>{d['status_title']}</h3><p>{d['status_body']}</p></article><article><h3>{d['limits_title']}</h3><p>{d['limits_body']}</p></article></div><div class="actions"><a class="button" href="https://github.com/zkFMI/aethel/blob/main/docs/ENTERPRISE_POC_JA.md">{d['docs']} <span aria-hidden="true">↗</span></a><a class="text-link" href="https://github.com/zkFMI/aethel">{d['source']} <span aria-hidden="true">↗</span></a></div></div></section></main>
<footer class="shell footer"><div><a class="wordmark" href="{p}">aethel<span class="wordmark-period">.</span></a><p>{d['footer']}</p></div><p class="brand-note">{d['brand']} <a href="https://zkfmi.github.io/aemeth/">æmeth</a></p><div class="footer-end"><span>© 2026 Aethel / Aemeth</span><a href="{tech}">zkfmi.com</a><a href="https://github.com/zkFMI/aethel">GitHub</a></div></footer></body></html>'''

if __name__=='__main__':
 OUT.mkdir(exist_ok=True); (OUT/'ja').mkdir(exist_ok=True)
 (OUT/'index.html').write_text(render('en')); (OUT/'ja/index.html').write_text(render('ja'))
 for name in ('style.css','favicon.svg'): shutil.copyfile(ROOT/'static'/name,OUT/name)
 (OUT/'.nojekyll').touch()
 (OUT/'version.txt').write_text(os.environ.get('GITHUB_SHA','local-preview')+'\n')
 (OUT/'404.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found — Aethel</title><h1>Page not found</h1><a href="'+BASE+'/">Return to Aethel</a></html>')
 (OUT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+BASE+'/sitemap.xml\n')
 (OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+BASE+p+'</loc></url>' for p in ('/','/ja/'))+'</urlset>')
 print('Built Aethel English and Japanese pages')
