# サイトの構築・公開・独自ドメイン

## 構成

- `build.py`: 英語・日本語のコンテンツとHTML生成。
- `static/style.css`: PCと狭幅の表示。外部フォントや画像の取得は不要。
- `static/favicon.svg`: ブランドの文字アイコン。
- `public/`: 公開対象のみ。生成物はGit管理しない。
- `.github/workflows/pages.yml`: mainから生成し、Pagesへ配信。
- `version.txt`: 配信されたソースcommit SHA。

英語のURLは `/`、日本語は `/ja/`。リンクはプロジェクトURLの
サブディレクトリでも独自ドメインでも動く相対パスを使う。
JavaScript、バックエンド、フォーム、問い合わせメール設定はない。
技術資料はzkFMIの公開ドキュメント、実装はGitHubへ接続する。

## 通常の更新

```sh
python3 build.py
python3 -m http.server 8000 --directory public
```

両言語のPC・狭幅画面で、見出し、本文、ナビゲーション、主要リンクを
実操作で確認する。変更をcommitしてmainへpushすると公開される。
GitHub Actionsの終了だけでなく、配信URLを開き、画面と
`version.txt`が対象commitに一致することを確認する。

## 独自ドメインへの接続

対象: `aethel.fi` / 管理サービス: Marcaria /
GitHub repository: `zkFMI/aethel-site`。

2026-09-13にMarcariaのアカウント認証を完了。aethel.fiはPagesの独自ドメインへ設定し、apex Aの4件とwww CNAMEを保存した。aemeth.fiは登録処理中のためDNS設定画面がなく、Pages URLで公開中。DNS伝播とHTTPSの確認結果は実行記録で別に扱う。

1. Marcariaの確認メールでアカウント認証を完了する。
2. 対象ドメインの登録完了と既存DNSレコードを確認する。
3. GitHub Pagesに対象ドメインを設定してからDNSを変更する。
4. 既存メール用MX・TXTなどを保持し、対象サイトのapex Aを
   次のGitHub Pagesの値に設定する。

| 名前 | 種別 | 値 |
| --- | --- | --- |
| @ | A | 185.199.108.153 |
| @ | A | 185.199.109.153 |
| @ | A | 185.199.110.153 |
| @ | A | 185.199.111.153 |
| www | CNAME | zkfmi.github.io |

5. GitHubリポジトリ変数 `SITE_URL` を `https://aethel.fi` にし再公開する。
6. DNS応答、Pagesのドメイン確認、HTTPS証明書を確認する。
7. 独自ドメインの両言語を実ブラウザーで開き、配信版・表示・リンクを確認する。
8. サイト間のリンクも独自ドメインへ更新する。

GitHub Actionsで公開するためCNAMEファイルは不要。
Pages設定をDNSより先に行う。DNS変更と証明書発行には時間がかかる場合がある。
独自ドメイン設定後は `https://zkfmi.github.io/aethel-site/` も独自ドメインへリダイレクトする。証明書の発行前は、HTTPSの公開確認が完了したとは扱わない。

設定値の一次資料:
[GitHub公式: Custom domain](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site)

## 証跡の扱い

サイトの表示・公開確認は、金融基盤の新たな統合試験ではない。
研究結果の記述は、リンク先の実行条件・版・制限と一緒に評価する。
会話の原文、Marcariaのアカウント情報、ログイン情報は公開物へ含めない。

## 2026-09-13の実操作確認

1. 公開英語ページを390px幅で開き、Explore the lifecycleをクリック。#lifecycleへ移動し債権の手順が表示された。
2. 日本語の企業向けPoCガイドをクリックし、GitHub上のガイド本文と章見出しを確認。
3. 独自ドメインの日本語ページを390px幅で開き、修正した見出しが2行に収まり、横幅390pxに対しscrollWidthも390pxであることを確認。実証・評価をクリックし#evaluateへ移動。PCでも両言語と下部導線を視認。

確認時の配信ソース: `8b370067041478c614246b9053240ee39b435284`。

DNSはPagesへ接続済み。HTTPの独自ドメインで表示確認済みだが、HTTPS証明書は未発行。HTTPS接続とサイト間リンクの受け入れは未完了。
