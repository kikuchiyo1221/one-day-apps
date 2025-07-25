#!/usr/bin/env node
// md2html_cli/main.js
// Convert Markdown to HTML.
// Usage:
//   node main.js --input README.md --output README.html
//   cat README.md | node main.js > README.html
const fs = require("fs");
const path = require("path");
const { marked } = require("marked");
const yargs = require("yargs");
const { hideBin } = require("yargs/helpers");

function convertMarkdown(md) {
  return marked.parse(md);
}

async function main() {
  const argv = yargs(hideBin(process.argv))
    .option("input", {
      alias: "i",
      type: "string",
      description: "Input Markdown file (optional; stdin if omitted)",
    })
    .option("output", {
      alias: "o",
      type: "string",
      description: "Output HTML file (default: stdout)",
    })
    .help()
    .argv;

  let markdown = "";
  if (argv.input) {
    markdown = fs.readFileSync(path.resolve(argv.input), "utf8");
  } else {
    markdown = fs.readFileSync(0, "utf8"); // read from stdin
  }

  const html = convertMarkdown(markdown);

  if (argv.output) {
    fs.writeFileSync(path.resolve(argv.output), html, "utf8");
  } else {
    process.stdout.write(html);
  }
}

if (require.main === module) {
  main();
}

module.exports = { convertMarkdown }; 