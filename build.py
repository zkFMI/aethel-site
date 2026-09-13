"""Build Aethel's English and Japanese product pages without dependencies.

python3 build.py  ->  public/  (English at /, Japanese at /ja/)
"""
from pathlib import Path
from html import escape
import os
import shutil

ROOT = Path(__file__).parent
OUT = ROOT / 'public'
BASE = (os.environ.get('SITE_URL') or 'https://aethel.fi').rstrip('/')
ZK = 'https://zkfmi.com/'
AEMETH = 'https://aemeth.fi/'
REPO = 'https://github.com/zkFMI/aethel'
POC = REPO + '/blob/main/docs/ENTERPRISE_POC_JA.md'

MARK = ('<svg viewBox="0 0 32 32" aria-hidden="true">'
        '<rect class="b" x="2" y="18" width="4" height="10" rx="1"/><rect class="b" x="8" y="13" width="4" height="15" rx="1"/>'
        '<rect class="b" x="14" y="8" width="4" height="20" rx="1"/><rect class="k" x="22" y="4" width="8" height="24" rx="2"/></svg>')


def wm():
    return f'<span class="wm">{MARK}aethel</span>'


COPY = {
 'en': {
  'title': 'Aethel — the payment stream is the receivable',
  'description': 'Aethel turns a payment stream both parties have signed into a receivable that independent credit assessors, guarantors, liquidity providers and servicers act on with separately signed authority, and settles it through a pluggable settlement rail, zkFMI first, without holding the cash.',
  'nav': [('product', 'Product'), ('lifecycle', 'Lifecycle'), ('providers', 'Providers'), ('boundaries', 'Boundaries'), ('pilot', 'Pilot'), ('status', 'Status')],
  'eyebrow': 'Aethel · a zkFMI application', 'by': 'by æmeth',
  'h1': 'The payment stream is the receivable.',
  'lede': 'Aethel takes a payment stream that both parties have signed and turns it into a receivable that independent credit assessors, guarantors, liquidity providers and servicers can act on, each with its own signed authority. It settles through a pluggable settlement rail, zkFMI being the first, and never holds the cash.',
  'cta': 'See the lifecycle', 'cta2': 'Enterprise PoC guide',
  'side_b': 'Built for the teams who run origination, credit, funding and servicing.',
  'side': 'Nothing here is a marketplace or a lender. Aethel is the state machine those teams plug their own providers into, and the record they can audit afterwards.',
  'hero_note': ['Rust state machine', '12 crates', 'Research implementation', 'Not audited'],
  'dg': {
    'stream_lbl': 'SIGNED PAYMENT STREAM', 'stream_id': 'strm-8f2c · v3', 'stream_sig': 'signed: obligor · creditor', 'stream_att': 'attested by StreamAttestor',
    'ticks': ['M+1', 'M+2', 'M+3', 'M+4', 'M+5', 'M+6'],
    'rcv_lbl': 'RECEIVABLE', 'rcv_id': 'rcv-0142 · series S-07', 'rcv_pol': 'policy: guarantee required · DeKYX qualification',
    'att': [('CreditDecision', 'signed · valid to 2026-10-01', 'CreditAssessor'), ('GuaranteeCommitment', 'committed · amount confidential', 'Guarantor · DeCCP hold'), ('FundingQuote', 'accepted', 'LiquidityProvider')],
    'set_lbl': 'SETTLEMENT', 'set_1': 'zkPI instruction', 'set_1b': 'typed · nullifier · proof', 'set_2': 'DeFMI settles', 'set_2b': 'both legs, or neither',
    'set_ev': 'evidence validated by host', 'set_state': 'Aethel state → Issued',
    'out_paid': 'paid → Closed', 'out_def': 'default → GuaranteeClaim → DeCCP',
    'cap': 'One receivable, four signatures from four providers, one settlement. Aethel keeps the meaning; DeFMI moves the value.',
  },
  'dg_list': [
    ('Signed payment stream', 'Both parties sign the schedule and terms; an attestor confirms it. Every update is a new version.'),
    ('Receivable', 'A series policy admits the stream. A credit decision, a guarantee and a funding quote attach, each signed by a different provider and bound to this receivable only.'),
    ('Settlement', 'Issuance becomes a typed zkPI instruction. DeFMI settles it and Aethel records the evidence. Paid closes it; default binds a guarantee claim.'),
  ],

  'prod_eb': 'What Aethel is', 'prod_h2': 'Not another ledger of invoices. A state machine for obligations.',
  'prod_p': 'Aethel does not hard-code a lender, a rating model, a guarantor or a marketplace. It records what a payment stream means commercially, who has decided what about it and where each decision stands, and hands anything that moves value to the settlement layer.',
  'prod_cards': [
    ('01', 'Signed, versioned streams', 'A stream is registered with its terms, a version and both signatures. Updates are new versions; a stale version cannot be financed, and the same obligation cannot be registered twice under another identifier.', 'blue'),
    ('02', 'Series with a policy', 'A receivable series says which streams may be financed and under what rules: whether a guarantee is required, which qualifications the counterparty must prove, what expires when.', 'amber'),
    ('03', 'Decisions bound to one context', 'A credit decision, a guarantee and a funding quote each carry the exact receivable, a validity window, a nonce and the provider’s signature. None of them can be replayed for another receivable.', 'teal'),
  ],

  'life_eb': 'Lifecycle', 'life_h2': 'Five stages. Every transition has a reason to refuse.',
  'life_p': 'The core is deterministic: the same inputs always produce the same state. What makes it useful is what it rejects.',
  'stages': [
    ('01 · Register', 'Attest the stream, open a series', 'The stream attestor confirms the payment stream and its updates. A series defines which streams are eligible and under what policy.', ['unsigned stream, or a version that does not match', 'the same obligation registered twice']),
    ('02 · Assess & cover', 'Signed decisions, committed cover', 'A credit assessor signs a decision for this receivable. A guarantor commits coverage backed by a DeCCP facility; the amount can stay confidential.', ['expired decision', 'policy requires a guarantee and none is attached', 'artifact signed under the wrong capability']),
    ('03 · Fund & issue', 'Quotes compete, the receivable is issued', 'Liquidity providers submit executable quotes. Issuance creates a typed zkPI instruction; DeFMI settles it and Aethel records the evidence.', ['final state before settlement evidence', 'quote from an unregistered provider', 'supply above the obligation']),
    ('04 · Service', 'Evidence in, state out', 'Payment evidence, delinquency, cure and permitted servicing actions are recorded by the servicer. A retried request applies once.', ['the same settlement result applied twice', 'servicing action outside the capability']),
    ('05 · Close or claim', 'Paid closes. Default claims.', 'A paid obligation closes the receivable. A default attestation binds evidence to a guarantee claim; loss allocation runs in DeCCP, settlement in DeFMI.', ['claim without a default attestation', 'release by an unauthorised provider']),
  ],
  'refuses': 'Refused',
  'states_lbl': 'records', 'states': ['RegisteredStream', 'ReceivableSeries', 'CreditDecision', 'GuaranteeCommitment', 'FundingQuote', 'ReceivableIssuance', 'DefaultAttestation', 'GuaranteeClaim', 'ProviderDefinition'],

  'prov_eb': 'Open provider model', 'prov_h2': 'Six capabilities. None implies another.',
  'prov_p': 'Providers register with narrowly scoped capabilities and sign only the artifacts they are responsible for. A credit assessment cannot quietly act as a guarantee; a guarantor cannot issue a funding quote unless separately authorised. One company may hold several capabilities, each granted and revoked on its own.',
  'mx_cols': ['Stream attestation', 'Credit decision', 'Guarantee', 'Funding quote', 'Servicing action', 'Issuer vouch'],
  'mx_rows': [('StreamAttestor', 'attests a stream and its updates'), ('CreditAssessor', 'signs a decision for one receivable'), ('Guarantor', 'commits cover from an external facility'), ('LiquidityProvider', 'submits an executable funding quote'), ('Servicer', 'performs permitted servicing actions'), ('CredentialIssuer', 'vouches for a DeKYX issuer key, nothing else')],
  'mx_cap': 'A filled dot is the only artifact that capability may sign. Everything else is refused at the state transition, not by convention.',
  'chips': ['<b>register</b> → active → suspended → revoked', 'key rotation: old signatures stay verifiable, new ones under the retired key are refused', 'DeKYX presentation can be required before a decision or guarantee is accepted'],

  'bd_eb': 'Where things live', 'bd_h2': 'Aethel holds the meaning. Everything else stays where it is authoritative.',
  'bd_p': 'A receivable touches money, identity, guarantees and tokens. Aethel keeps one copy of each, in the system that is the record for it, and stores only references and digests. The same balance, qualification or facility is never copied into a second ledger.',
  'sor_h': ['Information', 'System of record', 'What Aethel keeps'],
  'sor': [
    ('Payment stream, series, remaining principal', '<b>Aethel</b>', 'both signatures, versions, terms, current state'),
    ('Credit decision', 'the assessor signs · <b>Aethel</b> accepts as state', 'signed decision, target, version, validity, provider reference'),
    ('Legal name, registration number, KYB evidence', '<b>DeKYX</b> issuer', 'pseudonymous subject reference and a qualification digest'),
    ('Guarantee facility and remaining capacity', '<b>DeCCP</b> or the guarantor', 'opaque hold id and commitment; a settlement digest on release or claim'),
    ('Token holdings per holder', '<b>DeFMI</b> or another asset ledger', 'supply caps and mint/burn intents with the ledger receipt; no per-holder balances'),
    ('Cash, securities, collateral', '<b>DeFMI</b>', 'note, lock and settlement references; the confirmed root'),
    ('Settlement instruction', '<b>zkPI</b>', 'instruction id, nullifier, domain, proof and signature summary'),
  ],
  'conf': [
    ('Anonymous qualification', 'A series can require a DeKYX presentation before a decision or guarantee is accepted. It is bound to this domain, action, artifact statement, nonce and expiry, so a proof for one decision cannot be replayed for another. Aethel keeps only the verified subject-line binding, never a legal name.', 'blue'),
    ('Confidential cover', 'The guarantee amount may stay confidential. Aethel and DeCCP then exchange commitments, state digests, identifiers and verified transition receipts instead of a plaintext amount.', 'amber'),
    ('Settlement with evidence', 'Issuance, releases and claims are verified by the settlement rail before the book moves. On zkFMI they become typed zkPI instructions that DeFMI settles; on the attested rail an operator-signed settlement is the witness. Aethel never advances on its own say-so.', 'teal'),
  ],

  'pilot_eb': 'Enterprise PoC', 'pilot_h2': 'Run it with your own roles, your own keys, and the failures you expect.',
  'pilot_p': 'The PoC guide walks from a signed stream to settlement, lists the failure cases that must be refused, the evidence to keep and example acceptance criteria. Roles are separated by key even when one team plays all of them; otherwise the separation of authority cannot be tested.',
  'scen_h': 'The minimal scenario',
  'scen': ['Create a payment stream both parties sign, with subject references instead of raw identities', 'Register credit providers: keys, qualification conditions, decision validity, model version', 'Compose the receivable: matching version, unexpired decision, guarantee where the policy requires one', 'Fund and tokenise: supply never above the obligation, no reuse of redeemed rights', 'Service and collect: retries apply once, outcomes flow to holders once', 'Settle through zkPI and DeFMI; Aethel finalises only on confirmed evidence'],
  'fail_h': 'Must be refused',
  'fail': ['financing after the credit decision expired', 'issuing a guarantee-required product without a guarantee', 'a guarantee released by an unauthorised provider', 'acquiring tokens with a revoked qualification', 'the same stream registered twice under another identifier', 'a new decision signed with a rotated-out key', 'the same settlement result received twice', 'tokens above the remaining obligation'],
  'acc_h': 'Acceptance, at minimum',
  'acc': ['authority for credit, guarantee and funding is independent', 'a required guarantee cannot be substituted by a credit decision', 'DeKYX revocation and key rotation reach new operations', 'if zkPI or DeFMI fails, Aethel’s settlement state does not finalise', 'after a retry, one business request applies exactly once', 'every material transition audits back to the input version and signature'],
  'pilot_a': 'Enterprise PoC guide (Japanese)', 'pilot_b': 'Source', 'pilot_c': 'Aethel on zkfmi.com',

  'st_eb': 'Status and limits', 'st_h2': 'A research implementation, with the edges marked.',
  'limits': [
    'Not audited for production use.',
    'Aethel is an embeddable state machine, not a server. The host application supplies authenticated APIs, persistence, concurrency control, key management, and a settlement rail and qualification port. The repository ships two of each: zkFMI (zkPI, DeFMI, DeCCP, DeKYX) and an attested rail backed by operator-signed records that depends on no zkFMI crate.',
    'Qualification is scope-pseudonymous, not issuer-unlinkable. Cross-issuer anti-Sybil policy is a governance decision outside the crate.',
    'Guarantee claims and releases are full-cover transitions; partial cover needs an extended state model.',
    'Legal assignment, perfection, tax, accounting and bankruptcy treatment of a receivable are outside the code and specific to each deployment.',
    'Passing the build gates is not a substitute for an independent cryptographic, financial, state-machine, host and integration audit.',
  ],
  'gates': ['cargo test --workspace --locked', 'cargo clippy --workspace --all-targets --locked -- -D warnings', 'cargo fmt --all -- --check', 'cargo build --workspace --release --locked'],
  'gates_note': '# the four gates, on Linux with the locked dependency graph',

  'f_tag': 'Payment streams, composed.',
  'f_note': 'Aethel is a payment-stream receivables application in the zkFMI stack, developed by',
  'skip': 'Skip to content', 'lang': '日本語', 'lang_href': 'ja/', 'lang_code': 'ja', 'navlabel': 'Main',
 },
 'ja': {
  'title': 'Aethel — 支払の流れが、そのまま債権になる',
  'description': 'Aethelは、両当事者が署名した支払ストリームを債権に変え、独立した与信評価者・保証者・資金供給者・回収管理者がそれぞれ署名した権限で関わる仕組みです。決済は差し替え可能な決済レール（最初はzkFMI）で行い、Aethel自身は資金を保有しません。',
  'nav': [('product', 'プロダクト'), ('lifecycle', '債権の流れ'), ('providers', '提供者の権限'), ('boundaries', '正本の所在'), ('pilot', '企業PoC'), ('status', '現状と限界')],
  'eyebrow': 'Aethel · zkFMI アプリケーション', 'by': 'æmeth 開発',
  'h1': '支払の流れが、そのまま債権になる。',
  'lede': 'Aethelは、両当事者が署名した支払ストリームを債権に変えます。独立した与信評価者・保証者・資金供給者・回収管理者が、それぞれ自分で署名した権限の範囲で関わります。決済は差し替え可能な決済レール（最初はzkFMI）で行い、Aethel自身は資金を保有しません。',
  'cta': '債権の流れを見る', 'cta2': '企業向けPoCガイド',
  'side_b': '債権の組成・与信・資金供給・回収を実際に担当するチームのために。',
  'side': 'ここにあるのは、マーケットプレイスでも貸し手でもありません。担当チームが自社の提供者を接続する状態機械であり、あとから監査できる記録です。',
  'hero_note': ['Rust の状態機械', '12 クレート', '研究実装', '監査未実施'],
  'dg': {
    'stream_lbl': '署名済み支払ストリーム', 'stream_id': 'strm-8f2c · v3', 'stream_sig': '署名: 支払義務者 · 債権者', 'stream_att': 'StreamAttestor が証明',
    'ticks': ['M+1', 'M+2', 'M+3', 'M+4', 'M+5', 'M+6'],
    'rcv_lbl': '債権', 'rcv_id': 'rcv-0142 · series S-07', 'rcv_pol': '方針: 保証必須 · DeKYX 資格',
    'att': [('CreditDecision', '署名済 · 2026-10-01 まで有効', 'CreditAssessor'), ('GuaranteeCommitment', '約束済 · 金額は秘匿', 'Guarantor · DeCCP hold'), ('FundingQuote', '受諾', 'LiquidityProvider')],
    'set_lbl': '決済', 'set_1': 'zkPI 指図', 'set_1b': '型付き · nullifier · 証明', 'set_2': 'DeFMI が決済', 'set_2b': '両方動くか、どちらも動かない',
    'set_ev': 'ホストが証跡を検証', 'set_state': 'Aethel の状態 → Issued',
    'out_paid': '完済 → Closed', 'out_def': '不履行 → GuaranteeClaim → DeCCP',
    'cap': '一つの債権に、四つの提供者の四つの署名、一つの決済。Aethelは意味を持ち、DeFMIが価値を動かす。',
  },
  'dg_list': [
    ('署名済み支払ストリーム', '両当事者が支払予定と条件に署名し、証明者が確認します。更新はすべて新しい版になります。'),
    ('債権', 'シリーズの方針がストリームを受け入れます。与信判断・保証・資金供給見積が、それぞれ別の提供者の署名付きで、この債権だけに結び付きます。'),
    ('決済', '発行は型付きのzkPI指図になります。DeFMIが決済し、Aethelは証跡を記録します。完済で終了し、不履行なら保証請求に結び付けます。'),
  ],

  'prod_eb': 'Aethel とは', 'prod_h2': '請求書の台帳ではなく、支払義務の状態機械。',
  'prod_p': 'Aethelは、貸し手・格付けモデル・保証者・市場を固定しません。支払ストリームが業務上何を意味し、誰がそれについて何を決め、各判断が今どの状態にあるかを記録し、価値を動かす処理はすべて決済層へ渡します。',
  'prod_cards': [
    ('01', '署名付きで版管理されたストリーム', '条件・版・両当事者の署名とともにストリームを登録します。更新は新しい版になり、古い版は資金調達に使えず、同じ支払義務を別の識別子で二重登録することもできません。', 'blue'),
    ('02', '方針を持つシリーズ', '債権シリーズが、どのストリームをどの規則で資金調達してよいかを定めます。保証が必須か、相手方がどの資格を証明すべきか、何がいつ失効するか。', 'amber'),
    ('03', '一つの文脈に結び付いた判断', '与信判断・保証・資金供給見積は、対象の債権、有効期間、nonce、提供者の署名を持ちます。どれも別の債権へ使い回せません。', 'teal'),
  ],

  'life_eb': '債権の流れ', 'life_h2': '五つの段階。どの遷移にも、拒否する理由がある。',
  'life_p': 'コアは決定的です。同じ入力からは必ず同じ状態になります。役に立つのは、何を拒否するかが決まっているからです。',
  'stages': [
    ('01 · 登録', 'ストリームを証明し、シリーズを開く', 'ストリーム証明者が支払ストリームとその更新を確認します。シリーズが、対象となるストリームと方針を定めます。', ['署名のないストリーム、版の不一致', '同じ支払義務の二重登録']),
    ('02 · 与信と保証', '署名付きの判断、約束された保証', '与信評価者がこの債権への判断に署名します。保証者がDeCCPの保証枠に裏付けられた保証を約束します。金額は秘匿できます。', ['期限切れの判断', '方針が保証を求めるのに保証がない', '権限の異なる署名']),
    ('03 · 資金供給と発行', '見積が競い、債権が発行される', '資金供給者が実行可能な見積を出します。発行は型付きのzkPI指図になり、DeFMIが決済し、Aethelが証跡を記録します。', ['決済証跡より先の確定', '未登録の提供者からの見積', '支払義務を超える発行']),
    ('04 · 回収管理', '証跡が入り、状態が出る', '支払証跡、延滞、解消、許可された回収操作を回収管理者が記録します。再試行された依頼は一度だけ反映されます。', ['同じ決済結果の二重反映', '権限外の回収操作']),
    ('05 · 完済または請求', '完済なら終了。不履行なら請求。', '完済した支払義務は債権を終了します。不履行の証明が保証請求に結び付き、損失配賦はDeCCPで、決済はDeFMIで行われます。', ['不履行証明のない請求', '権限のない提供者による解放']),
  ],
  'refuses': '拒否されるもの',
  'states_lbl': '記録', 'states': ['RegisteredStream', 'ReceivableSeries', 'CreditDecision', 'GuaranteeCommitment', 'FundingQuote', 'ReceivableIssuance', 'DefaultAttestation', 'GuaranteeClaim', 'ProviderDefinition'],

  'prov_eb': '開かれた提供者モデル', 'prov_h2': '六つの権限。どれも他を含意しない。',
  'prov_p': '提供者は狭く限定された権限で登録され、自分が責任を持つ成果物にだけ署名します。与信判断が黙って保証として振る舞うことはなく、保証者が別途認可なしに資金供給見積を出すこともできません。一社が複数の権限を持ってもよく、それぞれ個別に付与・失効します。',
  'mx_cols': ['ストリーム証明', '与信判断', '保証', '資金供給見積', '回収操作', '発行者の承認'],
  'mx_rows': [('StreamAttestor', 'ストリームとその更新を証明する'), ('CreditAssessor', '一つの債権への判断に署名する'), ('Guarantor', '外部の保証枠から保証を約束する'), ('LiquidityProvider', '実行可能な資金供給見積を出す'), ('Servicer', '許可された回収操作を行う'), ('CredentialIssuer', 'DeKYXの発行者鍵を承認する。それ以外は何もしない')],
  'mx_cap': '塗りつぶした点が、その権限で署名できる唯一の成果物です。それ以外は慣習ではなく状態遷移で拒否されます。',
  'chips': ['<b>登録</b> → 有効 → 停止 → 失効', '鍵更新: 旧鍵の署名は検証でき、旧鍵での新しい署名は拒否', '判断や保証の受理前にDeKYXの提示を必須にできる'],

  'bd_eb': '正本の所在', 'bd_h2': 'Aethelは意味を持つ。それ以外は、正本のある場所に置いたまま。',
  'bd_p': '債権には、資金・本人性・保証・トークンが関わります。Aethelはそれぞれを一箇所、正本となるシステムにだけ置き、自分は参照とダイジェストだけを保存します。同じ残高・資格・保証枠を二つ目の台帳へ複製しません。',
  'sor_h': ['情報', '正本', 'Aethelが保存するもの'],
  'sor': [
    ('支払ストリーム、シリーズ、残存元本', '<b>Aethel</b>', '両当事者の署名、版、条件、現在の状態'),
    ('与信判断', '評価者が署名 · <b>Aethel</b>が状態として受理', '署名付き判断、対象、版、有効期限、提供者参照'),
    ('法的名称、登録番号、KYB証跡', '<b>DeKYX</b> 発行者', '仮名の主体参照と資格のダイジェスト'),
    ('保証枠と残容量', '<b>DeCCP</b> または保証者', 'opaqueなhold IDとcommitment。解放・請求時はsettlement digest'),
    ('保有者別のトークン残高', '<b>DeFMI</b> 等の外部asset ledger', '発行上限とmint/burnのintent、ledgerのreceipt。保有者別残高は持たない'),
    ('資金、証券、担保', '<b>DeFMI</b>', 'note・lock・settlementの参照と確定root'),
    ('決済指図', '<b>zkPI</b>', '指図ID、nullifier、domain、証明と署名の要約'),
  ],
  'conf': [
    ('匿名の資格確認', '判断や保証を受理する前に、シリーズがDeKYXの提示を必須にできます。提示はこのドメイン・行為・成果物の文・nonce・期限に結び付くので、ある判断のための証明を別の判断へ使い回せません。Aethelは検証済みの主体参照だけを持ち、法的名称は持ちません。', 'blue'),
    ('秘匿された保証', '保証額は秘匿できます。その場合、AethelとDeCCPは平文の金額ではなく、commitment・状態ダイジェスト・識別子・検証済みの遷移receiptを交換します。', 'amber'),
    ('証跡と引き換えの決済', '発行・解放・請求は、Bookが動く前に決済レールが検証します。zkFMIでは型付きのzkPI指図になりDeFMIが決済し、attestedレールではオペレーターが署名した決済記録が証跡になります。Aethelが自分の判断だけで先へ進むことはありません。', 'teal'),
  ],

  'pilot_eb': '企業向けPoC', 'pilot_h2': '自社の役割と鍵で動かし、想定する失敗をぶつける。',
  'pilot_p': 'PoCガイドは、署名済みストリームから決済までの最小シナリオ、拒否されなければならない失敗系、保存すべき証拠、受入基準の例を示します。一つのチームが全役割を演じる場合でも、鍵は役割ごとに分けます。分けなければ権限分離を検証できないからです。',
  'scen_h': '最小シナリオ',
  'scen': ['両当事者が署名する支払ストリームを作る。生の本人情報ではなく主体参照を使う', '与信事業者を登録する。鍵、資格条件、判断の有効期限、モデルの版', '債権を組成する。版の一致、期限内の判断、方針が求める保証', '資金供給とトークン化。発行総数は支払義務を超えず、償還済みの権利は再利用しない', '回収管理。再試行は一度だけ反映され、結果は保有者へ一度だけ配分される', 'zkPIとDeFMIで決済する。Aethelは確定した証跡を受けてから確定する'],
  'fail_h': '拒否されなければならないもの',
  'fail': ['与信判断の期限切れ後の債権化', '保証必須の商品を保証なしで発行', '権限のない事業者による保証の解除', '失効したDeKYX資格でのトークン取得', '同じストリームを別の識別子で二重登録', '更新前の鍵による新しい与信判断への署名', '同じ決済結果の二回受信', '残存する支払義務を超えるトークン発行'],
  'acc_h': '受入基準（最低限）',
  'acc': ['与信・保証・資金供給の権限が独立している', '方針が求める保証を与信判断で代替できない', 'DeKYXの失効・鍵更新が新しい処理へ反映される', 'zkPIまたはDeFMIが失敗した場合、Aethelの決済状態が確定しない', '再試行後も一つの業務依頼が一度だけ反映される', 'すべての重要な状態遷移を、入力の版と署名まで遡って監査できる'],
  'pilot_a': '企業向けPoCガイド', 'pilot_b': 'ソースコード', 'pilot_c': 'zkfmi.com の Aethel',

  'st_eb': '現状と限界', 'st_h2': '研究実装。境界は明記してある。',
  'limits': [
    '本番利用に向けた監査は未実施です。',
    'Aethelは組み込み可能な状態機械であり、サーバーではありません。認証済みAPI、永続化、同時実行制御、鍵管理、そして決済レールと資格確認ポートはホストアプリケーションが用意します。リポジトリには2組が入っています。zkFMI（zkPI・DeFMI・DeCCP・DeKYX）と、オペレーターの署名付き記録を証跡にする、zkFMIに依存しないattestedレールです。',
    '資格確認はスコープ内の仮名性であり、発行者間の非連結性はありません。発行者をまたぐSybil対策はクレートの外のガバナンス判断です。',
    '保証請求と解放は全額を対象とする遷移です。部分保証には拡張した状態モデルが必要です。',
    '債権譲渡の法的効力、対抗要件、税務、会計、倒産時の取扱いはコードの外にあり、導入ごとに定めます。',
    'ビルドの4ゲートに通ることは、暗号・金融・状態機械・ホスト・接続の独立した監査の代わりになりません。',
  ],
  'gates': ['cargo test --workspace --locked', 'cargo clippy --workspace --all-targets --locked -- -D warnings', 'cargo fmt --all -- --check', 'cargo build --workspace --release --locked'],
  'gates_note': '# 4つのゲート。Linux、固定した依存グラフで',

  'f_tag': '支払ストリームを、組み合わせる。',
  'f_note': 'Aethelは、zkFMI体系の支払ストリーム債権アプリケーションです。開発:',
  'skip': '本文へ移動', 'lang': 'EN', 'lang_href': '../', 'lang_code': 'en', 'navlabel': 'メイン',
 },
}


