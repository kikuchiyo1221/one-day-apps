const { convertMarkdown } = require("../md2html_cli/main.js");

test("convertMarkdown converts heading", () => {
  const md = "# Hello\n\nThis is *markdown*.";
  const html = convertMarkdown(md).trim();
  expect(html.startsWith("<h1 id=\"hello\">Hello</h1>" )).toBe(true);
  expect(html.includes("<em>markdown</em>")).toBe(true);
}); 