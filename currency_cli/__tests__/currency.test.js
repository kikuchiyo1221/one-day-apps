const axios = require("axios");
const { convertAmount } = require("../index.js");

jest.mock("axios");

describe("convertAmount", () => {
  it("returns converted numeric value", async () => {
    axios.get.mockResolvedValue({ data: { result: "success", rates: { JPY: 157 } } });
    const result = await convertAmount("USD", "JPY", 100);
    expect(result).toBe(15700);
  });
}); 