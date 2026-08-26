# デスクトップ版Codexへ渡す開始プロンプト

以下をそのままデスクトップ版Codexに渡してください。

---

`satoshi-bon/bon` を開き、ブランチ `feature/living-field-studio-v01` をcheckoutしてください。

最初に、次のファイルを順番に読んでください。

1. `threejs/sky/studio/AGENTS.md`
2. `threejs/sky/studio/HANDOFF.md`
3. `threejs/sky/studio/studio-config.example.json`
4. `threejs/sky/v12/index.html`
5. `threejs/sky/index.html`

その上で、`Living Field Studio v01` を `threejs/sky/studio/v01/` に実装してください。

重要事項：

- v03〜v12は一切変更しない。
- `threejs/sky/index.html` の公開ルータも、ユーザーの承認前には変更しない。
- v12の見た目を初期presetとして維持する。
- seeded randomness、主要変数パネル、A/B、Undo/Redo、JSON import/exportを実装する。
- 高負荷パラメータはApply/Rebuild方式にする。
- デスクトップとモバイルでブラウザ動作確認する。
- ローカルHTTPサーバーを起動し、実際にブラウザで各機能を確認する。
- 作業は論理的な単位でcommitするが、masterへmergeしない。

まずコードを監査して実装計画を短く提示し、その後は実装・テストまで継続してください。完了時には、変更ファイル、実行したテスト、既知の制約、確認用ローカルURL、commit SHAを報告してください。

---
