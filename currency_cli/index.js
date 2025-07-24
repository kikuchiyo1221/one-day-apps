#!/usr/bin/env node
// ↑ ① シバン行：Unix 系環境で「node index.js」の代わりに
//    ./index.js で直接実行できるようにする。
//    Windows では無視されるので問題なし。

const axios = require("axios");          // ② HTTP クライアント
// yargs は CLI 実行時のみ必要。テストでは不要なので main 内で require する。

// ④ 純粋関数：API を呼び換算結果を数値で返す
async function convertAmount(from, to, amount) {
  const url = `https://open.er-api.com/v6/latest/${from}`;
  const { data } = await axios.get(url);

  if (data.result !== "success") {
    throw new Error("API error");
  }
  const rate = data.rates[to];
  if (!rate) throw new Error(`Unknown currency: ${to}`);

  return amount * rate;
}

// テスト用に関数をエクスポート
module.exports = { convertAmount };

// ⑤ CLI のエントリーポイント
async function main() {
  const yargs = require("yargs");
  const { hideBin } = require("yargs/helpers");
  // hideBin は process.argv から node 実行分を取り除くヘルパ
  const argv = yargs(hideBin(process.argv))
    .option("from", {
      alias: "f",
      type: "string",
      demandOption: true,
      describe: "変換元通貨 (例: USD)"
    })
    .option("to", {
      alias: "t",
      type: "string",
      demandOption: true,
      describe: "変換先通貨 (例: JPY)"
    })
    .option("amount", {
      alias: "a",
      type: "number",
      demandOption: true,
      describe: "金額"
    })
    .help()            // --help を自動生成
    .version(false)    // --version を無効化（任意）
    .argv;             // ここで実際にパース

  try {
    const converted = await convertAmount(argv.from, argv.to, argv.amount);
    console.log(`${argv.amount} ${argv.from} = ${converted} ${argv.to}`);
  } catch (err) {
    console.error("Error:", err.message);
    process.exitCode = 1;
  }
}

// ⑥ ファイルが “直接実行” されたか判定して main() を実行
if (require.main === module) {
  main();
}
