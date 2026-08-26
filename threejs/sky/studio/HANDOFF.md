# Living Field Studio v01 — 引継ぎ仕様

## 0. 引継ぎ先

- Repository: `satoshi-bon/bon`
- Working branch: `feature/living-field-studio-v01`
- Current published baseline: `threejs/sky/v12/index.html`
- Current public router: `threejs/sky/index.html`
- Studio target path: `threejs/sky/studio/v01/`

このブランチは、デスクトップ版Codexへ作業を引き継ぐために用意したものです。公開済みのv03〜v12は変更しません。

---

## 1. 背景

Living Fieldは、研究室サイトのトップビジュアル候補として検討しているThree.js表現です。現在のv12では、以下が同じ共有風場に反応します。

- 地平線まで広がる草原
- 風と連動して密度・明暗が変化する空
- 白〜生成りの通常飛翔体
- 通常飛翔体とは別系統の、小型で鮮やかな虹色飛翔体群

これまで、コード内の定数を変更し、新しい連番バージョンを作って比較してきました。しかし、主要変数を本人が直接操作してデザインを比較できる方が効率的です。そのため、公開デザインとは別に `Living Field Studio v01` を作ります。

ユーザーは基本的にコードを手書きしません。ChatGPT / Codexに生成・修正させ、VS Codeは確認・差分閲覧・部分調整・デバッグに使います。したがって、操作UIは専門的なコード知識を前提にせず、意味が分かる日本語ラベルと適切な安全範囲を持たせてください。

---

## 2. v01の目的

主要なデザイン変数をブラウザ上で操作し、同じランダム初期条件の下で比較し、設定を保存・再現できるツールを作ることです。

### 最重要成果

1. v12に近い初期表示
2. 主要パラメータのリアルタイム操作
3. seed固定による再現性
4. A/B比較
5. Undo / Redo
6. JSON保存・読込
7. デスクトップとモバイルの操作性
8. GitHub Pagesで公開可能な静的構成

---

## 3. デザイン上の固定方針

以下はパラメータ化しても壊さないでください。

### 草原

- 水平線まで続く広がりを重視する。
- 草の線が一本ずつ容易に認識できる、絵本的・稚拙な表現にしない。
- 風は手前から奥へ立体的に流れる。
- 大きな風の波と、草ごとの微細な揺らぎを併存させる。
- v05以降で維持してきた草原の質感を基準にする。

### 空

- 雲の輪郭を描くのではなく、空気の密度と光が動くように見せる。
- 草原のガストや渦と連動するが、草より遅く大きなスケールで反応する。
- 空単独の派手な背景アニメーションにしない。

### 通常飛翔体

- 種、紙片、花びらのいずれかに断定しない曖昧な形。
- 白、生成り、灰白を中心にする。
- 虹色群とは別系統で存在し続ける。

### 虹色飛翔体群

- パーティクルではなく、通常飛翔体と同じ系統の小型飛翔体形状を使う。
- 通常飛翔体とは別系統。
- 固定色マテリアルによる赤・橙・黄・緑・シアン・青・紫を使う。
- 群としてまとまりながら、各個体に小さな位相差・回転差・サイズ差を持たせる。
- 出現位置は完全乱数で偏らせず、層化ランダム等で空間を均等に使う。
- 最大個体サイズはv12の `.44` を初期上限とする。

### 風

- 風を分かりやすい線として直接描かない。
- 草、空、飛翔体の運動から風を感じさせる。
- `dirA / dirB / dirC`、gust packets、whirls、interferenceを中核としてよい。
- 全要素を同一運動にせず、共有風場への感度を要素ごとに変える。

---

## 4. 推奨アーキテクチャ

初期版は静的サイトとして構成してください。例：

```text
threejs/sky/studio/v01/
├─ index.html
├─ styles.css
├─ src/
│  ├─ main.js
│  ├─ engine.js
│  ├─ config.js
│  ├─ seeded-random.js
│  ├─ controls.js
│  ├─ history.js
│  └─ presets.js
└─ README.md
```

この構造は提案であり、同等以上に分かりやすい構造なら変更可能です。

### 必須原則

- 描画エンジンとUIを分離する。
- 設定値は単一のcanonical config objectで管理する。
- UI、プリセット、JSON import/export、A/B、URL状態はすべて同じconfigを使う。
- v12ファイル自体は編集しない。必要な処理をStudio側へ複製・整理する。
- 将来、Studioの採用設定からLiving Field v13を生成しやすい構成にする。

---

## 5. UI案

### デスクトップ

- 画面の大部分：リアルタイムプレビュー
- 右側：幅320〜380px程度の操作パネル
- パネルは折りたたみ可能
- 上部にPreset、Seed、A/B、Undo/Redo、Export/Import
- 下部にFPSまたはQuality表示（任意だが有用）

### モバイル

- プレビューを最大限残す。
- 操作パネルは下部シート、ドロワー、または全画面オーバーレイ。
- スライダー操作中も主要部分が見えること。
- スクロール可能なパネルにする。

### 操作部品

- スライダー＋数値入力を基本とする。
- Resetボタンをカテゴリごとに付ける。
- 高負荷パラメータには `Apply / Rebuild` を付ける。
- 危険な範囲へ行かないようmin/maxを制約する。
- ラベルは日本語中心。必要に応じて短い英語識別子を併記する。
- ツールチップまたは短い説明で、見た目への影響を説明する。

