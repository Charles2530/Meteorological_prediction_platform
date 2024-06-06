/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
  theme: {
    extend: {
      backgroundImage: {
        "top-background-light": "url('/src/assets/img/top-background.jpg')",
        "top-background": "url('/src/assets/img/top-background-dark.png')",
        "mobile-sunny": "url('/src/assets/img/background_sunny.png')",
        "mobile-rainy": "url('/src/assets/img/background_rainy.png')",
        "mobile-overcast": "url('/src/assets/img/background_overcast.png')",
        "mobile-night": "url('/src/assets/img/background_night.png')",
        "mobile-cloudy": "url('/src/assets/img/background_cloudy.png')",
      },
      margin: {},
      fontSize: {
        base: "16px",
      },
    },
  },
  plugins: [],
};
