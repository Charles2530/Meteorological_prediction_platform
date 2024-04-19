// vite.config.ts
import { defineConfig } from "file:///D:/Programing/SoftwareEngineering/Meteorological_prediction_platform/front_end/node_modules/vite/dist/node/index.js";
import vue from "file:///D:/Programing/SoftwareEngineering/Meteorological_prediction_platform/front_end/node_modules/@vitejs/plugin-vue/dist/index.mjs";
import Inspect from "file:///D:/Programing/SoftwareEngineering/Meteorological_prediction_platform/front_end/node_modules/vite-plugin-inspect/dist/index.mjs";
import Icons from "file:///D:/Programing/SoftwareEngineering/Meteorological_prediction_platform/front_end/node_modules/unplugin-icons/dist/vite.js";
import AutoImport from "file:///D:/Programing/SoftwareEngineering/Meteorological_prediction_platform/front_end/node_modules/unplugin-auto-import/dist/vite.js";
import Components from "file:///D:/Programing/SoftwareEngineering/Meteorological_prediction_platform/front_end/node_modules/unplugin-vue-components/dist/vite.js";
import IconsResolver from "file:///D:/Programing/SoftwareEngineering/Meteorological_prediction_platform/front_end/node_modules/unplugin-icons/dist/resolver.js";
import { ElementPlusResolver } from "file:///D:/Programing/SoftwareEngineering/Meteorological_prediction_platform/front_end/node_modules/unplugin-vue-components/dist/resolvers.js";
import { resolve } from "path";
var __vite_injected_original_dirname = "D:\\Programing\\SoftwareEngineering\\Meteorological_prediction_platform\\front_end";
var vite_config_default = defineConfig({
  plugins: [
    vue(),
    AutoImport({
      // Auto import functions from Vue, e.g. ref, reactive, toRef...
      // 自动导入 Vue 相关函数，如：ref, reactive, toRef 等
      imports: ["vue", "vue-router"],
      // Auto import functions from Element Plus, e.g. ElMessage, ElMessageBox... (with style)
      // 自动导入 Element Plus 相关函数，如：ElMessage, ElMessageBox... (带样式)
      resolvers: [
        ElementPlusResolver(),
        // Auto import icon components
        // 自动导入图标组件
        IconsResolver({
          prefix: "Icon"
        })
      ],
      dts: resolve(__vite_injected_original_dirname, "src", "auto-imports.d.ts"),
      // 解决eslint报错问题
      eslintrc: {
        // 这里先设置成true然后npm run dev 运行之后会生成 .eslintrc-auto-import.json 文件之后，在改为false
        enabled: false,
        filepath: "./.eslintrc-auto-import.json",
        // 生成的文件路径
        globalsPropValue: true
      }
    }),
    Components({
      resolvers: [
        // Auto register icon components
        // 自动注册图标组件
        IconsResolver({
          enabledCollections: ["ep"]
        }),
        // Auto register Element Plus components
        // 自动导入 Element Plus 组件
        ElementPlusResolver()
      ],
      // 允许子目录作为组件的命名空间前缀。
      directoryAsNamespace: true,
      dts: resolve(__vite_injected_original_dirname, "src", "components.d.ts")
    }),
    Icons({
      autoInstall: true
    }),
    Inspect()
  ],
  resolve: {
    // Alias configuration: use @ to represent the src directory
    alias: {
      "@": resolve(__vite_injected_original_dirname, "src"),
      "@c": resolve(__vite_injected_original_dirname, "src/components"),
      "@css": resolve(__vite_injected_original_dirname, "src/assets/css"),
      "@img": resolve(__vite_injected_original_dirname, "src/assets/img")
    }
  }
  //   server: {
  //     // Enable the proxy
  //     proxy: {
  //       "/api": {
  //         target: "http://localhost:3000",
  //         changeOrigin: true,
  //         rewrite: (path) => path.replace(/^\/api/, ""),
  //       },
  //     },
  //     // Allow the CORS
  //     headers: {
  //       "Access-Control-Allow-Origin": "*",
  //       "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, PATCH, OPTIONS",
  //       "Access-Control-Allow-Headers":
  //         "X-Requested-With, content-type, Authorization",
  //     },
  //   },
});
export {
  vite_config_default as default
};
//# sourceMappingURL=data:application/json;base64,ewogICJ2ZXJzaW9uIjogMywKICAic291cmNlcyI6IFsidml0ZS5jb25maWcudHMiXSwKICAic291cmNlc0NvbnRlbnQiOiBbImNvbnN0IF9fdml0ZV9pbmplY3RlZF9vcmlnaW5hbF9kaXJuYW1lID0gXCJEOlxcXFxQcm9ncmFtaW5nXFxcXFNvZnR3YXJlRW5naW5lZXJpbmdcXFxcTWV0ZW9yb2xvZ2ljYWxfcHJlZGljdGlvbl9wbGF0Zm9ybVxcXFxmcm9udF9lbmRcIjtjb25zdCBfX3ZpdGVfaW5qZWN0ZWRfb3JpZ2luYWxfZmlsZW5hbWUgPSBcIkQ6XFxcXFByb2dyYW1pbmdcXFxcU29mdHdhcmVFbmdpbmVlcmluZ1xcXFxNZXRlb3JvbG9naWNhbF9wcmVkaWN0aW9uX3BsYXRmb3JtXFxcXGZyb250X2VuZFxcXFx2aXRlLmNvbmZpZy50c1wiO2NvbnN0IF9fdml0ZV9pbmplY3RlZF9vcmlnaW5hbF9pbXBvcnRfbWV0YV91cmwgPSBcImZpbGU6Ly8vRDovUHJvZ3JhbWluZy9Tb2Z0d2FyZUVuZ2luZWVyaW5nL01ldGVvcm9sb2dpY2FsX3ByZWRpY3Rpb25fcGxhdGZvcm0vZnJvbnRfZW5kL3ZpdGUuY29uZmlnLnRzXCI7aW1wb3J0IHsgZGVmaW5lQ29uZmlnIH0gZnJvbSBcInZpdGVcIjtcclxuaW1wb3J0IHZ1ZSBmcm9tIFwiQHZpdGVqcy9wbHVnaW4tdnVlXCI7XHJcbmltcG9ydCBJbnNwZWN0IGZyb20gXCJ2aXRlLXBsdWdpbi1pbnNwZWN0XCI7XHJcbmltcG9ydCBJY29ucyBmcm9tIFwidW5wbHVnaW4taWNvbnMvdml0ZVwiO1xyXG5pbXBvcnQgQXV0b0ltcG9ydCBmcm9tIFwidW5wbHVnaW4tYXV0by1pbXBvcnQvdml0ZVwiO1xyXG5pbXBvcnQgQ29tcG9uZW50cyBmcm9tIFwidW5wbHVnaW4tdnVlLWNvbXBvbmVudHMvdml0ZVwiO1xyXG5pbXBvcnQgSWNvbnNSZXNvbHZlciBmcm9tIFwidW5wbHVnaW4taWNvbnMvcmVzb2x2ZXJcIjtcclxuaW1wb3J0IHsgRWxlbWVudFBsdXNSZXNvbHZlciB9IGZyb20gXCJ1bnBsdWdpbi12dWUtY29tcG9uZW50cy9yZXNvbHZlcnNcIjtcclxuaW1wb3J0IHsgcmVzb2x2ZSB9IGZyb20gXCJwYXRoXCI7XHJcblxyXG4vLyBodHRwczovL3ZpdGVqcy5kZXYvY29uZmlnL1xyXG5leHBvcnQgZGVmYXVsdCBkZWZpbmVDb25maWcoe1xyXG4gIHBsdWdpbnM6IFtcclxuICAgIHZ1ZSgpLFxyXG4gICAgQXV0b0ltcG9ydCh7XHJcbiAgICAgIC8vIEF1dG8gaW1wb3J0IGZ1bmN0aW9ucyBmcm9tIFZ1ZSwgZS5nLiByZWYsIHJlYWN0aXZlLCB0b1JlZi4uLlxyXG4gICAgICAvLyBcdTgxRUFcdTUyQThcdTVCRkNcdTUxNjUgVnVlIFx1NzZGOFx1NTE3M1x1NTFGRFx1NjU3MFx1RkYwQ1x1NTk4Mlx1RkYxQXJlZiwgcmVhY3RpdmUsIHRvUmVmIFx1N0I0OVxyXG4gICAgICBpbXBvcnRzOiBbXCJ2dWVcIiwgXCJ2dWUtcm91dGVyXCJdLFxyXG4gICAgICAvLyBBdXRvIGltcG9ydCBmdW5jdGlvbnMgZnJvbSBFbGVtZW50IFBsdXMsIGUuZy4gRWxNZXNzYWdlLCBFbE1lc3NhZ2VCb3guLi4gKHdpdGggc3R5bGUpXHJcbiAgICAgIC8vIFx1ODFFQVx1NTJBOFx1NUJGQ1x1NTE2NSBFbGVtZW50IFBsdXMgXHU3NkY4XHU1MTczXHU1MUZEXHU2NTcwXHVGRjBDXHU1OTgyXHVGRjFBRWxNZXNzYWdlLCBFbE1lc3NhZ2VCb3guLi4gKFx1NUUyNlx1NjgzN1x1NUYwRilcclxuICAgICAgcmVzb2x2ZXJzOiBbXHJcbiAgICAgICAgRWxlbWVudFBsdXNSZXNvbHZlcigpLFxyXG4gICAgICAgIC8vIEF1dG8gaW1wb3J0IGljb24gY29tcG9uZW50c1xyXG4gICAgICAgIC8vIFx1ODFFQVx1NTJBOFx1NUJGQ1x1NTE2NVx1NTZGRVx1NjgwN1x1N0VDNFx1NEVGNlxyXG4gICAgICAgIEljb25zUmVzb2x2ZXIoe1xyXG4gICAgICAgICAgcHJlZml4OiBcIkljb25cIixcclxuICAgICAgICB9KSxcclxuICAgICAgXSxcclxuICAgICAgZHRzOiByZXNvbHZlKF9fZGlybmFtZSwgXCJzcmNcIiwgXCJhdXRvLWltcG9ydHMuZC50c1wiKSxcclxuICAgICAgLy8gXHU4OUUzXHU1MUIzZXNsaW50XHU2MkE1XHU5NTE5XHU5NUVFXHU5ODk4XHJcbiAgICAgIGVzbGludHJjOiB7XHJcbiAgICAgICAgLy8gXHU4RkQ5XHU5MUNDXHU1MTQ4XHU4QkJFXHU3RjZFXHU2MjEwdHJ1ZVx1NzEzNlx1NTQwRW5wbSBydW4gZGV2IFx1OEZEMFx1ODg0Q1x1NEU0Qlx1NTQwRVx1NEYxQVx1NzUxRlx1NjIxMCAuZXNsaW50cmMtYXV0by1pbXBvcnQuanNvbiBcdTY1ODdcdTRFRjZcdTRFNEJcdTU0MEVcdUZGMENcdTU3MjhcdTY1MzlcdTRFM0FmYWxzZVxyXG4gICAgICAgIGVuYWJsZWQ6IGZhbHNlLFxyXG4gICAgICAgIGZpbGVwYXRoOiBcIi4vLmVzbGludHJjLWF1dG8taW1wb3J0Lmpzb25cIiwgLy8gXHU3NTFGXHU2MjEwXHU3Njg0XHU2NTg3XHU0RUY2XHU4REVGXHU1Rjg0XHJcbiAgICAgICAgZ2xvYmFsc1Byb3BWYWx1ZTogdHJ1ZSxcclxuICAgICAgfSxcclxuICAgIH0pLFxyXG4gICAgQ29tcG9uZW50cyh7XHJcbiAgICAgIHJlc29sdmVyczogW1xyXG4gICAgICAgIC8vIEF1dG8gcmVnaXN0ZXIgaWNvbiBjb21wb25lbnRzXHJcbiAgICAgICAgLy8gXHU4MUVBXHU1MkE4XHU2Q0U4XHU1MThDXHU1NkZFXHU2ODA3XHU3RUM0XHU0RUY2XHJcbiAgICAgICAgSWNvbnNSZXNvbHZlcih7XHJcbiAgICAgICAgICBlbmFibGVkQ29sbGVjdGlvbnM6IFtcImVwXCJdLFxyXG4gICAgICAgIH0pLFxyXG4gICAgICAgIC8vIEF1dG8gcmVnaXN0ZXIgRWxlbWVudCBQbHVzIGNvbXBvbmVudHNcclxuICAgICAgICAvLyBcdTgxRUFcdTUyQThcdTVCRkNcdTUxNjUgRWxlbWVudCBQbHVzIFx1N0VDNFx1NEVGNlxyXG4gICAgICAgIEVsZW1lbnRQbHVzUmVzb2x2ZXIoKSxcclxuICAgICAgXSxcclxuICAgICAgLy8gXHU1MTQxXHU4QkI4XHU1QjUwXHU3NkVFXHU1RjU1XHU0RjVDXHU0RTNBXHU3RUM0XHU0RUY2XHU3Njg0XHU1NDdEXHU1NDBEXHU3QTdBXHU5NUY0XHU1MjREXHU3RjAwXHUzMDAyXHJcbiAgICAgIGRpcmVjdG9yeUFzTmFtZXNwYWNlOiB0cnVlLFxyXG5cclxuICAgICAgZHRzOiByZXNvbHZlKF9fZGlybmFtZSwgXCJzcmNcIiwgXCJjb21wb25lbnRzLmQudHNcIiksXHJcbiAgICB9KSxcclxuICAgIEljb25zKHtcclxuICAgICAgYXV0b0luc3RhbGw6IHRydWUsXHJcbiAgICB9KSxcclxuICAgIEluc3BlY3QoKSxcclxuICBdLFxyXG4gIHJlc29sdmU6IHtcclxuICAgIC8vIEFsaWFzIGNvbmZpZ3VyYXRpb246IHVzZSBAIHRvIHJlcHJlc2VudCB0aGUgc3JjIGRpcmVjdG9yeVxyXG4gICAgYWxpYXM6IHtcclxuICAgICAgXCJAXCI6IHJlc29sdmUoX19kaXJuYW1lLCBcInNyY1wiKSxcclxuICAgICAgXCJAY1wiOiByZXNvbHZlKF9fZGlybmFtZSwgXCJzcmMvY29tcG9uZW50c1wiKSxcclxuICAgICAgXCJAY3NzXCI6IHJlc29sdmUoX19kaXJuYW1lLCBcInNyYy9hc3NldHMvY3NzXCIpLFxyXG4gICAgICBcIkBpbWdcIjogcmVzb2x2ZShfX2Rpcm5hbWUsIFwic3JjL2Fzc2V0cy9pbWdcIiksXHJcbiAgICB9LFxyXG4gIH0sXHJcbiAgLy8gICBzZXJ2ZXI6IHtcclxuICAvLyAgICAgLy8gRW5hYmxlIHRoZSBwcm94eVxyXG4gIC8vICAgICBwcm94eToge1xyXG4gIC8vICAgICAgIFwiL2FwaVwiOiB7XHJcbiAgLy8gICAgICAgICB0YXJnZXQ6IFwiaHR0cDovL2xvY2FsaG9zdDozMDAwXCIsXHJcbiAgLy8gICAgICAgICBjaGFuZ2VPcmlnaW46IHRydWUsXHJcbiAgLy8gICAgICAgICByZXdyaXRlOiAocGF0aCkgPT4gcGF0aC5yZXBsYWNlKC9eXFwvYXBpLywgXCJcIiksXHJcbiAgLy8gICAgICAgfSxcclxuICAvLyAgICAgfSxcclxuICAvLyAgICAgLy8gQWxsb3cgdGhlIENPUlNcclxuICAvLyAgICAgaGVhZGVyczoge1xyXG4gIC8vICAgICAgIFwiQWNjZXNzLUNvbnRyb2wtQWxsb3ctT3JpZ2luXCI6IFwiKlwiLFxyXG4gIC8vICAgICAgIFwiQWNjZXNzLUNvbnRyb2wtQWxsb3ctTWV0aG9kc1wiOiBcIkdFVCwgUE9TVCwgUFVULCBERUxFVEUsIFBBVENILCBPUFRJT05TXCIsXHJcbiAgLy8gICAgICAgXCJBY2Nlc3MtQ29udHJvbC1BbGxvdy1IZWFkZXJzXCI6XHJcbiAgLy8gICAgICAgICBcIlgtUmVxdWVzdGVkLVdpdGgsIGNvbnRlbnQtdHlwZSwgQXV0aG9yaXphdGlvblwiLFxyXG4gIC8vICAgICB9LFxyXG4gIC8vICAgfSxcclxufSk7XHJcbiJdLAogICJtYXBwaW5ncyI6ICI7QUFBc2EsU0FBUyxvQkFBb0I7QUFDbmMsT0FBTyxTQUFTO0FBQ2hCLE9BQU8sYUFBYTtBQUNwQixPQUFPLFdBQVc7QUFDbEIsT0FBTyxnQkFBZ0I7QUFDdkIsT0FBTyxnQkFBZ0I7QUFDdkIsT0FBTyxtQkFBbUI7QUFDMUIsU0FBUywyQkFBMkI7QUFDcEMsU0FBUyxlQUFlO0FBUnhCLElBQU0sbUNBQW1DO0FBV3pDLElBQU8sc0JBQVEsYUFBYTtBQUFBLEVBQzFCLFNBQVM7QUFBQSxJQUNQLElBQUk7QUFBQSxJQUNKLFdBQVc7QUFBQTtBQUFBO0FBQUEsTUFHVCxTQUFTLENBQUMsT0FBTyxZQUFZO0FBQUE7QUFBQTtBQUFBLE1BRzdCLFdBQVc7QUFBQSxRQUNULG9CQUFvQjtBQUFBO0FBQUE7QUFBQSxRQUdwQixjQUFjO0FBQUEsVUFDWixRQUFRO0FBQUEsUUFDVixDQUFDO0FBQUEsTUFDSDtBQUFBLE1BQ0EsS0FBSyxRQUFRLGtDQUFXLE9BQU8sbUJBQW1CO0FBQUE7QUFBQSxNQUVsRCxVQUFVO0FBQUE7QUFBQSxRQUVSLFNBQVM7QUFBQSxRQUNULFVBQVU7QUFBQTtBQUFBLFFBQ1Ysa0JBQWtCO0FBQUEsTUFDcEI7QUFBQSxJQUNGLENBQUM7QUFBQSxJQUNELFdBQVc7QUFBQSxNQUNULFdBQVc7QUFBQTtBQUFBO0FBQUEsUUFHVCxjQUFjO0FBQUEsVUFDWixvQkFBb0IsQ0FBQyxJQUFJO0FBQUEsUUFDM0IsQ0FBQztBQUFBO0FBQUE7QUFBQSxRQUdELG9CQUFvQjtBQUFBLE1BQ3RCO0FBQUE7QUFBQSxNQUVBLHNCQUFzQjtBQUFBLE1BRXRCLEtBQUssUUFBUSxrQ0FBVyxPQUFPLGlCQUFpQjtBQUFBLElBQ2xELENBQUM7QUFBQSxJQUNELE1BQU07QUFBQSxNQUNKLGFBQWE7QUFBQSxJQUNmLENBQUM7QUFBQSxJQUNELFFBQVE7QUFBQSxFQUNWO0FBQUEsRUFDQSxTQUFTO0FBQUE7QUFBQSxJQUVQLE9BQU87QUFBQSxNQUNMLEtBQUssUUFBUSxrQ0FBVyxLQUFLO0FBQUEsTUFDN0IsTUFBTSxRQUFRLGtDQUFXLGdCQUFnQjtBQUFBLE1BQ3pDLFFBQVEsUUFBUSxrQ0FBVyxnQkFBZ0I7QUFBQSxNQUMzQyxRQUFRLFFBQVEsa0NBQVcsZ0JBQWdCO0FBQUEsSUFDN0M7QUFBQSxFQUNGO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQWtCRixDQUFDOyIsCiAgIm5hbWVzIjogW10KfQo=
