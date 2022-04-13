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
        "twitter-grey1-10": "rgba(83, 100, 113, .1)",
        "twitter-green1": "rgba(0, 186, 124, 1)",
        "twitter-green1-10": "rgba(83, 100, 113, .1)",
        "twitter-pink1": "rgba(249, 24, 128, 1)",
        "twitter-pink1-10": "rgba(249, 24, 128, .1)"
      }
    },
  },
  plugins: [],
}
