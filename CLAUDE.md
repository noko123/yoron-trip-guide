# yoron-trip-guide — 与論島ガイドブック (2026-09-05〜07)

単一 HTML の旅行ガイド。**`yoron-guide.template.html` を編集して push すれば、GitHub Actions が `docs/index.html` を組み直して GitHub Pages に公開する** (1〜2 分)。旅先からスマホの Claude Code で直すための構成。

## 触るファイル

| ファイル | 役割 |
|---|---|
| `yoron-guide.template.html` | **本文 (これだけ編集する)**。CSS・SVG 図・章立てを含む単一テンプレ |
| `build.py` | テンプレ → `docs/index.html`。画像の base64 埋め込みと写真の帰属表記もここで生成 |
| `use/*.jpg` | 埋め込む写真 (Wikimedia Commons の CC 画像、幅 1000px に縮小済み) |
| `manifest.json` | 写真 slug → ファイル名・作者・ライセンス・Commons URL |
| `docs/index.html` | 生成物 (Actions が作る。手で編集しない) |

## テンプレ内のマーカー

- `{{IMG:slug}}` — `use/<slug>.jpg` を base64 で埋め込む。`{{CREDIT:slug}}` は帰属表記 (図の caption 末尾に置く)
- `{{PV:key|公開テキスト}}` — 個人情報の分岐。公開版 (Pages) は常に「公開テキスト」。`private.json` (コミットしない・PC にだけある) に key があれば自分用版でそちらに置換される。**公開版に予約番号・航空券番号・金額・宿泊者名を書かない**。書きたい時はこのマーカーで包む
- `{{CREDITS_LIST}}` — 末尾の写真出典一覧 (自動)

## 編集の作法

- 事実 (時刻・料金・営業時間) を変えたら、末尾「出典」節の該当番号を確認する。新しい出典は `<li id="s47">` のように番号を足し、本文は `<sup class="cite"><a href="#s47">47</a></sup>` で参照
- 写真を足すなら Commons の CC ライセンス品のみ。`manifest.json` に slug を追加し、`use/<slug>.jpg` を置く (幅 1000px 目安・1 枚 200KB 以下)。食べログ・Google マップ・個人ブログの写真は著作権上コピーしない (リンクで示す)
- 色は CSS 変数 (`var(--accent)` 等) を使う。生の hex を本文に書かない
- push 前に `python build.py` が通ることを確認する (未置換マーカー・画像欠落・公開版への個人情報漏れで失敗する)

## 新しいページ・別のサイトを足す時

- **置き場は `docs/<slug>/index.html`** (slug は英小文字とハイフン)。push すると `https://noko123.github.io/yoron-trip-guide/<slug>/` で公開される。`build.py` は `docs/index.html` だけを書き換え、他のファイルには触らない
- 単一 HTML で完結させる (画像は base64 か `docs/<slug>/` 内に置く)。1 ファイル 25MB 以下。外部の CDN は原則使わないが、**地図の Leaflet (cdnjs) と OpenStreetMap タイルだけは例外**として使っている (§03 の対話地図。圏外では静止画にフォールバック)
- 地図を直す時: 座標は `spots.json`、静止画は `map_draw.py` (OSM タイルの貼り合わせ `basemap_z15.png` は `tiles.py` が作る)、Leaflet のマーカーはテンプレ内の `var S=[...]` (spots.json から `map_block.py` が生成した)。3 つを同時に更新する
- **公開リポジトリなので、予約番号・住所・電話番号・人の顔写真・金額など個人情報は書かない**。必要なら `{{PV:...}}` の仕組みは使えないので、そもそも載せない
- ガイド本体 (`docs/index.html`) からリンクしたい時は、テンプレの該当章に `<a href="./<slug>/">` を足す
- 写真は自分で撮ったものか CC ライセンスのものだけ。他サイトの画像をコピーしない

## 公開先

- 公開版: GitHub Pages (このリポジトリの `docs/`)
- 自分用版: PC でだけ `python build.py` → `dist/` に出る (`private.json` がある時)。dev-reports への掲載は `report-publisher/publish.ps1`
