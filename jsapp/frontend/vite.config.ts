import { defineConfig } from "vite";

export default defineConfig(({ mode }) => ({
  // ...
  build: {
    outDir: "../dist",
  },
  server: {
    proxy: {
      "/api": {
        target: "http://localhost:3003",
        changeOrigin: true,
        secure: false,
      },
    },
  },
}));