---

## 6. v01で操作可能にする主要変数

すべてを最初から露出しすぎないでください。Primary controlsは30〜40個程度に抑え、Advancedを折りたたみます。

### Scene

- 地平線の高さ
- カメラ高さ
- FOV
- 遠景の霞
- 光の広がり

### Wind

- 基本風向
- 全体速度
- 大きな風の波の強度
- 複数方向の混合量
- gust count
- gust strength
- gust radius
- gust speed / frequency
- whirl count
- whirl strength
- interference strength
- 草・空・飛翔体への連動率

### Meadow

- blade count（rebuild）
- 平均草丈
- 草丈のばらつき
- 草幅
- 風への感度
- 遠景フェード
- 近景・中景・遠景の色

### Sky

- 大気密度
- 大気コントラスト
- 流動速度
- gust response
- whirl response
- horizon haze

### Ordinary Flyers

- count（rebuild）
- min / max size
- opacity
- inertia
- lift sensitivity
- flutter intensity

### Rainbow Flocks

- max group count（rebuild）
- initial group count
- flyers per group（rebuild）
- spawn interval min / max
- lifetime min / max
- spread min / max
- min / max flyer size
- size distribution bias
- color intensity
- spawn x / y / z bounds
- spawn grid columns / rows
- wind following / inertia

### Quality

- pixel ratio cap
- max FPS
- desktop/mobile density preset
- reduced-motion preview
- pause when panel or tab is inactive

---

## 7. 再現性

v01ではseed固定を必須にします。

### 要件

- 同じseedと同じconfigで、再読み込み後も同じ初期配置・風パケット・渦・飛翔体群を再現する。
- デザインに影響する乱数は、seeded PRNGを経由する。
- runtimeの微小ノイズも、比較に影響するものは可能な限りseed由来にする。
- `New Seed`、`Copy Seed`、数値入力を用意する。

---

## 8. A/B比較

v01の必須範囲は、左右分割ではなく瞬時切替でも構いません。

### 必須

- `Save A`
- `Save B`
- `Show A / Show B`
- A/Bそれぞれにconfigとseedを保存
- A/Bが未保存の場合は明示

### Stretch goal

- 左右分割またはスライダー比較
- カメラ時間を同期した二画面比較

---

## 9. 履歴・保存

### Undo / Redo

- 代表的な操作を戻せる。
- スライダーのmousemoveごとに無限に履歴を作らず、操作終了時に1履歴とする。
- rebuild操作も履歴として扱う。

### JSON

- Download JSON
- Import JSON
- Copy JSON to clipboard
- 読込時のversion、型、範囲を検証
- 未知キーは安全に無視または警告

### Local storage

- 最後の設定を自動保存してよい。
- `Reset to v12 baseline` を必ず用意する。

### URL共有

- v01では必須ではないが、configを圧縮してURLへ入れる構造を阻害しないこと。

---

## 10. 初期プリセット

最低限、以下を用意してください。

1. `v12 Baseline`
2. `Calm`
3. `Strong Wind`
4. `Wide Sky`
5. `Sparse Flyers`
6. `Rainbow Study`

`v12 Baseline` の値は `studio-config.example.json` を出発点にしてください。

---

## 11. v01で行わないこと

- WordPress本番サイトへの組込み
- GitHub認証をブラウザに持たせた直接publish
- 公開中のv03〜v12の共通化・書換え
- 大規模なフレームワーク導入
- 複数ユーザー共同編集
- サーバー保存
- 生成AIによる自動評価
- 完全なデザイン探索・最適化

将来の `Publish as v13` は別タスクです。

---

## 12. Definition of Done

以下を満たしたらv01完成候補です。

- `threejs/sky/studio/v01/index.html` がローカルHTTPサーバーで起動する。
- 初期presetがv12の印象を明確に維持する。
- Primary controlsが各カテゴリに整理されている。
- 主要スライダーが意図どおりリアルタイム反映される。
- rebuild対象は明示され、Apply後に正しく再構築される。
- 同じseed＋configで初期状態が再現される。
- A/B保存・切替が動く。
- Undo / Redoが動く。
- JSON export/importが往復可能。
- DesktopとmobileでUIが使える。
- `prefers-reduced-motion` に配慮する。
- コンソールエラーがない。
- v03〜v12へのdiffがない。
- READMEに起動方法、操作方法、既知の制約が書かれている。
- Codexが実行確認結果と変更ファイルを報告する。

---

## 13. 推奨作業順

1. v12を監査し、設定化可能な定数を分類する。
2. engineとconfigを分離する。
3. seeded PRNGを入れ、baselineの再現性を確立する。
4. 最小UIでScene / Wind / Meadowを接続する。
5. Sky / Flyers / Rainbowを接続する。
6. rebuildパラメータを整理する。
7. Preset、A/B、Undo/Redoを追加する。
8. JSON import/exportを追加する。
9. mobile UIとquality controlsを調整する。
10. ブラウザで反復検証し、READMEを完成する。

---

## 14. Codex終了時の報告形式

- 実装した機能
- 変更したファイル
- 実行したテスト
- Desktop / mobile確認結果
- 未実装または既知の制約
- 次にユーザーが見るべきローカルURL
- commit SHA
- masterへmergeしていないことの確認
