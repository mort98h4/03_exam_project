module.exports = {
  mode: "JIT",
  purge: ["../views/*.html"],
  content: [],
  theme: {
    extend: {
      colors: {
        "twitter-blue1": "rgba(29, 155, 240, 1)",
        "twitter-blue1-10": "rgba(29, 155, 240, .1)",
        "twitter-blue2": "rgba(26, 140, 216, 1)",
        "twitter-grey1": "rgba(83, 100, 113, 1)",
        "twitter-grey1-50": "rgba(83, 100, 113, .5)",
        "twitter-grey1-10": "rgba(83, 100, 113, .1)"
      }
    },
  },
  plugins: [],
}
