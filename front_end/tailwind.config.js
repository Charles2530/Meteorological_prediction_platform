/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
  theme: {
    extend: {
      backgroundImage: {
        "top-background-light": "url('/src/assets/img/top-background.jpg')",
        "top-background": "url('/src/assets/img/top-background-dark.png')",
      },
      margin: {},
    },
  },
  plugins: [],
};
