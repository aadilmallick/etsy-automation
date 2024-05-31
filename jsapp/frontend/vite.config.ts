import { defineConfig, loadEnv } from "vite";

export default defineConfig(({ mode, command }) => {
  const env = loadEnv("production", "../");
  console.log(env);
  console.log(mode);
  const target =
    mode === "development" ? env.VITE_API_URL_DEV : env.VITE_API_URL_PRODUCTION;
  return {
    // ...
    build: {
      outDir: "../dist",
    },
    server: {
      proxy: {
        "/api": {
          target: target,
          changeOrigin: true,
          secure: false,
        },
      },
    },
  };
});
