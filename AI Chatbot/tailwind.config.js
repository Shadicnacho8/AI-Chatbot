/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/templates/**/*.html", "./app/static/js/**/*.js"],
  darkMode: "class",
  theme: {
    container: {
      padding: "1rem",
      center: true,
    },
    extend: {},
  },
  plugins: [],
};
