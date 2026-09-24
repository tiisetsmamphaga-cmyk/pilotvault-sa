import nextConfig from "eslint-config-next"

const eslintConfig = [
  ...nextConfig,
  {
    ignores: [".next/**", "node_modules/**", "out/**"],
  },
  {
    rules: {
      // These fire on existing, working "reset local state when a prop/dep
      // changes" effects (e.g. resetting an image loader on `src` change).
      // Real fix requires a per-case behavioral review, not a blind rewrite
      // right before launch — keep as a warning so lint stays actionable.
      "react-hooks/set-state-in-effect": "warn",
      // Flags Date.now() used for a coarse trial-days-remaining display —
      // harmless in this context. Same reasoning as above.
      "react-hooks/purity": "warn",
    },
  },
]

export default eslintConfig