def diagram(d):
    g = d['dg']
    W, H = 1160, 400
    o = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="{escape(g["cap"])}">']
    # --- panel 1: signed payment stream -------------------------------------
    o.append('<rect class="panel" x="0" y="0" width="340" height="330" rx="14"/>')
    o.append(f'<text class="t-lbl" x="24" y="34">{escape(g["stream_lbl"])}</text>')
    o.append(f'<text class="t-id" x="24" y="58">{escape(g["stream_id"])}</text>')
    heights = [48, 62, 40, 74, 56, 66]
    base = 210
    o.append(f'<path class="axis" d="M24 {base} H316"/>')
    for i, (h, t) in enumerate(zip(heights, g['ticks'])):
        x = 34 + i * 47
        o.append(f'<rect class="bar" x="{x}" y="{base - h}" width="30" height="{h}" rx="3"/>')
        o.append(f'<text class="tick" x="{x + 15}" y="{base + 18}" text-anchor="middle">{escape(t)}</text>')
    o.append(f'<rect class="tag" x="24" y="246" width="292" height="26" rx="6"/>')
    o.append(f'<text class="tag-t" x="36" y="263">{escape(g["stream_sig"])}</text>')
    o.append(f'<text class="t-mute" x="24" y="300">{escape(g["stream_att"])}</text>')
    # arrow 1
    o.append('<path class="arrow" d="M348 165 H392 m-8 -6 l8 6 l-8 6"/>')
    # --- panel 2: receivable ------------------------------------------------
    o.append('<rect class="panel" x="404" y="0" width="380" height="330" rx="14"/>')
    o.append(f'<text class="t-lbl" x="428" y="34">{escape(g["rcv_lbl"])}</text>')
    o.append(f'<text class="t-id" x="428" y="58">{escape(g["rcv_id"])}</text>')
    o.append(f'<text class="t-mute" x="428" y="80">{escape(g["rcv_pol"])}</text>')
    for i, ((name, status, who), cls) in enumerate(zip(g['att'], ['blue', 'amber', 'teal'])):
        y = 100 + i * 66
        o.append(f'<rect class="att-{cls}" x="428" y="{y}" width="332" height="54" rx="8"/>')
        o.append(f'<circle class="c-{cls}" cx="446" cy="{y + 27}" r="5"/>')
        o.append(f'<text class="t-ttl" x="460" y="{y + 22}" style="font-size:14px">{escape(name)}</text>')
        o.append(f'<text class="t-sm" x="460" y="{y + 41}">{escape(status)}</text>')
        o.append(f'<text class="sig" x="748" y="{y + 22}" text-anchor="end">✎ {escape(who)}</text>')
    # arrow 2
    o.append('<path class="arrow" d="M792 165 H836 m-8 -6 l8 6 l-8 6"/>')
    # --- panel 3: settlement ------------------------------------------------
    o.append('<rect class="panel" x="848" y="0" width="312" height="330" rx="14"/>')
    o.append(f'<text class="t-lbl" x="872" y="34">{escape(g["set_lbl"])}</text>')
    o.append('<rect class="card" x="872" y="52" width="264" height="56" rx="8"/>')
    o.append(f'<path class="seal" d="M888 80 l8 -12 h20 l8 12 l-8 12 h-20 z"/>')
    o.append(f'<text class="t-ttl" x="936" y="76" style="font-size:14px">{escape(g["set_1"])}</text>')
    o.append(f'<text class="t-sm" x="936" y="95">{escape(g["set_1b"])}</text>')
    o.append('<path class="arrow-teal" d="M1004 112 V128 m-6 -8 l6 8 l6 -8"/>')
    o.append('<rect class="card" x="872" y="134" width="264" height="56" rx="8"/>')
    o.append('<circle class="c-teal" cx="898" cy="162" r="6"/>')
    o.append(f'<text class="t-ttl" x="936" y="158" style="font-size:14px">{escape(g["set_2"])}</text>')
    o.append(f'<text class="t-sm" x="936" y="177">{escape(g["set_2b"])}</text>')
    o.append(f'<text class="t-mute" x="872" y="218">✓ {escape(g["set_ev"])}</text>')
    o.append(f'<text class="t-id" x="872" y="240" style="fill:var(--teal)">{escape(g["set_state"])}</text>')
    o.append('<path class="axis" d="M872 258 H1136"/>')
    o.append('<circle class="c-teal" cx="880" cy="284" r="4"/>')
    o.append(f'<text class="t-sm" x="892" y="288">{escape(g["out_paid"])}</text>')
    o.append('<circle class="c-red" cx="880" cy="308" r="4"/>')
    o.append(f'<text class="t-sm" x="892" y="312">{escape(g["out_def"])}</text>')
    # bottom rail: who signed what
    o.append(f'<path class="axis" d="M0 356 H{W}" stroke-dasharray="2 4"/>')
    o.append(f'<text class="t-mute" x="0" y="386">{escape(g["cap"])}</text>')
    o.append('</svg>')
    return ''.join(o)


