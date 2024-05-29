// vite.config.ts
import { defineConfig } from "file:///root/Meteorological_prediction_platform/front_end/node_modules/vite/dist/node/index.js";
import vue from "file:///root/Meteorological_prediction_platform/front_end/node_modules/@vitejs/plugin-vue/dist/index.mjs";
import Inspect from "file:///root/Meteorological_prediction_platform/front_end/node_modules/vite-plugin-inspect/dist/index.mjs";
import Icons from "file:///root/Meteorological_prediction_platform/front_end/node_modules/unplugin-icons/dist/vite.js";
import AutoImport from "file:///root/Meteorological_prediction_platform/front_end/node_modules/unplugin-auto-import/dist/vite.js";
import Components from "file:///root/Meteorological_prediction_platform/front_end/node_modules/unplugin-vue-components/dist/vite.js";
import IconsResolver from "file:///root/Meteorological_prediction_platform/front_end/node_modules/unplugin-icons/dist/resolver.js";
import { ElementPlusResolver } from "file:///root/Meteorological_prediction_platform/front_end/node_modules/unplugin-vue-components/dist/resolvers.js";
import { resolve } from "path";
var __vite_injected_original_dirname = "/root/Meteorological_prediction_platform/front_end";
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
  // port: 80,
  // Allow the CORS
  // headers: {
  //   "Access-Control-Allow-Origin": "*",
  //   "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, PATCH, OPTIONS",
  //   "Access-Control-Allow-Headers":
  //     "X-Requested-With, content-type, Authorization",
  // },
  //   },
});
export {
  vite_config_default as default
};
//# sourceMappingURL=data:application/json;base64,ewogICJ2ZXJzaW9uIjogMywKICAic291cmNlcyI6IFsidml0ZS5jb25maWcudHMiXSwKICAic291cmNlc0NvbnRlbnQiOiBbImNvbnN0IF9fdml0ZV9pbmplY3RlZF9vcmlnaW5hbF9kaXJuYW1lID0gXCIvcm9vdC9NZXRlb3JvbG9naWNhbF9wcmVkaWN0aW9uX3BsYXRmb3JtL2Zyb250X2VuZFwiO2NvbnN0IF9fdml0ZV9pbmplY3RlZF9vcmlnaW5hbF9maWxlbmFtZSA9IFwiL3Jvb3QvTWV0ZW9yb2xvZ2ljYWxfcHJlZGljdGlvbl9wbGF0Zm9ybS9mcm9udF9lbmQvdml0ZS5jb25maWcudHNcIjtjb25zdCBfX3ZpdGVfaW5qZWN0ZWRfb3JpZ2luYWxfaW1wb3J0X21ldGFfdXJsID0gXCJmaWxlOi8vL3Jvb3QvTWV0ZW9yb2xvZ2ljYWxfcHJlZGljdGlvbl9wbGF0Zm9ybS9mcm9udF9lbmQvdml0ZS5jb25maWcudHNcIjtpbXBvcnQgeyBkZWZpbmVDb25maWcgfSBmcm9tIFwidml0ZVwiO1xuaW1wb3J0IHZ1ZSBmcm9tIFwiQHZpdGVqcy9wbHVnaW4tdnVlXCI7XG5pbXBvcnQgSW5zcGVjdCBmcm9tIFwidml0ZS1wbHVnaW4taW5zcGVjdFwiO1xuaW1wb3J0IEljb25zIGZyb20gXCJ1bnBsdWdpbi1pY29ucy92aXRlXCI7XG5pbXBvcnQgQXV0b0ltcG9ydCBmcm9tIFwidW5wbHVnaW4tYXV0by1pbXBvcnQvdml0ZVwiO1xuaW1wb3J0IENvbXBvbmVudHMgZnJvbSBcInVucGx1Z2luLXZ1ZS1jb21wb25lbnRzL3ZpdGVcIjtcbmltcG9ydCBJY29uc1Jlc29sdmVyIGZyb20gXCJ1bnBsdWdpbi1pY29ucy9yZXNvbHZlclwiO1xuaW1wb3J0IHsgRWxlbWVudFBsdXNSZXNvbHZlciB9IGZyb20gXCJ1bnBsdWdpbi12dWUtY29tcG9uZW50cy9yZXNvbHZlcnNcIjtcbmltcG9ydCB7IHJlc29sdmUgfSBmcm9tIFwicGF0aFwiO1xuXG4vLyBodHRwczovL3ZpdGVqcy5kZXYvY29uZmlnL1xuZXhwb3J0IGRlZmF1bHQgZGVmaW5lQ29uZmlnKHtcbiAgcGx1Z2luczogW1xuICAgIHZ1ZSgpLFxuICAgIEF1dG9JbXBvcnQoe1xuICAgICAgLy8gQXV0byBpbXBvcnQgZnVuY3Rpb25zIGZyb20gVnVlLCBlLmcuIHJlZiwgcmVhY3RpdmUsIHRvUmVmLi4uXG4gICAgICAvLyBcdTgxRUFcdTUyQThcdTVCRkNcdTUxNjUgVnVlIFx1NzZGOFx1NTE3M1x1NTFGRFx1NjU3MFx1RkYwQ1x1NTk4Mlx1RkYxQXJlZiwgcmVhY3RpdmUsIHRvUmVmIFx1N0I0OVxuICAgICAgaW1wb3J0czogW1widnVlXCIsIFwidnVlLXJvdXRlclwiXSxcbiAgICAgIC8vIEF1dG8gaW1wb3J0IGZ1bmN0aW9ucyBmcm9tIEVsZW1lbnQgUGx1cywgZS5nLiBFbE1lc3NhZ2UsIEVsTWVzc2FnZUJveC4uLiAod2l0aCBzdHlsZSlcbiAgICAgIC8vIFx1ODFFQVx1NTJBOFx1NUJGQ1x1NTE2NSBFbGVtZW50IFBsdXMgXHU3NkY4XHU1MTczXHU1MUZEXHU2NTcwXHVGRjBDXHU1OTgyXHVGRjFBRWxNZXNzYWdlLCBFbE1lc3NhZ2VCb3guLi4gKFx1NUUyNlx1NjgzN1x1NUYwRilcbiAgICAgIHJlc29sdmVyczogW1xuICAgICAgICBFbGVtZW50UGx1c1Jlc29sdmVyKCksXG4gICAgICAgIC8vIEF1dG8gaW1wb3J0IGljb24gY29tcG9uZW50c1xuICAgICAgICAvLyBcdTgxRUFcdTUyQThcdTVCRkNcdTUxNjVcdTU2RkVcdTY4MDdcdTdFQzRcdTRFRjZcbiAgICAgICAgSWNvbnNSZXNvbHZlcih7XG4gICAgICAgICAgcHJlZml4OiBcIkljb25cIixcbiAgICAgICAgfSksXG4gICAgICBdLFxuICAgICAgZHRzOiByZXNvbHZlKF9fZGlybmFtZSwgXCJzcmNcIiwgXCJhdXRvLWltcG9ydHMuZC50c1wiKSxcbiAgICAgIC8vIFx1ODlFM1x1NTFCM2VzbGludFx1NjJBNVx1OTUxOVx1OTVFRVx1OTg5OFxuICAgICAgZXNsaW50cmM6IHtcbiAgICAgICAgLy8gXHU4RkQ5XHU5MUNDXHU1MTQ4XHU4QkJFXHU3RjZFXHU2MjEwdHJ1ZVx1NzEzNlx1NTQwRW5wbSBydW4gZGV2IFx1OEZEMFx1ODg0Q1x1NEU0Qlx1NTQwRVx1NEYxQVx1NzUxRlx1NjIxMCAuZXNsaW50cmMtYXV0by1pbXBvcnQuanNvbiBcdTY1ODdcdTRFRjZcdTRFNEJcdTU0MEVcdUZGMENcdTU3MjhcdTY1MzlcdTRFM0FmYWxzZVxuICAgICAgICBlbmFibGVkOiBmYWxzZSxcbiAgICAgICAgZmlsZXBhdGg6IFwiLi8uZXNsaW50cmMtYXV0by1pbXBvcnQuanNvblwiLCAvLyBcdTc1MUZcdTYyMTBcdTc2ODRcdTY1ODdcdTRFRjZcdThERUZcdTVGODRcbiAgICAgICAgZ2xvYmFsc1Byb3BWYWx1ZTogdHJ1ZSxcbiAgICAgIH0sXG4gICAgfSksXG4gICAgQ29tcG9uZW50cyh7XG4gICAgICByZXNvbHZlcnM6IFtcbiAgICAgICAgLy8gQXV0byByZWdpc3RlciBpY29uIGNvbXBvbmVudHNcbiAgICAgICAgLy8gXHU4MUVBXHU1MkE4XHU2Q0U4XHU1MThDXHU1NkZFXHU2ODA3XHU3RUM0XHU0RUY2XG4gICAgICAgIEljb25zUmVzb2x2ZXIoe1xuICAgICAgICAgIGVuYWJsZWRDb2xsZWN0aW9uczogW1wiZXBcIl0sXG4gICAgICAgIH0pLFxuICAgICAgICAvLyBBdXRvIHJlZ2lzdGVyIEVsZW1lbnQgUGx1cyBjb21wb25lbnRzXG4gICAgICAgIC8vIFx1ODFFQVx1NTJBOFx1NUJGQ1x1NTE2NSBFbGVtZW50IFBsdXMgXHU3RUM0XHU0RUY2XG4gICAgICAgIEVsZW1lbnRQbHVzUmVzb2x2ZXIoKSxcbiAgICAgIF0sXG4gICAgICAvLyBcdTUxNDFcdThCQjhcdTVCNTBcdTc2RUVcdTVGNTVcdTRGNUNcdTRFM0FcdTdFQzRcdTRFRjZcdTc2ODRcdTU0N0RcdTU0MERcdTdBN0FcdTk1RjRcdTUyNERcdTdGMDBcdTMwMDJcbiAgICAgIGRpcmVjdG9yeUFzTmFtZXNwYWNlOiB0cnVlLFxuXG4gICAgICBkdHM6IHJlc29sdmUoX19kaXJuYW1lLCBcInNyY1wiLCBcImNvbXBvbmVudHMuZC50c1wiKSxcbiAgICB9KSxcbiAgICBJY29ucyh7XG4gICAgICBhdXRvSW5zdGFsbDogdHJ1ZSxcbiAgICB9KSxcbiAgICBJbnNwZWN0KCksXG4gIF0sXG4gIHJlc29sdmU6IHtcbiAgICAvLyBBbGlhcyBjb25maWd1cmF0aW9uOiB1c2UgQCB0byByZXByZXNlbnQgdGhlIHNyYyBkaXJlY3RvcnlcbiAgICBhbGlhczoge1xuICAgICAgXCJAXCI6IHJlc29sdmUoX19kaXJuYW1lLCBcInNyY1wiKSxcbiAgICAgIFwiQGNcIjogcmVzb2x2ZShfX2Rpcm5hbWUsIFwic3JjL2NvbXBvbmVudHNcIiksXG4gICAgICBcIkBjc3NcIjogcmVzb2x2ZShfX2Rpcm5hbWUsIFwic3JjL2Fzc2V0cy9jc3NcIiksXG4gICAgICBcIkBpbWdcIjogcmVzb2x2ZShfX2Rpcm5hbWUsIFwic3JjL2Fzc2V0cy9pbWdcIiksXG4gICAgfSxcbiAgfSxcbi8vICAgc2VydmVyOiB7XG4gICAgLy8gcG9ydDogODAsXG4gICAgLy8gQWxsb3cgdGhlIENPUlNcbiAgICAvLyBoZWFkZXJzOiB7XG4gICAgLy8gICBcIkFjY2Vzcy1Db250cm9sLUFsbG93LU9yaWdpblwiOiBcIipcIixcbiAgICAvLyAgIFwiQWNjZXNzLUNvbnRyb2wtQWxsb3ctTWV0aG9kc1wiOiBcIkdFVCwgUE9TVCwgUFVULCBERUxFVEUsIFBBVENILCBPUFRJT05TXCIsXG4gICAgLy8gICBcIkFjY2Vzcy1Db250cm9sLUFsbG93LUhlYWRlcnNcIjpcbiAgICAvLyAgICAgXCJYLVJlcXVlc3RlZC1XaXRoLCBjb250ZW50LXR5cGUsIEF1dGhvcml6YXRpb25cIixcbiAgICAvLyB9LFxuLy8gICB9LFxufSk7XG4iXSwKICAibWFwcGluZ3MiOiAiO0FBQXdVLFNBQVMsb0JBQW9CO0FBQ3JXLE9BQU8sU0FBUztBQUNoQixPQUFPLGFBQWE7QUFDcEIsT0FBTyxXQUFXO0FBQ2xCLE9BQU8sZ0JBQWdCO0FBQ3ZCLE9BQU8sZ0JBQWdCO0FBQ3ZCLE9BQU8sbUJBQW1CO0FBQzFCLFNBQVMsMkJBQTJCO0FBQ3BDLFNBQVMsZUFBZTtBQVJ4QixJQUFNLG1DQUFtQztBQVd6QyxJQUFPLHNCQUFRLGFBQWE7QUFBQSxFQUMxQixTQUFTO0FBQUEsSUFDUCxJQUFJO0FBQUEsSUFDSixXQUFXO0FBQUE7QUFBQTtBQUFBLE1BR1QsU0FBUyxDQUFDLE9BQU8sWUFBWTtBQUFBO0FBQUE7QUFBQSxNQUc3QixXQUFXO0FBQUEsUUFDVCxvQkFBb0I7QUFBQTtBQUFBO0FBQUEsUUFHcEIsY0FBYztBQUFBLFVBQ1osUUFBUTtBQUFBLFFBQ1YsQ0FBQztBQUFBLE1BQ0g7QUFBQSxNQUNBLEtBQUssUUFBUSxrQ0FBVyxPQUFPLG1CQUFtQjtBQUFBO0FBQUEsTUFFbEQsVUFBVTtBQUFBO0FBQUEsUUFFUixTQUFTO0FBQUEsUUFDVCxVQUFVO0FBQUE7QUFBQSxRQUNWLGtCQUFrQjtBQUFBLE1BQ3BCO0FBQUEsSUFDRixDQUFDO0FBQUEsSUFDRCxXQUFXO0FBQUEsTUFDVCxXQUFXO0FBQUE7QUFBQTtBQUFBLFFBR1QsY0FBYztBQUFBLFVBQ1osb0JBQW9CLENBQUMsSUFBSTtBQUFBLFFBQzNCLENBQUM7QUFBQTtBQUFBO0FBQUEsUUFHRCxvQkFBb0I7QUFBQSxNQUN0QjtBQUFBO0FBQUEsTUFFQSxzQkFBc0I7QUFBQSxNQUV0QixLQUFLLFFBQVEsa0NBQVcsT0FBTyxpQkFBaUI7QUFBQSxJQUNsRCxDQUFDO0FBQUEsSUFDRCxNQUFNO0FBQUEsTUFDSixhQUFhO0FBQUEsSUFDZixDQUFDO0FBQUEsSUFDRCxRQUFRO0FBQUEsRUFDVjtBQUFBLEVBQ0EsU0FBUztBQUFBO0FBQUEsSUFFUCxPQUFPO0FBQUEsTUFDTCxLQUFLLFFBQVEsa0NBQVcsS0FBSztBQUFBLE1BQzdCLE1BQU0sUUFBUSxrQ0FBVyxnQkFBZ0I7QUFBQSxNQUN6QyxRQUFRLFFBQVEsa0NBQVcsZ0JBQWdCO0FBQUEsTUFDM0MsUUFBUSxRQUFRLGtDQUFXLGdCQUFnQjtBQUFBLElBQzdDO0FBQUEsRUFDRjtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBV0YsQ0FBQzsiLAogICJuYW1lcyI6IFtdCn0K
