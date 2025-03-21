module.exports = {
  // ... other config
  theme: {
    extend: {
      keyframes: {
        "slide-in": {
          "0%": { transform: "translateX(100%)" },
          "100%": { transform: "translateX(0)" },
        },
      },
      animation: {
        "slide-in": "slide-in 0.3s ease-out",
      },
      colors: {
        primary: "var(--color-primary)",
        element: "var(--color-element)",
        primaryText: "var(--color-primaryText)",
        secondaryText: "var(--color-secondaryText)",
        primaryBackground: "var(--color-primaryBackground)",
        secondaryBackground: "var(--color-secondaryBackground)",
      },
    },
  },
};
