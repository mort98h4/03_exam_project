module.exports = {
  mode: "JIT",
  purge: ["../views/*.html"],
  content: [],
  theme: {
    extend: {
      colors: {
        "twitter-blue1": "rgba(29, 155, 240, 1)",
        "twitter-blue1-10": "rgba(29, 155, 240, .1)",
        "twiiter-blue2": "rgba(26, 140, 216, 1)"
      }
    },
  },
  plugins: [],
}