def render(lang):
    d = COPY[lang]
    ja = lang == 'ja'
    p = '../' if ja else './'
    path = '/ja/' if ja else '/'
    zk = ZK + ('ja/' if ja else '')
    nav = ''.join(f'<a href="#{k}">{escape(v)}</a>' for k, v in d['nav'])
    hero_note = ''.join(f'<span>{escape(s)}</span>' for s in d['hero_note'])
    dg_list = ''.join(f'<li><span class="kicker">0{i}</span><b>{escape(t)}</b><p>{escape(b)}</p></li>' for i, (t, b) in enumerate(d['dg_list'], 1))
    prod_cards = ''.join(f'<article class="cardx {cls}"><span class="num">{n}</span><h3>{escape(t)}</h3><p>{escape(b)}</p></article>' for n, t, b, cls in d['prod_cards'])
    stages = ''.join(
        f'<li><span class="num">{escape(n)}</span><h3>{escape(t)}</h3><p>{escape(b)}</p>'
        f'<div class="ref"><b>{escape(d["refuses"])}</b>{"".join(f"<span>{escape(r)}</span>" for r in refs)}</div></li>'
        for n, t, b, refs in d['stages'])
    states = f'<span class="lbl">{escape(d["states_lbl"])}</span>' + ''.join(f'<span>{s}</span>' for s in d['states'])
    mx_head = ''.join(f'<th>{escape(c)}</th>' for c in d['mx_cols'])
    mx_rows = ''.join(
        f'<tr><th class="row" scope="row"><code>{name}</code><small>{escape(desc)}</small></th>'
        + ''.join(f'<td><span class="dot{" on" if j == i else ""}" aria-label="{"yes" if j == i else "no"}"></span></td>' for j in range(6)) + '</tr>'
        for i, (name, desc) in enumerate(d['mx_rows']))
    chips = ''.join(f'<span class="chip">{c}</span>' for c in d['chips'])
    sor_head = ''.join(f'<th{" class=min" if i else ""}>{escape(h)}</th>' for i, h in enumerate(d['sor_h']))
    sor = ''.join(f'<tr><td>{escape(a)}</td><td>{b}</td><td>{escape(c)}</td></tr>' for a, b, c in d['sor'])
    conf = ''.join(f'<article class="cardx {cls}"><h3>{escape(t)}</h3><p>{escape(b)}</p></article>' for t, b, cls in d['conf'])
    scen = ''.join(f'<li>{escape(s)}</li>' for s in d['scen'])
    fail = ''.join(f'<li>{escape(s)}</li>' for s in d['fail'])
    acc = ''.join(f'<li>{escape(s)}</li>' for s in d['acc'])
    limits = ''.join(f'<li>{escape(s)}</li>' for s in d['limits'])
    gates = f'<span>{escape(d["gates_note"])}</span><br>' + '<br>'.join(escape(g) for g in d['gates'])
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(d['title'])}</title>
<meta name="description" content="{escape(d['description'])}">
<link rel="canonical" href="{BASE}{path}">
<link rel="alternate" hreflang="en" href="{BASE}/">
<link rel="alternate" hreflang="ja" href="{BASE}/ja/">
<link rel="alternate" hreflang="x-default" href="{BASE}/">
<meta property="og:title" content="{escape(d['title'])}">
<meta property="og:description" content="{escape(d['description'])}">
<meta property="og:type" content="website">
<meta property="og:url" content="{BASE}{path}">
<meta property="og:image" content="{BASE}/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#f7f8fa">
<link rel="icon" href="{p}favicon.svg" type="image/svg+xml">
<link rel="preload" href="{p}fonts/bricolage.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{p}style.css">
</head>
<body>
<a class="skip" href="#main">{escape(d['skip'])}</a>
<header class="top"><div class="wrap">
<a href="{p}" aria-label="Aethel home">{wm()}</a>
<nav aria-label="{escape(d['navlabel'])}">{nav}</nav>
<a class="lang" lang="{d['lang_code']}" hreflang="{d['lang_code']}" href="{d['lang_href']}">{escape(d['lang'])}</a>
</div></header>

