/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        // color palette
        "background" : "#F8F9F7",
        "primary" : {
          "100" : "#d2d4db",
          "200" : "#495270",
          "300" : "#1C274C",
        },

        "dimwhite" : "#BEB9B1",

        whitesmoke: "#f8f9f7",
        darkslateblue: {
          "100": "#1c274c",
          "200": "rgba(28, 39, 76, 0.5)",
        },
        slategray: "#6c6f7e",
        orangered: {
          "100": "#ff5a26",
          "200": "#ff5800",
          "300": "#ff3d00",
        },
        royalblue: "#4b74ff",
        white: "#fff",
      },
      spacing: {},
      fontFamily: {
        montserrat: "Montserrat",
        syne: "Syne",
        inter: "Inter",
      },
    },
    fontSize: {
      sm: "14px",
      mini: "15px",
      smi: "13px",
      base: "16px",
      "11xl": "30px",
      "5xl": "24px",
      lg: "18px",
      xl: "20px",
      "6xl": "25px",
      "16xl": "35px",
      "9xl": "28px",
      "2xl": "21px",
      mid: "17px",
      xs: "12px",
      inherit: "inherit",
    },
    screens: {
      lg: {
        max: "1200px",
      },
      mq1100: {
        raw: "screen and (max-width: 1100px)",
      },
      mq1050: {
        raw: "screen and (max-width: 1050px)",
      },
      mq1000: {
        raw: "screen and (max-width: 1000px)",
      },
      mq850: {
        raw: "screen and (max-width: 850px)",
      },
      mq750: {
        raw: "screen and (max-width: 750px)",
      },
      mq675: {
        raw: "screen and (max-width: 675px)",
      },
      mq650: {
        raw: "screen and (max-width: 650px)",
      },
      mq625: {
        raw: "screen and (max-width: 625px)",
      },
      mq450: {
        raw: "screen and (max-width: 450px)",
      },
      mq436: {
        raw: "screen and (max-width: 436px)",
      },
      mq406: {
        raw: "screen and (max-width: 406px)",
      },
      mq398: {
        raw: "screen and (max-width: 398px)",
      },
      mq374: {
        raw: "screen and (max-width: 374px)",
      },
    },
  },
  corePlugins: {
    preflight: false,
  },
};
