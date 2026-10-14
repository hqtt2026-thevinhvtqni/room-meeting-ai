// @lovable.dev/vite-tanstack-config already includes TanStack devtools, tanstackStart, viteReact,
// tailwindcss, tsConfigPaths, nitro (cloudflare target), VITE_* env, @ alias — do NOT add manually.
import { defineConfig } from "@lovable.dev/vite-tanstack-config";

export default defineConfig({
  tanstackStart: {
    // Redirect TanStack Start's bundled server entry to src/server.ts (SSR error wrapper).
    server: { entry: "server" },
  },
});