<main id="main">
<section class="hero"><div class="wrap">
<div class="hero-grid">
<div>
<p class="eyebrow">{escape(d['eyebrow'])} <span class="by">· {escape(d['by'])}</span></p>
<h1>{escape(d['h1'])}</h1>
<p class="lede">{escape(d['lede'])}</p>
<div class="actions"><a class="btn primary" href="#lifecycle">{escape(d['cta'])} <span class="arr">↓</span></a><a class="btn" href="{POC}">{escape(d['cta2'])} <span class="arr">↗</span></a></div>
</div>
<div class="hero-side"><b>{escape(d['side_b'])}</b>{escape(d['side'])}</div>
</div>
<div class="diagram">{diagram(d)}</div>
<ol class="diagram-list">{dg_list}</ol>
<p class="hero-note">{hero_note}</p>
</div></section>

<section class="section" id="product"><div class="wrap">
<div class="head"><p class="eyebrow">{escape(d['prod_eb'])}</p><div><h2>{escape(d['prod_h2'])}</h2><p>{escape(d['prod_p'])}</p></div></div>
<div class="cards">{prod_cards}</div>
</div></section>

<section class="section night" id="lifecycle"><div class="wrap">
<div class="head"><p class="eyebrow">{escape(d['life_eb'])}</p><div><h2>{escape(d['life_h2'])}</h2><p>{escape(d['life_p'])}</p></div></div>
<ol class="stages">{stages}</ol>
<div class="states">{states}</div>
</div></section>

<section class="section" id="providers"><div class="wrap">
<div class="head"><p class="eyebrow">{escape(d['prov_eb'])}</p><div><h2>{escape(d['prov_h2'])}</h2><p>{escape(d['prov_p'])}</p></div></div>
<div class="matrix-wrap"><table class="matrix"><thead><tr><th></th>{mx_head}</tr></thead><tbody>{mx_rows}</tbody></table></div>
<p class="matrix-cap">{escape(d['mx_cap'])}</p>
<div class="chips">{chips}</div>
</div></section>

<section class="section bg-2" id="boundaries"><div class="wrap">
<div class="head"><p class="eyebrow">{escape(d['bd_eb'])}</p><div><h2>{escape(d['bd_h2'])}</h2><p>{escape(d['bd_p'])}</p></div></div>
<div class="sor-wrap"><table class="sor"><thead><tr>{sor_head}</tr></thead><tbody>{sor}</tbody></table></div>
<div class="conf">{conf}</div>
</div></section>

<section class="section" id="pilot"><div class="wrap">
<div class="head"><p class="eyebrow">{escape(d['pilot_eb'])}</p><div><h2>{escape(d['pilot_h2'])}</h2><p>{escape(d['pilot_p'])}</p></div></div>
<div class="pilot">
<div class="pane"><h3>{escape(d['scen_h'])}</h3><ol>{scen}</ol></div>
<div class="pane"><h3>{escape(d['fail_h'])}</h3><ul>{fail}</ul></div>
<div class="pane ok" style="grid-column:1/-1"><h3>{escape(d['acc_h'])}</h3><ul style="columns:2;column-gap:2.5rem">{acc}</ul></div>
</div>
<div class="actions pilot-actions"><a class="btn primary" href="{POC}">{escape(d['pilot_a'])} <span class="arr">↗</span></a><a class="btn" href="{REPO}">{escape(d['pilot_b'])} <span class="arr">↗</span></a><a class="btn" href="{zk}docs/aethel.html">{escape(d['pilot_c'])} <span class="arr">↗</span></a></div>
</div></section>

<section class="section bg-2" id="status"><div class="wrap">
<div class="head"><p class="eyebrow">{escape(d['st_eb'])}</p><div><h2>{escape(d['st_h2'])}</h2></div></div>
<ul class="limits">{limits}</ul>
<pre class="gates">{gates}</pre>
</div></section>
</main>

<footer><div class="wrap">
<div><a href="{p}" aria-label="Aethel home">{wm()}</a><p class="tag">{escape(d['f_tag'])}</p></div>
<p class="note">{escape(d['f_note'])} <a href="{AEMETH}{'ja/' if ja else ''}">æmeth (Aemeth)</a>.</p>
<div class="end"><span>© 2026 Aethel · æmeth</span><a href="{AEMETH}{'ja/' if ja else ''}">aemeth.fi</a><a href="{zk}">zkfmi.com</a><a href="{REPO}">GitHub</a></div>
</div></footer>
</body>
</html>
'''


def favicon():
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#2743c9"/>'
            '<rect x="12" y="38" width="7" height="16" rx="1.5" fill="#fff" opacity=".7"/><rect x="22" y="30" width="7" height="24" rx="1.5" fill="#fff" opacity=".85"/>'
            '<rect x="32" y="20" width="7" height="34" rx="1.5" fill="#fff"/><rect x="43" y="10" width="11" height="44" rx="3" fill="#fff"/></svg>')


if __name__ == '__main__':
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / 'ja').mkdir(parents=True)
    (OUT / 'index.html').write_text(render('en'))
    (OUT / 'ja' / 'index.html').write_text(render('ja'))
    shutil.copytree(ROOT / 'static', OUT, dirs_exist_ok=True)
    (OUT / 'favicon.svg').write_text(favicon())
    (OUT / '.nojekyll').touch()
    (OUT / 'version.txt').write_text(os.environ.get('GITHUB_SHA', 'local-preview') + '\n')
    (OUT / '404.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found — Aethel</title><link rel="stylesheet" href="' + BASE + '/style.css"><main class="wrap" style="padding:6rem 0"><h1>Page not found</h1><p><a class="btn" href="' + BASE + '/">Return to Aethel</a></p></main></html>')
    (OUT / 'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: ' + BASE + '/sitemap.xml\n')
    (OUT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join('<url><loc>' + BASE + q + '</loc></url>' for q in ('/', '/ja/')) + '</urlset>')
    print('Built Aethel English and Japanese pages → public/')
